from flask import Flask, request, jsonify, abort, send_file
import embeddings_service
from db_service import DatabaseService
from datetime import datetime
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()
API_KEY = os.getenv('GPTS_API_KEY')
IS_TEST_ENV = os.getenv('IS_TEST_ENV', 'false').lower() == 'true'

app = Flask(__name__)
db_service = DatabaseService()

def authenticate_request():
    auth_header = request.headers.get('Authorization')
    if auth_header != f"Bearer {API_KEY}":
        abort(401, description="Unauthorized: Invalid API key")

@app.route('/privacy', methods=['GET'])
def privacy_policy():
    return send_file('privacy_policy.html')

@app.route('/search', methods=['POST'])
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
    response_text = f"""Below is a list of notes found for different dates. Newer ones are more important, and information in older notes from more than a month ago may already be outdated. Current date is {datetime.now().strftime('%d %B %Y, %H:%M')}. Use these notes to craft the most helpful response to the query. If context requires referencing older notes. If the question was about the present or futuremake sure to clarify that this is how you noted it earlier. \n\n"""
    
    for i, result in enumerate(results, start=1):
        # response_text += f"**Note {i}:** {result['title']}\n"
        # response_text += f"**Folder:** {result['folder_name']}\n"
        # response_text += f"**Created date:** {embeddings_service.format_timestamp(result['created_date'])}\n"
        # response_text += f"**Last modified date:** {embeddings_service.format_timestamp(result['last_edited_date'])}\n"
        response_text += f"""**Note {i} content:**\n```\n{result['text']}\n```\n\n"""

    return jsonify({'response': response_text})

if __name__ == "__main__":
    if IS_TEST_ENV:
        logger.info("Starting server in development mode...")
        app.run(host='0.0.0.0', port=8080, debug=True)
    else:
        logger.info("Starting server in production mode...")
        from waitress import serve
        serve(app, host='0.0.0.0', port=8080)
        logger.info("Server is running on http://0.0.0.0:8080")