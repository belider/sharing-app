import os
import requests
import uuid
import base64
import json
from dotenv import load_dotenv
import logging
from pyicloud import PyiCloudService
from pyicloud.exceptions import PyiCloudFailedLoginException

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()

ICLOUD_USERNAME = os.getenv('ICLOUD_USERNAME')
ICLOUD_PASSWORD = os.getenv('ICLOUD_PASSWORD')

def authenticate_icloud():
    logger.debug(f"Attempting to authenticate with username: {ICLOUD_USERNAME}")
    
    try:
        api = PyiCloudService(ICLOUD_USERNAME, ICLOUD_PASSWORD)
        
        if api.requires_2fa:
            print("Two-factor authentication required.")
            code = input("Enter the code you received on one of your approved devices: ")
            result = api.validate_2fa_code(code)
            logger.debug(f"2FA code validation result: {result}")

            if not result:
                raise PyiCloudFailedLoginException("Failed to verify 2FA code")

        logger.debug("Authentication successful")
        return api
    except PyiCloudFailedLoginException as e:
        logger.error(f"Login failed: {str(e)}")
        return None


# def get_notes(api):
#     try:
#         logger.debug("Attempting to fetch notes")
#         # Здесь будет код для получения заметок
#         # Пока что возвращаем пустой список
#         return []
#     except Exception as e:
#         logger.error(f"Error getting notes: {e}")
#         return []

def get_notes(api):
    try:
        # Настройка URL и параметров запроса
        url = "https://p140-ckdatabasews.icloud.com/database/1/com.apple.notes/production/private/records/query"
        
        # Параметры запроса (их можно также динамически определять, если это необходимо)
        params = {
            "ckjsBuildVersion": "2310ProjectDev27",
            "ckjsVersion": "2.6.4",
            "clientId": "d244e81c-50ac-47ea-aac2-d03f52876266",
            "clientBuildNumber": "2420Project27",
            "clientMasteringNumber": "2420B21",
            "dsid": api.session["dsid"]
        }

        # Заголовки запроса
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-GB,en;q=0.9",
            "Connection": "keep-alive",
            "Content-Type": "text/plain",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
            "Cookie": api.session.cookies.get_dict(),  # Вставляем куки из текущей сессии
        }

        # Тело запроса
        payload = {
            "records": []
        }

        # Выполнение POST-запроса
        response = requests.post(url, headers=headers, params=params, data=json.dumps(payload))
        response.raise_for_status()  # Проверка на ошибки HTTP

        notes = response.json()
        logger.debug(f"Response content: {json.dumps(notes, indent=2)}")

        if notes:
            logger.debug(f"Total notes retrieved: {len(notes)}")
            return notes
        else:
            logger.info("No notes found.")
            return []
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to retrieve notes: {e}")
        return []