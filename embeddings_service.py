import os
import tiktoken
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def format_timestamp(timestamp):
    """Convert timestamp to a readable date format."""
    return datetime.fromtimestamp(timestamp / 1000).strftime('%d %B %Y, %H:%M')

def num_tokens_from_string(string: str, encoding_name: str = "cl100k_base") -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def truncate_text(text: str, max_tokens: int, encoding_name: str = "cl100k_base") -> str:
    """
    Truncate the text to the maximum number of tokens.
    """
    encoding = tiktoken.get_encoding(encoding_name) 
    tokens = encoding.encode(text)
    
    if len(tokens) > max_tokens:
        tokens = tokens[:max_tokens]
    
    return encoding.decode(tokens)

def create_chunks(note, max_tokens=8192):
    """
    Create chunks from a note, ensuring each chunk starts with note metadata.
    
    :param note: A dictionary containing note data
    :param max_tokens: Maximum number of tokens per chunk
    :return: A list of text chunks
    """
    metadata = f"Folder: {note['folder_name']}\n"
    metadata += f"Creation Date: {format_timestamp(note['created_date'])}\n"
    metadata_tokens = num_tokens_from_string(metadata)
    
    text = note['text']
    lines = text.split('\n')
    
    chunks = []
    current_chunk = metadata
    current_tokens = metadata_tokens

    for line in lines:
        line_tokens = num_tokens_from_string(line + '\n')
        if current_tokens + line_tokens > max_tokens:
            chunks.append(current_chunk.strip())
            current_chunk = metadata + line + '\n'
            current_tokens = metadata_tokens + line_tokens
        else:
            current_chunk += line + '\n'
            current_tokens += line_tokens

    if current_chunk.strip() != metadata.strip():
        chunks.append(current_chunk.strip())

    return chunks

def create_embedding(text, model="text-embedding-3-large"):
    """Create an embedding using the OpenAI API."""
    try:
        response = client.embeddings.create(
            model=model,
            input=text,
            encoding_format="float",
            dimensions=3072
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"An error occurred while creating the embedding: {e}")
        return None

def process_note(note):
    """
    Process a note: create chunks if necessary and generate embeddings.
    
    :param note: A dictionary containing note data
    :return: A list of tuples (chunk, embedding)
    """
    chunks = create_chunks(note)
    results = []
    
    for chunk in chunks:
        embeddings = create_embedding(chunk)
        results.append((chunk, embeddings))
        
    return results

# Example usage
if __name__ == "__main__":
    test_note = {
        "folder_name": "Personal",
        "created_date": 1718347207097,
        "text": "This is a test note.\nIt has multiple lines.\nSome of them are short.\n" * 1000  # Make it long enough to be split
    }
    
    processed_results = process_note(test_note)
    
    for i, (chunk, embeddings) in enumerate(processed_results):
        print(f"Chunk {i + 1}:")
        print(chunk[:100] + "...")  # Print first 100 characters of the chunk
        print(f"Embedding: {embeddings[:5]}... (total length: {len(embeddings)})")
        print("-" * 50)