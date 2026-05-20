import chromadb
from google import genai
import os

# Initialize the Gemini Client (Make sure GEMINI_API_KEY is set in your environment)
# You can set it via terminal: export GEMINI_API_KEY="your_key"
client = genai.Client()

# Initialize a persistent local vector database inside a folder named 'chroma_storage'
chroma_client = chromadb.PersistentClient(path="./chroma_storage")
collection = chroma_client.get_or_create_collection(name="project_knowledge")

def get_embedding(text: str):
    """Generates a vector embedding for a given text chunk using Gemini."""
    response = client.models.embed_content(
        model="gemini-embedding-2",
        contents=text
    )
    # Extract the vector list from the response object
    return response.embeddings[0].values

def add_document_to_vector_db(doc_id: str, text: str):
    """Embeds a document chunk and stores it in ChromaDB."""
    vector = get_embedding(text)
    collection.add(
        ids=[doc_id],
        embeddings=[vector],
        documents=[text]
    )
    print(f"Successfully indexed chunk: {doc_id}")

def query_vector_db(user_query: str, num_results: int = 2):
    """Searches the database for chunks matching the user's intent."""
    query_vector = get_embedding(user_query)
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=num_results
    )
    # Return the raw text of the matching documents
    return results['documents'][0] if results['documents'] else []