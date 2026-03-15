import os
import requests
import streamlit as st
from dotenv import load_dotenv
from groq import Groq
# ── 1. Load environment variables ──────────────────────────
load_dotenv()  # reads .env if present


# ──2. Fetch the Available Models from Groq API ──────────────────────────

def get_groq_models(api_key):
    url = "https://api.groq.com/openai/v1/models"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    available_models = []
    for i in response.json().get("data", []):
        available_models.append(i['id'])
    return available_models

# ── 3. Page configuration ───────────────────────────────────
st.set_page_config(
    page_title="AI Chatbot using Groq API and Streamlit",
    page_icon="🤖",
    layout="centered",
)

# ── 4. App title & description ──────────────────────────────
st.title("🤖 AI Chatbot using Groq API and Streamlit")
st.caption("Powered by Groq LLMs.Built with Streamlit.")

if "messages" not in st.session_state:
    st.session_state.messages = []
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
# ── 5. Sidebar – configuration ──────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")

    # API key: prefer .env → fallback to user input
    api_key_default = os.getenv("GROQ_API_KEY", "")
    api_key = st.text_input(
        "Groq API Key",
        value=api_key_default,
        type="password",
        placeholder="gsk_...",
        help="Get your free key at https://console.groq.com",
    )

     # Model selection — fetched live from Groq API
    available_models = get_groq_models(api_key)
    model = st.selectbox(
        "Model",
        options=available_models,
        help=f"{len(available_models)} models available from Groq API.",
    )

    # System prompt
    system_prompt = st.text_area(
        "System Prompt",
        value="You are a helpful, concise, and friendly AI assistant.",
        height=100,
        help="Sets the assistant's personality / role.",
    )

    # Temperature
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.05,
                            help="Higher = more creative; lower = more focused.")
    
user_input = st.chat_input("Ask me a question")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    client = Groq(api_key=api_key)

    chat_completion = client.chat.completions.create(
        messages=st.session_state.messages,
        model=model,
        temperature=temperature,
    )

    response = chat_completion.choices[0].message.content
    st.markdown(f"**Response:** {response}")
    st.session_state.messages.append({"role": "assistant", "content": response})
        
        



