import os
import requests
import json
import base64
import logging
from icloudpy import ICloudPyService
from icloudpy.exceptions import ICloudPyFailedLoginException
from dotenv import load_dotenv
from decrypt import decrypt_note_text
import time

# Настройка логирования
# logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # Устанавливаем уровень логирования на INFO

load_dotenv()

ICLOUD_USERNAME = os.getenv('ICLOUD_USERNAME')
ICLOUD_PASSWORD = os.getenv('ICLOUD_PASSWORD')
SERVER_KEY = os.getenv('SERVER_KEY', '')
SERVER_URL = os.getenv('SERVER_URL', 'http://localhost:8080')


def authenticate_icloud():
    logger.debug(f"Attempting to authenticate with username: {ICLOUD_USERNAME}")
    
    try:
        api = ICloudPyService(ICLOUD_USERNAME, ICLOUD_PASSWORD)
        
        if api.requires_2fa:
            logger.info("Two-factor authentication required.")
            
            # Ожидаем ввода кода пользователем через веб-интерфейс
            auth_url = f"{SERVER_URL}/server_auth?key={SERVER_KEY}"
            logger.info(f"Please enter the verification code at: {auth_url}")
            
            # Ожидаем ввода кода
            code = None
            start_time = time.time()
            while not code and (time.time() - start_time) < 300:  # Ждем максимум 5 минут
                response = requests.get(f"{SERVER_URL}/icloud_auth_status?key={SERVER_KEY}")
                if response.status_code == 200:
                    data = response.json()
                    code = data.get('code')
                if not code:
                    time.sleep(5)  # Пауза перед следующей проверкой
            
            if not code:
                raise ICloudPyFailedLoginException("Timeout waiting for verification code")
            
            result = api.validate_2fa_code(code)
            logger.debug(f"2FA code validation result: {result}")

            if not result:
                raise ICloudPyFailedLoginException("Failed to verify 2FA code")

        logger.debug("Authentication successful")
        return api
    except ICloudPyFailedLoginException as e:
        logger.error(f"Login failed: {str(e)}")
        return None

# def authenticate_icloud():
#     logger.debug(f"Attempting to authenticate with username: {ICLOUD_USERNAME}")
    
#     try:
#         api = ICloudPyService(ICLOUD_USERNAME, ICLOUD_PASSWORD)
        
#         if api.requires_2fa:
#             print("Two-factor authentication required.")
#             code = input("Enter the code you received on one of your approved devices: ")
#             result = api.validate_2fa_code(code)
#             logger.debug(f"2FA code validation result: {result}")

#             if not result:
#                 raise ICloudPyFailedLoginException("Failed to verify 2FA code")

#         logger.debug("Authentication successful")
#         return api
#     except ICloudPyFailedLoginException as e:
#         logger.error(f"Login failed: {str(e)}")
#         return None


def setup_headers(api):
    """Создает заголовки и параметры запроса с использованием куки."""
    dsid = api.data['dsInfo']['dsid']

    if not dsid:
        raise ValueError("DSID not found in the session data.")
    
    params = {
        "ckjsBuildVersion": "2310ProjectDev27",
        "ckjsVersion": "2.6.4",
        "clientId": "d244e81c-50ac-47ea-aac2-d03f52876266",
        "clientBuildNumber": "2420Project27",
        "clientMasteringNumber": "2420B21",
        "dsid": dsid
    }

    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-GB,en;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "text/plain",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
        "Origin": "https://www.icloud.com",
        "Referer": "https://www.icloud.com/"
    }

    cookies = requests.utils.dict_from_cookiejar(api.session.cookies)
    headers['Cookie'] = '; '.join([f"{key}={value}" for key, value in cookies.items()])

    return headers, params


def get_zones(dsid, headers):
    """Получить список всех shared зон (папок)."""
    url = f'https://p140-ckdatabasews.icloud.com/database/1/com.apple.notes/production/shared/zones/list?dsid={dsid}'
    response = requests.get(url, headers=headers)
    
    logger.debug(f"Zones Response Status Code: {response.status_code}")
    logger.debug(f"Zones Response Content: {response.text}")
    
    if response.status_code == 200:
        return response.json().get('zones', [])
    else:
        response.raise_for_status()

def get_zone_changes(zone_id, owner_record_name, dsid, headers):
    """Получить изменения в конкретной зоне, включая заметки."""
    url = f'https://p140-ckdatabasews.icloud.com/database/1/com.apple.notes/production/shared/changes/zone?dsid={dsid}'
    payload = {
        "zones": [{
            "zoneID": {
                "zoneName": zone_id,
                "ownerRecordName": owner_record_name,
                "zoneType": "REGULAR_CUSTOM_ZONE"
            },
            "desiredKeys": [
                "TitleEncrypted", "SnippetEncrypted", "FirstAttachmentUTIEncrypted",
                "FirstAttachmentThumbnail", "CreationDate", "ModificationDate"
            ],
            "desiredRecordTypes": ["Note"]
        }]
    }
    response = requests.post(url, headers=headers, json=payload)
    
    logger.debug(f"Zone Changes Response Status Code: {response.status_code}")
    # logger.debug(f"Zone Changes Response Content: {response.text}")
    # Убедимся, что директория для логов существует
    os.makedirs('logs', exist_ok=True)
    
    with open(f'logs/zone_changes_logs.json', 'w', encoding='utf-8') as file:
        json.dump(response.json(), file, ensure_ascii=False, indent=4)
    
    if response.status_code == 200:
        # return response.json().get('records', [])
        records = []
        for zone in response.json().get('zones', []):
            zone_records = zone.get('records', [])
            records.extend(zone_records)
        
        if records:
            return records
        else:
            logger.warning("No 'records' found in the response.")
            return []
    else:
        response.raise_for_status()


