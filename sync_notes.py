from notes_reader import authenticate_icloud, get_notes_list, accept_shared_folder
from db_service import DatabaseService
from embeddings_service import process_note
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def sync_notes(db_service):
    # Попытка загрузки существующей сессии
    logger.info("Attempting to load existing session")
    
    api = authenticate_icloud()
    
    if api:
        logger.info("Authentication successful")
        logger.info("Attempting to save new session")
    else:
        logger.error("Authentication failed")
        return
    
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

def accept_invite(db_service, short_guid):
    logger.info(f"Attempting to accept invite for shared folder with shortGUID: {short_guid}")
    
    # Попытка загрузки существующей сессии
    api = authenticate_icloud()
    
    if api:
        logger.info("Authentication successful")
        result = accept_shared_folder(api, short_guid)
        if result:
            logger.info(f"Successfully accepted shared folder with shortGUID: {short_guid}")
            # Здесь можно добавить дополнительную логику, например, немедленную синхронизацию новой папки
            sync_notes(db_service)
        else:
            logger.error(f"Failed to accept shared folder with shortGUID: {short_guid}")
    else:
        logger.error("Authentication failed, unable to accept invite")