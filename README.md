> **⚠️ Experimental Project:**  
> This Apple Notes GPT Assistant was hacked together over a couple of weekends. It uses a reverse-engineered API to access iCloud Notes and integrate them with GPTs for personalized responses. If you're interested in contributing, feel free to reach out on [Twitter](https://x.com/LiderAlexandr)!

# Apple Notes GPT Assistant

This project integrates GPT with Apple Notes, enabling responses that draw directly from shared folders and notes in your iCloud. By sharing content with a designated account (`sharing.app@icloud.com`), this assistant reads and responds to your queries based on your notes. 

## Project Overview

The app uses `flask-apscheduler` for continuous sync with iCloud Notes, with key components divided as follows:

- **Authentication & Sync** (`notes_reader.py`, `sync_notes.py`): Authenticates iCloud sessions (supports 2FA) and syncs new or edited notes every two minutes. Handles shared folders via the `/accept_shared_folder` API endpoint.
  
- **Database and Embeddings** (`db_service.py`, `embeddings_service.py`): Decrypts and chunks notes for vector search, using embeddings to make note content easily searchable.

- **Server & API** (`server.py`): Provides endpoints for GPT to query notes:
  - **`/search`**: Finds relevant notes using embeddings.
  - **`/accept_shared_folder`**: Processes shared folders to add them to the sync.

## Key Endpoints

- **`/search`**: Searches for relevant notes.
- **`/accept_shared_folder`**: Adds shared folders for syncing.

## Deployment

1. **Setup**: Configure environment variables (iCloud credentials, API keys) in `.env`.
2. **Run**:
   - Start `sync_notes.py` to handle iCloud note synchronization.
   - Start `server.py` to provide the API for querying notes.

This setup combines GPT with Apple Notes for a novel, personal assistant experience. Your contributions are welcome to help expand and refine it!