def fetch_encryption_key(dsid, headers):
    """Fetch the encryption key using the dsid."""
    url = f'https://p140-keyvalueservice.icloud.com/json/sync?dsid={dsid}'
    payload = {
        "service-id": "appleprefs",
        "apps": [
            {"app-id": "notes3", "registry-version": ""},
            {"app-id": "account", "registry-version": ""}
        ]
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    logger.debug(f"Fetch encryption key Response Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        with open(f'logs/encryption_key_logs.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        
        # Поиск ключа, связанного с 'identifier': 'notes'
        for key in data.get('apps', []):
            if key.get('app-id') == 'account':
                for sub_key in key.get('keys', []):
                    if sub_key.get('data') and isinstance(sub_key['data'], dict):
                        for config in sub_key['data'].get('configurations', []):
                            if config.get('identifier') == 'notes':
                                encryption_key = config.get('uuid')
                                if encryption_key:
                                    return encryption_key
        
        raise ValueError("Encryption key not found in response")
    else:
        response.raise_for_status()


def get_folder_name(folder_id, zone_id, owner_record_name, dsid, headers):
    url = f'https://p140-ckdatabasews.icloud.com/database/1/com.apple.notes/production/shared/records/lookup?dsid={dsid}'
    payload = {
        "records": [{"recordName": folder_id}],
        "zoneID": {
            "zoneName": zone_id,
            "ownerRecordName": owner_record_name
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    
    # Логируем ответ в файл
    with open('logs/folder_name_response.json', 'w', encoding='utf-8') as log_file:
        json.dump(response.json(), log_file, ensure_ascii=False, indent=4)
    
    if response.status_code == 200:
        folder_data = response.json().get('records', [{}])[0]
        folder_name = folder_data.get('fields', {}).get('TitleEncrypted', {}).get('value', '')
        if folder_name:
            return base64.b64decode(folder_name).decode('utf-8')
    
    return folder_id


def get_note_details(record_name, zone_id, owner_record_name, dsid, headers):
    """Получить детали конкретной заметки."""
    url = f'https://p140-ckdatabasews.icloud.com/database/1/com.apple.notes/production/shared/records/lookup?dsid={dsid}'
    payload = {
        "records": [{"recordName": record_name}],
        "zoneID": {
            "zoneName": zone_id,
            "ownerRecordName": owner_record_name
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    
    logger.debug(f"Note Details Response Status Code: {response.status_code}")
    # logger.debug(f"Note Details Response Content: {response.text}")
    with open(f'logs/note_details_logs.json', 'w', encoding='utf-8') as file:
        json.dump(response.json(), file, ensure_ascii=False, indent=4)
    
    if response.status_code == 200:
        return response.json().get('records', [])
    else:
        response.raise_for_status()


def process_record(record, zone_id, owner_record_name, dsid, headers):
    fields = record['fields']
    
    title = base64.b64decode(fields['TitleEncrypted']['value']).decode('utf-8')
    
    text = decrypt_note_text(fields['TextDataEncrypted']['value'])
    
    # Получение информации о папке
    folder = fields['Folders']['value'][0]
    folder_id = folder['recordName']
    owner_id = folder['zoneID']['ownerRecordName']
    
    folder_name = get_folder_name(folder_id, zone_id, owner_record_name, dsid, headers)
    
    # Формирование результата
    processed_note = {
        'title': title,
        'text': text,
        'record_id': record['recordName'],
        'created_date': record['created']['timestamp'],
        'last_edited_date': record['modified']['timestamp'],
        'folder_id': folder_id,
        'folder_name': folder_name, 
        'owner_id': owner_id
    }
    
    return processed_note


def get_notes_list(api, synced_notes_edited_dates={}):
    try:
        headers, params = setup_headers(api)
        
        # Получение списка зон (shared папок)
        zones = get_zones(params['dsid'], headers)
        all_notes = []

        for zone in zones:
            zone_id = zone['zoneID']['zoneName']
            owner_record_name = zone['zoneID']['ownerRecordName']
            
            # Получение заметок из зоны
            notes = get_zone_changes(zone_id, owner_record_name, params['dsid'], headers)
            
            for note in notes:
                note_record_name = note['recordName']
                modification_date = note['fields']['ModificationDate']['value']
                
                # Проверяем, нужно ли обновлять эту заметку
                if note_record_name not in synced_notes_edited_dates or modification_date > synced_notes_edited_dates[note_record_name]:
                    note_details = get_note_details(note_record_name, zone_id, owner_record_name, params['dsid'], headers)
                    
                    for record in note_details:
                        processed_note = process_record(record, zone_id, owner_record_name, params['dsid'], headers)
                        all_notes.append(processed_note)
        
        return all_notes

    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to retrieve notes: {e}")
        return []