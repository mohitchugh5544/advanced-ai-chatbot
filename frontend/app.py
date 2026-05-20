import streamlit as st
import requests

# Page configurations
st.set_page_config(page_title="Advanced RAG Assistant", page_icon="🤖", layout="centered")
st.title("🤖 Advanced RAG Chatbot")
st.caption("Powered by FastAPI, ChromaDB, and Gemini 2.5")

# Define the backend URL matching your FastAPI server port
BACKEND_URL = "http://127.0.0.1:8000"

# Initialize conversation history session state so it doesn't clear on refresh
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar for indexing new knowledge chunks on the fly
with st.sidebar:
    st.header("Document Knowledge Base")
    st.write("Inject unique facts into the Vector Database:")
    
    doc_id = st.text_input("Document ID / Title", placeholder="e.g., campus_policy")
    doc_text = st.text_area("Document Content", placeholder="Paste reference text here...")
    
    if st.button("Index Data Chunk", use_container_width=True):
        if doc_id and doc_text:
            with st.spinner("Embedding and indexing..."):
                try:
                    payload = {"doc_id": doc_id, "text": doc_text}
                    res = requests.post(f"{BACKEND_URL}/index-text", json=payload)
                    if res.status_code == 200:
                        st.sidebar.success(f"Successfully indexed: {doc_id}")
                    else:
                        st.sidebar.error(f"Error: {res.json().get('detail')}")
                except Exception as e:
                    st.sidebar.error(f"Could not connect to backend: {e}")
        else:
            st.sidebar.warning("Please fill out both fields.")

# Render existing conversation history from session state
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Prompt input for the user
if user_input := st.chat_input("Ask something about your indexed documents..."):
    
    # 1. Display user message instantly in the UI
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # 2. Query backend API and render response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        with st.spinner("Searching knowledge base and generating answer..."):
            try:
                payload = {"message": user_input}
                res = requests.post(f"{BACKEND_URL}/chat", json=payload)
                
                if res.status_code == 200:
                    api_data = res.json()
                    bot_response = api_data.get("response")
                    contexts = api_data.get("context_used", [])
                    
                    # Display the final synthesized answer
                    response_placeholder.markdown(bot_response)
                    
                    # If relevant context was retrieved, display it inside an expander drawer
                    if contexts:
                        with st.expander("🔍 View Retrieved Database Context"):
                            for ctx in contexts:
                                st.info(f"... {ctx} ...")
                                
                    # Save assistant response to memory state
                    st.session_state.messages.append({"role": "assistant", "content": bot_response})
                    
                else:
                    response_placeholder.error(f"API Error: {res.json().get('detail')}")
            except Exception as e:
                response_placeholder.error(f"Failed to reach FastAPI backend server. Ensure it's running. Error: {e}")