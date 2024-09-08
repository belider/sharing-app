import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import logging
import certifi
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