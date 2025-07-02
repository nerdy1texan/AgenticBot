import streamlit as st
import os
import base64
from io import BytesIO
from dotenv import load_dotenv
from chatgpt_agentic_clone.agent import web_search, scrape_webpage, deep_research, generate_image, setup_gemini
import google.generativeai as genai
import sys

# --- Setup ---
load_dotenv()
setup_gemini()
model = genai.GenerativeModel('gemini-2.0-flash-exp')

print("PYTHON EXECUTABLE:", sys.executable)

st.set_page_config(page_title="AgenticBot Chat", page_icon="🤖", layout="wide", initial_sidebar_state="expanded")

# --- Custom CSS for modern, readable dark mode ---
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
    <style>
    html, body, .stApp {
        background: linear-gradient(135deg, #232526 0%, #2c2f34 100%) !important;
        font-family: 'Inter', sans-serif !important;
    }
    .block-container {
        padding-top: 2rem;
        max-width: 900px;
        margin: 0 auto;
    }
    .main-chat-card {
        background: #23272f;
        border-radius: 18px;
        box-shadow: 0 4px 32px #0005;
        padding: 2.2rem 2.2rem 1.2rem 2.2rem;
        margin-bottom: 2.5rem;
    }
    .sidebar-content {padding-top: 1rem;}
    .sidebar-logo {display: flex; align-items: center; justify-content: center; margin-bottom: 1.5rem;}
    .sidebar-logo img {border-radius: 50%; width: 60px; height: 60px; margin-right: 0.5rem;}
    .sidebar-title {font-size: 1.5rem; font-weight: bold; margin-bottom: 0.5rem;}
    .sidebar-section {margin-bottom: 1.5rem;}
    .sidebar-divider {border-top: 1px solid #444; margin: 1rem 0;}
    .stChatMessage.user {
        background: #181c22;
        color: #fff;
        border-radius: 16px;
        margin-bottom: 0.7rem;
        box-shadow: 0 2px 8px #0002;
        font-size: 1.13rem;
        padding: 0.85rem 1.1rem;
    }
    .stChatMessage.assistant {
        background: #f5f7fa;
        color: #232526;
        border-radius: 16px;
        margin-bottom: 0.7rem;
        box-shadow: 0 2px 8px #0002;
        font-size: 1.13rem;
        padding: 0.85rem 1.1rem;
    }
    .stMarkdown {font-size: 1.13rem;}
    .stButton>button {background: #673ab7; color: white; border-radius: 8px;}
    .stTextInput>div>input {
        border-radius: 16px !important;
        font-size: 1.1rem;
        padding: 0.7rem 1.2rem;
        box-shadow: 0 2px 8px #0001;
        border: 1.5px solid #6a82fb;
        background: #23272f;
        color: #fff;
    }
    .stTextInput>div>input::placeholder {
        color: #bdbdbd;
        opacity: 1;
    }
    .st-emotion-cache-1kyxreq {background: transparent !important;}
    .stApp footer {display: none;}
    .custom-footer {
        position: fixed;
        left: 0; right: 0; bottom: 0;
        width: 100%;
        background: #181c22;
        color: #bdbdbd;
        text-align: center;
        font-size: 1rem;
        padding: 0.5rem 0 0.3rem 0;
        z-index: 100;
        letter-spacing: 0.03em;
        box-shadow: 0 -2px 12px #0002;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Session State ---
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'tool_trace' not in st.session_state:
    st.session_state.tool_trace = []
if 'chat' not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# --- Sidebar ---
st.sidebar.markdown('<div class="sidebar-logo"><img src="https://cdn-icons-png.flaticon.com/512/4712/4712035.png" alt="Bot Logo"><span class="sidebar-title">AgenticBot</span></div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="sidebar-section"><b>Capabilities:</b><br><span style="color:#e573c7;">●</span> General Q&A<br><span style="color:#64b5f6;">●</span> Web search<br><span style="color:#81c784;">●</span> Web scraping<br><span style="color:#ffd54f;">●</span> Deep research<br><span style="color:#ff8a65;">●</span> Image generation</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="sidebar-section"><b>Special commands:</b><br><span style="color:#81c784;">•</span> <code>search for [query]</code><br><span style="color:#ffd54f;">•</span> <code>scrape [url]</code><br><span style="color:#64b5f6;">•</span> <code>research [topic]</code><br><span style="color:#ff8a65;">•</span> <code>generate image [description]</code></div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
st.sidebar.markdown('<div style="text-align:center; margin-top:2rem;"><a href="https://github.com/nerdy1texan/AgenticBot.git" target="_blank" style="color:#90caf9; text-decoration:none; font-weight:bold; font-size:1.1rem;">🌐 View on GitHub</a></div>', unsafe_allow_html=True)

# --- Main Panel ---
st.markdown("""
<div class="main-chat-card">
    <div style="display:flex; align-items:center; gap:1rem;">
        <span style="font-size:2.5rem;">🤖</span>
        <span style="font-size:2.2rem; font-weight:bold; color:#fff; letter-spacing:0.01em;">AgenticBot Chat</span>
    </div>
    <div style="font-size:1.15rem; margin-bottom:1.5rem; color:#eee;">
    Welcome to <b>AgenticBot</b>! Ask anything, or try special commands for web search, scraping, research, or image generation.
    </div>
""", unsafe_allow_html=True)

# --- Chat Display ---
for entry in st.session_state.chat_history:
    if entry['role'] == 'user':
        st.chat_message("user").markdown(f"<span style='color:#90caf9; font-weight:bold;'>🧑‍💻 You:</span> {entry['content']}", unsafe_allow_html=True)
    elif entry['role'] == 'assistant':
        st.chat_message("assistant").markdown(f"<span style='color:#388e3c; font-weight:bold;'>🤖 AgenticBot:</span> {entry['content']}", unsafe_allow_html=True)
        # Show image if present
        if entry.get('image_data'):
            try:
                image_bytes = base64.b64decode(entry['image_data'])
                st.image(BytesIO(image_bytes), caption="Generated Image", use_column_width=True)
            except Exception:
                st.warning("[Image could not be displayed]")

# --- Tool Trace Display ---
if st.session_state.tool_trace:
    with st.expander("🔧 Tool/Action Trace", expanded=False):
        for trace in st.session_state.tool_trace[-5:]:
            st.markdown(trace)

# --- User Input ---
st.markdown("</div>", unsafe_allow_html=True)  # Close main-chat-card
user_input = st.chat_input("Type your message and press Enter...")

if user_input:
    st.session_state.chat_history.append({'role': 'user', 'content': user_input})
    response_text = ""
    image_data = None
    tool_trace = None

    try:
        # Tool detection
        if user_input.lower().startswith("search for"):
            query = user_input[11:]
            tool_trace = f"🔍 Web search for: {query}"
            result = web_search(query)
            if result["status"] == "success":
                response_text = f"Search results for '{query}':<br><br>"
                for i, item in enumerate(result["results"][:5], 1):
                    response_text += f"{i}. <b>{item['title']}</b><br>🔗 <a href='{item['url']}' target='_blank'>{item['url']}</a><br>{item['description'][:100]}...<br><br>"
            else:
                response_text = f"Search failed: {result['error_message']}"
        elif user_input.lower().startswith("scrape "):
            url = user_input[7:]
            tool_trace = f"🕸️ Scraping: {url}"
            result = scrape_webpage(url)
            if result["status"] == "success":
                content = result["content"][:500] + "..." if len(result["content"]) > 500 else result["content"]
                response_text = f"Content from <b>{url}</b>:<br><br>{content}"
            else:
                response_text = f"Scraping failed: {result['error_message']}"
        elif user_input.lower().startswith("research "):
            topic = user_input[9:]
            tool_trace = f"🔬 Researching: {topic}"
            result = deep_research(topic)
            if result["status"] == "success":
                response_text = f"Research on '<b>{topic}</b>':<br><br>{result['summary']}<br><br>Sources: {result['total_sources']}"
            else:
                response_text = f"Research failed: {result['error_message']}"
        elif user_input.lower().startswith("generate image"):
            prompt = user_input[15:]
            tool_trace = f"🎨 Generating image: {prompt}"
            result = generate_image(prompt)
            if result["status"] == "success" and result.get("image_data"):
                response_text = f"Image generated successfully! Prompt: <b>{prompt}</b>"
                image_data = result.get("image_data")
            else:
                response_text = f"Image generation failed: {result.get('error_message', 'Unknown error')}"
        elif any(word in user_input.lower() for word in ["weather", "current", "latest", "news", "today's", "now"]):
            tool_trace = f"🔍 Detected current info request, searching for: {user_input}"
            result = web_search(user_input)
            if result["status"] == "success":
                response_text = f"Current information for '<b>{user_input}</b>':<br><br>"
                for i, item in enumerate(result["results"][:3], 1):
                    response_text += f"{i}. <b>{item['title']}</b><br>🔗 <a href='{item['url']}' target='_blank'>{item['url']}</a><br>{item['description'][:150]}...<br><br>"
            else:
                response_text = f"Search failed: {result['error_message']}"
        else:
            # Regular chat
            response = st.session_state.chat.send_message(user_input)
            response_text = response.text
    except Exception as e:
        response_text = f"❌ Error: {e}"

    # Save tool trace
    if tool_trace:
        st.session_state.tool_trace.append(tool_trace)

    # Save assistant response
    st.session_state.chat_history.append({
        'role': 'assistant',
        'content': response_text,
        'image_data': image_data
    })

    st.experimental_rerun()

# --- Footer ---
st.markdown('<div class="custom-footer">✨ AgenticBot &copy; 2025 &mdash; <a href="https://github.com/nerdy1texan/AgenticBot.git" style="color:#90caf9; text-decoration:none;">GitHub</a> | Built with Google ADK, Firecrawl, and Streamlit</div>', unsafe_allow_html=True) 