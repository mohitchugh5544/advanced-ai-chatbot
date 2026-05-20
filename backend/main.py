from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai
from .database import query_vector_db, add_document_to_vector_db

app = FastAPI(title="Advanced RAG Chatbot API Engine")
client = genai.Client()

class ChatRequest(BaseModel):
    message: str

class DocumentRequest(BaseModel):
    doc_id: str
    text: str

@app.post("/index-text")
async def index_text(payload: DocumentRequest):
    """Endpoint to inject custom knowledge into the vector database."""
    try:
        add_document_to_vector_db(payload.doc_id, payload.text)
        return {"status": "success", "message": f"Document '{payload.doc_id}' successfully indexed."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat_endpoint(payload: ChatRequest):
    """Advanced RAG endpoint: Retrieves context, injects into prompt, and generates answer."""
    try:
        user_message = payload.message
        
        # 1. Retrieve matching knowledge from ChromaDB
        retrieved_contexts = query_vector_db(user_message, num_results=2)
        context_str = "\n".join(retrieved_contexts) if retrieved_contexts else "No specific context found."

        # 2. Construct a secure system prompt restricting hallucination
        system_instruction = (
            "You are an advanced context-aware assistant. Use the following retrieved data pieces "
            "to answer the user's query accurately. If the answer cannot be verified from the context, "
            "politely state that you do not possess that internal data.\n\n"
            f"Retrieved Context:\n{context_str}"
        )

        # 3. Request synthesis from the core LLM
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_message,
            config={'system_instruction': system_instruction}
        )
        
        return {
            "response": response.text,
            "context_used": retrieved_contexts
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))