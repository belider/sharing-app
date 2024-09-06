import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import logging
import certifi
import pickle
import base64
from http.cookiejar import Cookie
from icloudpy import ICloudPyService
import time

# Настройка логирования
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # Устанавливаем уровень логирования на INFO

load_dotenv()

ICLOUD_USERNAME = os.getenv('ICLOUD_USERNAME')
ICLOUD_PASSWORD = os.getenv('ICLOUD_PASSWORD')

class DatabaseService:
    def __init__(self):
        self.client = None
        self.db = None
        self.notes_collection = None
        self.initialize_db()

    def initialize_db(self):
        try:
            uri = os.getenv('MONGODB_URI')
            if not uri:
                raise ValueError("MONGODB_URI not found in environment variables")

            # self.client = MongoClient(uri, server_api=ServerApi('1'))
            self.client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
            self.db = self.client['apple-notes']
            self.notes_collection = self.db['notes']
            self.sessions_collection = self.db['sessions']
            
            # Проверка подключения
            self.client.admin.command('ping')
            logger.info("Successfully connected to MongoDB")
        except Exception as e:
            logger.error(f"An error occurred while connecting to MongoDB: {e}")
            raise
    
    def save_session(self, api):
        try:
            logger.debug(f"Attempting to save session for user: {ICLOUD_USERNAME}")
            
            # Преобразуем cookies в сериализуемый формат
            cookies_dict = {}
            for cookie in api.session.cookies:
                cookies_dict[cookie.name] = {
                    'value': cookie.value,
                    'domain': cookie.domain,
                    'path': cookie.path,
                    'secure': cookie.secure,
                    'expires': cookie.expires
                }
            
            session_data = {
                'session_cookies': cookies_dict,
                'session_token': getattr(api, 'session_token', None),
                'client_id': getattr(api, 'client_id', None)
            }
            
            # Добавим временную метку, чтобы обеспечить обновление при каждом сохранении
            session_data['last_updated'] = time.time()
            
            result = self.sessions_collection.update_one(
                {"username": ICLOUD_USERNAME},
                {"$set": {"session_data": session_data}},
                upsert=True
            )
            if result.modified_count > 0:
                logger.info(f"Session updated for user: {ICLOUD_USERNAME}")
            elif result.upserted_id:
                logger.info(f"New session inserted for user: {ICLOUD_USERNAME}")
            else:
                logger.warning(f"Session was not modified for user: {ICLOUD_USERNAME}")
            return result.modified_count > 0 or result.upserted_id is not None
        except Exception as e:
            logger.error(f"Error saving session: {str(e)}")
            logger.error(f"Session data: {session_data}")  # Добавим это для отладки
            return False

    def load_session(self):
        try:
            logger.debug(f"Attempting to load session for user: {ICLOUD_USERNAME}")
            result = self.sessions_collection.find_one({"username": ICLOUD_USERNAME})
            if result and 'session_data' in result:
                session_data = result['session_data']
                
                from icloudpy import ICloudPyService
                api = ICloudPyService(ICLOUD_USERNAME, ICLOUD_PASSWORD)
                
                # Обновляем cookies
                for name, cookie_data in session_data['session_cookies'].items():
                    cookie = Cookie(
                        version=0, 
                        name=name, 
                        value=cookie_data['value'],
                        port=None, 
                        port_specified=False,
                        domain=cookie_data['domain'],
                        domain_specified=bool(cookie_data['domain']),
                        domain_initial_dot=cookie_data['domain'].startswith('.'),
                        path=cookie_data['path'], 
                        path_specified=bool(cookie_data['path']),
                        secure=cookie_data['secure'],
                        expires=cookie_data['expires'],
                        discard=False,
                        comment=None,
                        comment_url=None,
                        rest={"HttpOnly": None},
                        rfc2109=False
                    )
                    api.session.cookies.set_cookie(cookie)
                
                if 'session_token' in session_data and session_data['session_token']:
                    api.session_token = session_data['session_token']
                if 'client_id' in session_data and session_data['client_id']:
                    api.client_id = session_data['client_id']
                
                logger.info(f"Session loaded successfully for user: {ICLOUD_USERNAME}")
                return api
            logger.info(f"No session found for user: {ICLOUD_USERNAME}")
            return None
        except Exception as e:
            logger.error(f"Error loading session: {str(e)}")
            return None

    def insert_or_update(self, note_data):
        try:
            # Проверяем наличие обязательных полей
            required_fields = ['title', 'text', 'record_id', 'created_date', 'last_edited_date', 
                               'folder_id', 'folder_name', 'owner_id', 'embeddings']
            for field in required_fields:
                if field not in note_data:
                    raise ValueError(f"Missing required field: {field}")

            # Подготовка данных для вставки/обновления
            query = {"record_id": note_data["record_id"]}
            update = {"$set": note_data}

            # Вставка или обновление документа
            result = self.notes_collection.update_one(query, update, upsert=True)

            if result.upserted_id:
                logger.info(f"Inserted new note with ID: {result.upserted_id}")
            else:
                logger.info(f"Updated existing note with ID: {note_data['record_id']}")

            return result.upserted_id or note_data['record_id']

        except Exception as e:
            logger.error(f"An error occurred while inserting/updating note: {e}")
            raise

    def get_last_edited_dates(self):
        result = {}
        for note in self.notes_collection.find({}, {'record_id': 1, 'last_edited_date': 1}):
            result[note['record_id']] = note['last_edited_date']
        return result
    
    def close_connection(self):
        if self.client:
            self.client.close()
            logger.info("Closed connection to MongoDB")
    
    # Метод для векторного поиска
    def vector_search_notes(self, query_vector, owner_id, index_name="content_vector_index", limit=5, num_candidates=100):
        try:
            pipeline = [
                {
                    '$vectorSearch': {
                        'index': index_name,
                        'path': 'embeddings', 
                        'queryVector': query_vector,
                        'numCandidates': num_candidates,
                        'limit': limit,
                        'filter': {
                            'owner_id': owner_id
                        }
                    }
                },
                {
                    '$addFields': {
                        'score': {'$meta': 'vectorSearchScore'}
                    }
                },
                {
                    '$project': {
                        '_id': 0,  # Исключаем поле _id, если оно вам не нужно
                        'score': 1,  # Явно включаем поле score
                        # Добавляем все остальные поля
                        'record_id': 1,
                        'owner_id': 1, 
                        'created_date': 1, 
                        'last_edited_date': 1, 
                        'folder_name': 1, 
                        'title': 1,    
                        'text': 1
                    }
                }
            ]
            results = list(self.notes_collection.aggregate(pipeline))
            return results
        
        except Exception as e:
            logger.error(f"Vector search failed: {e}")
            return None

# Пример использования
if __name__ == "__main__":
    db_service = DatabaseService()
    
    test_note = {
        'title': 'Test Note',
        'text': 'This is a test note',
        'record_id': 'test123',
        'created_date': 1234567890,
        'last_edited_date': 1234567891,
        'folder_id': 'folder123',
        'folder_name': 'Test Folder',
        'owner_id': 'owner123',
        'embeddings': [0.1, 0.2, 0.3] * 1024  # Пример эмбеддинга размерностью 3072
    }
    
    db_service.insert_or_update(test_note)
    db_service.close_connection()