from notes_reader import authenticate_icloud, get_notes_list
from db_service import DatabaseService
from embeddings_service import process_note
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    api = authenticate_icloud()
    if not api:
        print("Failed to authenticate with iCloud")
        return

    # Инициализация менеджера базы данных
    db_service = DatabaseService()
    
    notes = get_notes_list(api)
    logger.info(f"Retrieved {len(notes)} notes from iCloud")

    # Обработка каждой заметки
    for note in notes:
        logger.info(f"Processing note: {note['title']}")
        
        # Создание чанков и эмбеддингов
        chunks = process_note(note)
        
        # Сохранение каждого чанка в базу данных
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

    logger.info("All notes processed and saved to database")

if __name__ == "__main__":
    main()