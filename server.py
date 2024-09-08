from flask import Flask, request, jsonify, abort, send_file, render_template_string
import embeddings_service
from db_service import DatabaseService
from datetime import datetime
from dotenv import load_dotenv
import os
import logging
from flask_apscheduler import APScheduler
from sync_notes import sync_notes, accept_invite
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()
API_KEY = os.getenv('GPTS_API_KEY')
IS_TEST_ENV = os.getenv('IS_TEST_ENV', 'false').lower() == 'true'
SERVER_KEY = os.getenv('SERVER_KEY')

app = Flask(__name__)
db_service = DatabaseService()

# Инициализация планировщика
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

# Глобальная переменная для хранения кода подтверждения
verification_code = None

# HTML шаблон для страницы ввода кода
AUTH_PAGE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>iCloud Authentication</title>
</head>
<body>
    <h2>Enter iCloud Verification Code</h2>
    <form action="/submit_code" method="post">
        <input type="text" name="code" placeholder="Enter verification code">
        <input type="hidden" name="key" value="{{ key }}">
        <input type="submit" value="Submit">
    </form>
</body>
</html>
"""

@app.route('/icloud_auth')
def server_auth():
    key = request.args.get('key')
    if key != SERVER_KEY:
        abort(401, description="Unauthorized")
    return render_template_string(AUTH_PAGE_TEMPLATE, key=key)

@app.route('/submit_code', methods=['POST'])
def submit_code():
    global verification_code
    key = request.form.get('key')
    if key != SERVER_KEY:
        abort(401, description="Unauthorized")
    verification_code = request.form.get('code')
    return "Code submitted successfully"

@app.route('/icloud_auth_status')
def icloud_auth_status():
    key = request.args.get('key')
    if key != SERVER_KEY:
        abort(401, description="Unauthorized")
    global verification_code
    if verification_code:
        code = verification_code
        verification_code = None  # Сбрасываем код после получения
        return jsonify({"code": code})
    return jsonify({"code": None})

@app.route('/privacy', methods=['GET'])
def privacy_policy():
    return send_file('privacy_policy.html')

# def authenticate_request():
#     auth_header = request.headers.get('Authorization')
#     if auth_header != f"Bearer {API_KEY}":
#         abort(401, description="Unauthorized: Invalid API key")

from functools import wraps
from flask import request, abort

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header != f"Bearer {API_KEY}":
            abort(401, description="Unauthorized: Invalid API key")
        return f(*args, **kwargs)
    return decorated_function

@app.route('/search', methods=['POST'])
@require_api_key
def search():
    data = request.json

    # Проверяем, что поле search_text присутствует в запросе
    if 'search_query' not in data:
        return jsonify({'error': 'Missing search_text parameter'}), 400

    query_text = data['search_query']
    max_tokens = 8192
    num_tokens = embeddings_service.num_tokens_from_string(query_text)

    # Если текст длиннее, чем 8192 токена, обрезаем его
    if num_tokens > max_tokens:
        query_text = embeddings_service.truncate_text(query_text, max_tokens)

    # Получаем эмбеддинги для текста
    query_vector = embeddings_service.create_embedding(query_text)

    # Хардкод владельца заметок, по которым происходит поиск
    # Позже можно будет заменить owner_id на параметр запроса или извлекать его из авторизации
    owner_id = "_5e1e01c1b9373143f359de4bd060d2fd"
    
    # Выполняем векторный поиск
    results = db_service.vector_search_notes(query_vector=query_vector, owner_id=owner_id)

    if not results:
        return jsonify({'error': 'No results found or an error occurred'}), 404

    # Форматируем результаты в текстовый ответ
    response_text = f"""Below is a list of notes found for different dates. Newer ones are more important, and information in older notes from more than a month ago may already be outdated. Current date is {datetime.now().strftime('%d %B %Y, %H:%M')}. Use these notes to craft the most helpful response to the query. If the question was about the present or future make sure to clarify that this is how you noted it earlier. \n\n"""
    
    for i, result in enumerate(results, start=1):
        response_text += f"""**Note {i} content:**\n```\n{result['text']}\n```\n\n"""

    return jsonify({'response': response_text})

@app.route('/accept_shared_folder', methods=['POST'])
@require_api_key
def accept_shared_folder_route():
    logger.debug("Received request to /accept_shared_folder")
    
    data = request.json
    logger.debug(f"Received data: {data}")
    
    if not data or 'url' not in data:
        logger.error("Missing url parameter")
        return jsonify({'error': 'Missing url parameter'}), 400
    
    url = data['url']
    guid = re.search(r'([a-zA-Z0-9]+)$', url)
    
    if not guid:
        logger.error(f"Invalid URL format: {url}")
        return jsonify({'error': 'Invalid URL format'}), 400
    
    guid = guid.group(1)
    logger.debug(f"Extracted GUID: {guid}")
    
    try:
        result = accept_invite(db_service, guid)
        logger.debug(f"Result from accept_invite: {result}")
        return jsonify({'message': f'Shared folder invitation processed for GUID: {guid}'}), 200
    except Exception as e:
        logger.exception(f"Error processing shared folder invitation: {str(e)}")
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


# Функция для синхронизации
@scheduler.task('cron', id='do_sync', hour='*') # minute='*/2')
def scheduled_sync():
    with app.app_context():
        app.logger.info("Starting scheduled sync")
        sync_notes(db_service)
        app.logger.info("Scheduled sync completed")


if __name__ == "__main__":
    if IS_TEST_ENV:
        logger.info("Starting server in development mode...")
        app.run(host='0.0.0.0', port=8080, debug=True)
    else:
        logger.info("Starting server in production mode...")
        from waitress import serve
        serve(app, host='0.0.0.0', port=8080)
        logger.info("Server is running on http://0.0.0.0:8080")