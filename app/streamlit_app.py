import streamlit as st
import os
from dotenv import load_dotenv
from chatgpt_agentic_clone.agent import web_search, scrape_webpage, deep_research, generate_image, setup_gemini
import google.generativeai as genai
import sys

# --- Setup ---
load_dotenv()
setup_gemini()
model = genai.GenerativeModel('gemini-2.0-flash-exp')

print("PYTHON EXECUTABLE:", sys.executable)

st.set_page_config(page_title="AgenticBot Chat", page_icon="🤖", layout="centered")

# --- Session State ---
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'tool_trace' not in st.session_state:
    st.session_state.tool_trace = []
if 'chat' not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# --- Sidebar ---
st.sidebar.title("🤖 AgenticBot")
st.sidebar.markdown("""
**Capabilities:**
- General Q&A
- Web search (e.g. `search for latest AI news`)
- Web scraping (e.g. `scrape https://github.com/trending`)
- Deep research (e.g. `research quantum computing`)
- Image generation (e.g. `generate image of a robot`)

**Special commands:**
- `search for [query]`
- `scrape [url]`
- `research [topic]`
- `generate image [description]`

---
[View on GitHub](https://github.com/your-repo)
""")

# --- Main Panel ---
st.title("🤖 AgenticBot Chat")
st.markdown("""
Welcome to **AgenticBot**! Ask anything, or try special commands for web search, scraping, research, or image generation.
""")

# --- Chat Display ---
for entry in st.session_state.chat_history:
    if entry['role'] == 'user':
        st.chat_message("user").markdown(entry['content'])
    elif entry['role'] == 'assistant':
        st.chat_message("assistant").markdown(entry['content'])
        if entry.get('image_url'):
            st.image(entry['image_url'], caption="Generated Image", use_column_width=True)

# --- Tool Trace Display ---
if st.session_state.tool_trace:
    with st.expander("🔧 Tool/Action Trace", expanded=False):
        for trace in st.session_state.tool_trace[-5:]:
            st.markdown(trace)

# --- User Input ---
user_input = st.chat_input("Type your message and press Enter...")

if user_input:
    st.session_state.chat_history.append({'role': 'user', 'content': user_input})
    response_text = ""
    image_url = None
    tool_trace = None

    try:
        # Tool detection
        if user_input.lower().startswith("search for"):
            query = user_input[11:]
            tool_trace = f"🔍 Web search for: {query}"
            result = web_search(query)
            if result["status"] == "success":
                response_text = f"Search results for '{query}':\n\n"
                for i, item in enumerate(result["results"][:5], 1):
                    response_text += f"{i}. {item['title']}\n   URL: {item['url']}\n   {item['description'][:100]}...\n\n"
            else:
                response_text = f"Search failed: {result['error_message']}"
        elif user_input.lower().startswith("scrape "):
            url = user_input[7:]
            tool_trace = f"🕸️ Scraping: {url}"
            result = scrape_webpage(url)
            if result["status"] == "success":
                content = result["content"][:500] + "..." if len(result["content"]) > 500 else result["content"]
                response_text = f"Content from {url}:\n\n{content}"
            else:
                response_text = f"Scraping failed: {result['error_message']}"
        elif user_input.lower().startswith("research "):
            topic = user_input[9:]
            tool_trace = f"🔬 Researching: {topic}"
            result = deep_research(topic)
            if result["status"] == "success":
                response_text = f"Research on '{topic}':\n\n{result['summary']}\n\nSources: {result['total_sources']}"
            else:
                response_text = f"Research failed: {result['error_message']}"
        elif user_input.lower().startswith("generate image"):
            prompt = user_input[15:]
            tool_trace = f"🎨 Generating image: {prompt}"
            result = generate_image(prompt)
            if result["status"] == "success":
                response_text = f"Image generated successfully! Prompt: {prompt}"
                image_url = result.get("image_url")
            else:
                response_text = f"Image generation failed: {result['error_message']}"
        elif any(word in user_input.lower() for word in ["weather", "current", "latest", "news", "today's", "now"]):
            tool_trace = f"🔍 Detected current info request, searching for: {user_input}"
            result = web_search(user_input)
            if result["status"] == "success":
                response_text = f"Current information for '{user_input}':\n\n"
                for i, item in enumerate(result["results"][:3], 1):
                    response_text += f"{i}. {item['title']}\n   URL: {item['url']}\n   {item['description'][:150]}...\n\n"
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
        'image_url': image_url
    })

    st.experimental_rerun() 