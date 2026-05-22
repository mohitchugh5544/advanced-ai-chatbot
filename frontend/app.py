import streamlit as st
import requests

# Page configurations
st.set_page_config(page_title="Advanced RAG Assistant", page_icon="🤖", layout="centered")

# Custom CSS styling for advanced premium dark theme and animations
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Space+Grotesk:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

/* Global resets & radial-mesh background */
html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    background: radial-gradient(circle at 50% -25%, #1d1e34 0%, #08090f 75%) !important;
    color: #e2e8f0 !important;
}

/* Hide Streamlit default UI branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header[data-testid="stHeader"] {
    background-color: transparent !important;
}

/* Custom modern animated title */
.main-title-container {
    text-align: center;
    padding: 1.5rem 0 2rem 0;
}
.main-title {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 2.8rem;
    background: linear-gradient(45deg, #a855f7, #6366f1, #06b6d4, #a855f7);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: textShine 6s linear infinite;
    margin-bottom: 0.8rem;
    filter: drop-shadow(0 2px 15px rgba(99, 102, 241, 0.25));
}
@keyframes textShine {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
.main-subtitle {
    font-family: 'Outfit', sans-serif;
    font-weight: 400;
    font-size: 1.05rem;
    color: #94a3b8;
    letter-spacing: 0.02em;
    line-height: 1.5;
}
.tech-badge {
    display: inline-block;
    background: rgba(99, 102, 241, 0.12);
    border: 1px solid rgba(99, 102, 241, 0.25);
    color: #a5b4fc;
    padding: 4px 12px;
    border-radius: 9999px;
    font-size: 0.78rem;
    font-weight: 600;
    margin: 4px;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    box-shadow: 0 0 10px rgba(99, 102, 241, 0.1);
}

/* Sidebar glassmorphic container and metallic accent */
[data-testid="stSidebar"] {
    background: rgba(10, 11, 18, 0.88) !important;
    backdrop-filter: blur(20px) saturate(180%);
    border-right: 1px solid rgba(99, 102, 241, 0.15) !important;
    box-shadow: 4px 0 24px rgba(0, 0, 0, 0.4);
}
[data-testid="stSidebar"] > div:first-child {
    background: transparent !important;
}

/* Custom headers in sidebar */
.sidebar-header {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 600;
    font-size: 1.25rem;
    color: #f1f5f9;
    margin-top: 1.5rem;
    margin-bottom: 0.5rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    padding-bottom: 0.5rem;
    letter-spacing: 0.02em;
}
.sidebar-desc {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 0.88rem;
    color: #94a3b8;
    line-height: 1.4;
    margin-bottom: 1.2rem;
}

/* Premium Inputs Overrides */
div[data-testid="stTextInput"] input, div[data-testid="stTextArea"] textarea {
    background-color: rgba(15, 23, 42, 0.6) !important;
    color: #f8fafc !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 12px !important;
    padding: 12px 16px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.92rem !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.2) !important;
}
div[data-testid="stTextInput"] input:focus, div[data-testid="stTextArea"] textarea:focus {
    border-color: #818cf8 !important;
    box-shadow: 0 0 12px rgba(129, 140, 248, 0.35), inset 0 2px 4px rgba(0, 0, 0, 0.2) !important;
    background-color: rgba(15, 23, 42, 0.85) !important;
    outline: none !important;
}

/* Sidebar button styling with gradient glow and transitions */
div.stButton > button {
    background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
    color: #ffffff !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 12px 24px !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 4px 14px rgba(99, 102, 241, 0.3) !important;
    letter-spacing: 0.05em;
    font-size: 0.9rem;
    width: 100%;
}
div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(99, 102, 241, 0.55) !important;
    background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%) !important;
}
div.stButton > button:active {
    transform: translateY(1px);
}

/* Chat bubble styling with soft shadows and hover elevations */
[data-testid="stChatMessage"] {
    background: rgba(22, 28, 45, 0.4) !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    border-radius: 16px !important;
    padding: 1.25rem 1.5rem !important;
    margin-bottom: 1.25rem !important;
    backdrop-filter: blur(12px) !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}
