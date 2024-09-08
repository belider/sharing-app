from notes_reader import authenticate_icloud, get_notes_list
from db_service import DatabaseService
from embeddings_service import process_note
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    # Инициализация менеджера базы данных
    db_service = DatabaseService()
    
    # Попытка загрузки существующей сессии
    logger.info("Attempting to load existing session")
    api = db_service.load_session()
    
    if api:
        logger.info("Existing session loaded, validating...")
        try:
            # Проверяем, действительна ли сессия
            api.authenticate()
            # Дополнительная проверка: попытка получить список устройств
            devices = api.devices
            if not devices:
                raise Exception("Failed to retrieve devices list")
            logger.info("Existing session is valid")
        except Exception as e:
            logger.warning(f"Existing session is invalid: {str(e)}")
            api = None

    if not api:
        logger.info("Attempting to authenticate with iCloud")
        api = authenticate_icloud()
        if api:
            logger.info("Authentication successful")
            logger.info("Attempting to save new session")
            if db_service.save_session(api):
                logger.info("New session saved successfully")
            else:
                logger.warning("Failed to save new session")
        else:
            logger.error("Authentication failed")
            return
    
    # api = authenticate_icloud()
    # if not api:
    #     print("Failed to authenticate with iCloud")
    #     return
    
    try:
        # Получаем последние даты редактирования из базы данных
        synced_notes_edited_dates = db_service.get_last_edited_dates()
        
        # Передаем last_edited_dates в get_notes_list
        notes = get_notes_list(api, synced_notes_edited_dates)
        logger.info(f"Retrieved {len(notes)} updated notes from iCloud")

        for note in notes:
            chunks = process_note(note)
            
            for i, (chunk_text, embeddings) in enumerate(chunks):
                chunk_data = {
                    "title": f"{note['title']} - {i+1}" if len(chunks) > 1 else note['title'],
                    "text": chunk_text,
                    "embeddings": embeddings,
                    "record_id": f"{note['record_id']}-{i}" if len(chunks) > 1 else note['record_id'],
                    "created_date": note['created_date'],
                    "last_edited_date": note['last_edited_date'],
                    "folder_id": note['folder_id'],
                    "folder_name": note['folder_name'],
                    "owner_id": note['owner_id']
                }
                
                db_service.insert_or_update(chunk_data)
                logger.info(f"Saved chunk {i+1} for note: {note['title']}")

        logger.info("Synchronization completed successfully")

    except Exception as e:
        logger.error(f"An error occurred during synchronization: {e}")
    finally:
        # Сохраняем обновленную сессию после каждого успешного запуска
        # if api and api.is_trusted_session:
        #     if db_service.save_session(api):
        #         logger.info("Session saved successfully after synchronization")
        #     else:
        #         logger.warning("Failed to save session after synchronization")
        db_service.close_connection()


if __name__ == "__main__":
    main()