[data-testid="stChatMessage"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 25px rgba(99, 102, 241, 0.12) !important;
    border-color: rgba(99, 102, 241, 0.2) !important;
}

/* User vs Assistant specific chat bubble styles */
div[data-testid="stChatMessage"][data-test-role="user"] {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(99, 102, 241, 0.03) 100%) !important;
    border: 1px solid rgba(99, 102, 241, 0.2) !important;
    margin-left: 2rem !important;
}
div[data-testid="stChatMessage"][data-test-role="assistant"] {
    background: linear-gradient(135deg, rgba(168, 85, 247, 0.08) 0%, rgba(168, 85, 247, 0.02) 100%) !important;
    border: 1px solid rgba(168, 85, 247, 0.2) !important;
    margin-right: 2rem !important;
}

/* Avatar glows */
[data-testid="chatAvatarIcon-user"], [data-testid="stChatMessage"] [data-testid="chatAvatarIcon-user"] {
    background-color: #6366f1 !important;
    box-shadow: 0 0 12px rgba(99, 102, 241, 0.5) !important;
}
[data-testid="chatAvatarIcon-assistant"], [data-testid="stChatMessage"] [data-testid="chatAvatarIcon-assistant"] {
    background-color: #a855f7 !important;
    box-shadow: 0 0 12px rgba(168, 85, 247, 0.5) !important;
}

/* Bottom Chat Input box */
div[data-testid="stChatInput"] {
    border: 1px solid rgba(99, 102, 241, 0.18) !important;
    border-radius: 20px !important;
    background-color: rgba(15, 23, 42, 0.85) !important;
    backdrop-filter: blur(16px) !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35) !important;
    padding: 6px !important;
    transition: all 0.3s ease !important;
}
div[data-testid="stChatInput"]:focus-within {
    border-color: rgba(168, 85, 247, 0.45) !important;
    box-shadow: 0 0 20px rgba(168, 85, 247, 0.2) !important;
}
div[data-testid="stChatInput"] textarea {
    color: #f8fafc !important;
    background-color: transparent !important;
    font-size: 0.95rem !important;
}

/* Expander custom design */
[data-testid="stExpander"] {
    background-color: rgba(15, 23, 42, 0.25) !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1) !important;
    backdrop-filter: blur(8px) !important;
}
[data-testid="stExpander"] details {
    border: none !important;
}
[data-testid="stExpander"] summary {
    color: #a5b4fc !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 500 !important;
    padding: 10px 14px !important;
}
[data-testid="stExpander"] summary:hover {
    color: #c7d2fe !important;
}

/* Info dialogs/containers */
div.stInfo {
    background-color: rgba(30, 41, 59, 0.4) !important;
    border: 1px solid rgba(99, 102, 241, 0.15) !important;
    border-radius: 12px !important;
    color: #cbd5e1 !important;
    font-size: 0.9rem !important;
}

/* Smooth customized scrollbars */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
::-webkit-scrollbar-track {
    background: rgba(15, 23, 42, 0.1);
}
::-webkit-scrollbar-thumb {
    background: rgba(99, 102, 241, 0.2);
    border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
    background: rgba(99, 102, 241, 0.4);
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Glowing customized header title
st.markdown(
    """
    <div class="main-title-container">
        <div class="main-title">🤖 Advanced RAG Assistant</div>
        <div class="main-subtitle">
            Inject, query, and synthesize internal knowledge bases with ultimate precision.
            <div style="margin-top: 10px;">
                <span class="tech-badge">FastAPI</span>
                <span class="tech-badge">ChromaDB</span>
                <span class="tech-badge">Gemini 2.5</span>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Define the backend URL matching your FastAPI server port
BACKEND_URL = "http://127.0.0.1:8000"

# Initialize conversation history session state so it doesn't clear on refresh
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar for indexing new knowledge chunks on the fly
with st.sidebar:
    st.markdown('<div class="sidebar-header">Knowledge Base</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-desc">Inject unique reference facts dynamically into Chroma Vector Database.</div>', unsafe_allow_html=True)
    
    doc_id = st.text_input("Document ID / Title", placeholder="e.g., campus_policy")
    doc_text = st.text_area("Document Content", placeholder="Paste reference text here...", height=150)
    
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