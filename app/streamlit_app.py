import streamlit as st
import os
import base64
from io import BytesIO
from dotenv import load_dotenv
from chatgpt_agentic_clone.agent import web_search, scrape_webpage, deep_research, generate_image, setup_gemini
import google.generativeai as genai
import sys
import time
from datetime import datetime
from history_manager import HistoryManager

# --- Setup ---
load_dotenv()
setup_gemini()
model = genai.GenerativeModel('gemini-2.0-flash-exp')

print("PYTHON EXECUTABLE:", sys.executable)

# Initialize History Manager
history_manager = HistoryManager()

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
    .agentic-log {
        background: #2d3748;
        border: 1px solid #4a5568;
        border-radius: 8px;
        padding: 10px;
        margin: 5px 0;
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
        color: #e2e8f0;
    }
    .agent-step {
        color: #90cdf4;
        font-weight: bold;
    }
    .tool-execution {
        color: #68d391;
    }
    .api-call {
        color: #fbb6ce;
    }
    .result-processed {
        color: #ffd89b;
    }
    .history-item {
        background: #2d3748;
        border-radius: 8px;
        padding: 8px;
        margin: 4px 0;
        cursor: pointer;
        transition: background-color 0.2s;
    }
    .history-item:hover {
        background: #4a5568;
    }
    .history-title {
        font-size: 0.9rem;
        font-weight: bold;
        color: #e2e8f0;
        margin-bottom: 2px;
    }
    .history-meta {
        font-size: 0.7rem;
        color: #a0aec0;
    }
    .new-chat-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: bold;
        cursor: pointer;
        width: 100%;
        margin-bottom: 1rem;
    }
    .new-chat-btn:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Helper Functions for Agentic Logging ---
def log_agentic_step(step_type: str, message: str, timestamp: bool = True):
    """Add an agentic activity log entry"""
    if 'agentic_logs' not in st.session_state:
        st.session_state.agentic_logs = []
    
    timestamp_str = f"[{datetime.now().strftime('%H:%M:%S')}] " if timestamp else ""
    log_entry = {
        'timestamp': timestamp_str,
        'type': step_type,
        'message': message,
        'full_message': f"{timestamp_str}{message}"
    }
    st.session_state.agentic_logs.append(log_entry)

def clear_agentic_logs():
    """Clear previous agentic logs"""
    if 'agentic_logs' in st.session_state:
        st.session_state.agentic_logs = []

def initialize_new_session():
    """Initialize a new chat session"""
    st.session_state.chat_history = []
    st.session_state.agentic_logs = []
    st.session_state.tool_trace = []
    st.session_state.current_session_id = None
    st.session_state.current_session_title = None
    st.session_state.session_created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.chat = model.start_chat(history=[])
    st.session_state.loaded_session_filepath = None

def save_current_session():
    """Save the current chat session to history"""
    if st.session_state.get('chat_history') and len(st.session_state.chat_history) > 0:
        session_data = {
            'session_id': st.session_state.get('current_session_id'),
            'created_at': st.session_state.get('session_created_at', datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            'title': st.session_state.get('current_session_title'),
            'chat_history': [],
            'agentic_logs': st.session_state.get('agentic_logs', [])
        }
        
        # Add timestamps to chat history entries
        for entry in st.session_state.chat_history:
            entry_with_timestamp = entry.copy()
            if 'timestamp' not in entry_with_timestamp:
                entry_with_timestamp['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            session_data['chat_history'].append(entry_with_timestamp)
        
        return history_manager.save_session(session_data)
    return None

def load_session_from_history(filepath: str):
    """Load a saved session from history"""
    session_data = history_manager.load_session(filepath)
    if session_data:
        st.session_state.chat_history = session_data.get('chat_history', [])
        st.session_state.agentic_logs = session_data.get('agentic_logs', [])
        st.session_state.tool_trace = []
        st.session_state.current_session_id = session_data.get('session_id')
        st.session_state.current_session_title = session_data.get('title')
        st.session_state.session_created_at = session_data.get('created_at')
        st.session_state.chat = model.start_chat(history=[])
        st.session_state.loaded_session_filepath = filepath
        return True
    return False

def is_session_modified():
    """Check if current session has been modified since loading"""
    if not st.session_state.get('loaded_session_filepath'):
        return True  # New session, always considered modified
    
    # Load original session data
    original_data = history_manager.load_session(st.session_state.loaded_session_filepath)
    if not original_data:
        return True
    
    # Compare message counts
    original_msg_count = len(original_data.get('chat_history', []))
    current_msg_count = len(st.session_state.get('chat_history', []))
    
    return current_msg_count != original_msg_count

# --- Session State Initialization ---
if 'chat_history' not in st.session_state:
    initialize_new_session()

if 'history_search' not in st.session_state:
    st.session_state.history_search = ""

if 'show_history' not in st.session_state:
    st.session_state.show_history = True

# --- Sidebar ---
with st.sidebar:
    st.markdown('<div class="sidebar-logo"><img src="https://cdn-icons-png.flaticon.com/512/4712/4712035.png" alt="Bot Logo"><span class="sidebar-title">AgenticBot</span></div>', unsafe_allow_html=True)
    
    # New Chat Button
    if st.button("🆕 New Chat", key="new_chat", help="Start a new conversation"):
        # Save current session only if it has been modified
        if is_session_modified():
            save_current_session()
        initialize_new_session()
        st.experimental_rerun()
    
    # Cleanup button (optional)
    if st.button("🧹 Clean Duplicates", key="cleanup", help="Remove duplicate session files"):
        deleted_count = history_manager.cleanup_duplicate_sessions()
        if deleted_count > 0:
            st.success(f"Cleaned up {deleted_count} duplicate files")
        else:
            st.info("No duplicates found")
        st.experimental_rerun()
    
    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    
    # Capabilities Section
    st.markdown('<div class="sidebar-section"><b>Capabilities:</b><br><span style="color:#e573c7;">●</span> General Q&A<br><span style="color:#64b5f6;">●</span> Web search<br><span style="color:#81c784;">●</span> Web scraping<br><span style="color:#ffd54f;">●</span> Deep research<br><span style="color:#ff8a65;">●</span> Image generation</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    
    # Special Commands Section
    st.markdown('<div class="sidebar-section"><b>Special commands:</b><br><span style="color:#81c784;">•</span> <code>search for [query]</code><br><span style="color:#ffd54f;">•</span> <code>scrape [url]</code><br><span style="color:#64b5f6;">•</span> <code>research [topic]</code><br><span style="color:#ff8a65;">•</span> <code>generate image [description]</code></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    
    # Chat History Section
    st.markdown("**📚 Chat History**")
    
    # History search
    search_query = st.text_input("🔍 Search history", value=st.session_state.history_search, key="history_search_input", placeholder="Search chats...")
    
    if search_query != st.session_state.history_search:
        st.session_state.history_search = search_query
    
    # Toggle history visibility
    col1, col2 = st.columns([3, 1])
    with col1:
        show_all = st.checkbox("Show all sessions", value=st.session_state.show_history)
    with col2:
        if st.button("🔄", help="Refresh history"):
            st.experimental_rerun()
    
    st.session_state.show_history = show_all
    
    # Display history
    if st.session_state.show_history:
        if st.session_state.history_search:
            sessions = history_manager.search_sessions(st.session_state.history_search)
        else:
            sessions = history_manager.list_sessions()
        
        if sessions:
            st.markdown(f"*Found {len(sessions)} session(s)*")
            
            # Display sessions
            for i, session in enumerate(sessions[:20]):  # Limit to 20 most recent
                with st.container():
                    col1, col2 = st.columns([4, 1])
                    
                    with col1:
                        # Highlight current session
                        is_current = (st.session_state.get('current_session_id') == session['session_id'])
                        button_text = f"{'📍' if is_current else '💬'} {session['title'][:30]}{'...' if len(session['title']) > 30 else ''}"
                        
                        if st.button(
                            button_text, 
                            key=f"load_session_{i}",
                            help=f"{'Current session' if is_current else 'Load session from'} {session['updated_at']}",
                            disabled=is_current
                        ):
                            # Only save current session if it's different and has been modified
                            if (st.session_state.get('current_session_id') != session['session_id'] and 
                                is_session_modified()):
                                save_current_session()
                            
                            if load_session_from_history(session['filepath']):
                                st.success(f"Loaded: {session['title']}")
                                st.experimental_rerun()
                            else:
                                st.error("Failed to load session")
                    
                    with col2:
                        if st.button("🗑️", key=f"delete_session_{i}", help="Delete this session"):
                            if history_manager.delete_session(session['filepath']):
                                # If we're deleting the current session, start a new one
                                if st.session_state.get('current_session_id') == session['session_id']:
                                    initialize_new_session()
                                st.success("Session deleted")
                                st.experimental_rerun()
                            else:
                                st.error("Failed to delete")
                    
                    # Session metadata
                    tools_str = ", ".join(session['tools_used']) if session['tools_used'] else "None"
                    st.caption(f"📅 {session['updated_at'][:16]} | 💬 {session['total_messages']} msgs | 🔧 {tools_str}")
                    
                    st.markdown('<div style="margin-bottom: 8px;"></div>', unsafe_allow_html=True)
        else:
            st.markdown("*No chat history found*")
            if st.session_state.history_search:
                st.markdown("*Try a different search term*")
    
    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align:center; margin-top:2rem;"><a href="https://github.com/nerdy1texan/AgenticBot.git" target="_blank" style="color:#90caf9; text-decoration:none; font-weight:bold; font-size:1.1rem;">🌐 View on GitHub</a></div>', unsafe_allow_html=True)

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

# Session info display
if st.session_state.get('current_session_title'):
    session_status = "📍 Current Session" if st.session_state.get('loaded_session_filepath') else "💾 New Session"
    st.info(f"{session_status}: **{st.session_state.current_session_title}** (Started: {st.session_state.get('session_created_at', 'Unknown')[:16]})")

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

# --- Agentic Activity Logs Display ---
if st.session_state.agentic_logs:
    with st.expander("🔍 Agentic Workflow Activity", expanded=True):
        st.markdown("**Real-time Agent Execution Log:**")
        for log in st.session_state.agentic_logs[-15:]:  # Show last 15 entries
            css_class = {
                'agent_step': 'agent-step',
                'tool_execution': 'tool-execution', 
                'api_call': 'api-call',
                'result_processed': 'result-processed'
            }.get(log['type'], '')
            
            st.markdown(f'<div class="agentic-log {css_class}">{log["full_message"]}</div>', unsafe_allow_html=True)

# --- Tool Trace Display ---
if st.session_state.tool_trace:
    with st.expander("🔧 Tool/Action Trace", expanded=False):
        for trace in st.session_state.tool_trace[-5:]:
            st.markdown(trace)

# --- User Input ---
st.markdown("</div>", unsafe_allow_html=True)  # Close main-chat-card
user_input = st.chat_input("Type your message and press Enter...")

if user_input:
    # Clear previous logs for new query
    clear_agentic_logs()
    
    # Add timestamp to user message
    user_message = {
        'role': 'user', 
        'content': user_input,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    st.session_state.chat_history.append(user_message)
    
    response_text = ""
    image_data = None
    tool_trace = None

    try:
        # Log user query processing
        log_agentic_step('agent_step', f"🤖 Root Agent received query: '{user_input}'")
        log_agentic_step('agent_step', "🔍 Analyzing query intent and selecting appropriate agent...")
        
        # Tool detection
        if user_input.lower().startswith("search for"):
            query = user_input[11:]
            log_agentic_step('agent_step', f"🎯 Delegating to Search Agent for query: '{query}'")
            log_agentic_step('tool_execution', "🔧 Search Agent preparing web search tool...")
            tool_trace = f"🔍 Web search for: {query}"
            
            log_agentic_step('api_call', "🌐 Executing Firecrawl web search API call...")
            result = web_search(query)
            
            if result["status"] == "success":
                log_agentic_step('result_processed', f"✅ Search completed - found {len(result['results'])} results")
                log_agentic_step('agent_step', "📝 Search Agent formatting results for user...")
                response_text = f"Search results for '{query}':<br><br>"
                for i, item in enumerate(result["results"][:5], 1):
                    response_text += f"{i}. <b>{item['title']}</b><br>🔗 <a href='{item['url']}' target='_blank'>{item['url']}</a><br>{item['description'][:100]}...<br><br>"
                log_agentic_step('agent_step', "🎉 Root Agent received formatted results from Search Agent")
            else:
                log_agentic_step('result_processed', f"❌ Search failed: {result['error_message']}")
                response_text = f"Search failed: {result['error_message']}"
                
        elif user_input.lower().startswith("scrape "):
            url = user_input[7:]
            log_agentic_step('agent_step', f"🎯 Delegating to Web Extraction Agent for URL: '{url}'")
            log_agentic_step('tool_execution', "🔧 Web Extraction Agent preparing webpage scraper...")
            tool_trace = f"🕸️ Scraping: {url}"
            
            log_agentic_step('api_call', "🌐 Executing Firecrawl webpage scraping API call...")
            result = scrape_webpage(url)
            
            if result["status"] == "success":
                log_agentic_step('result_processed', f"✅ Scraping completed - extracted {len(result['content'])} characters")
                log_agentic_step('agent_step', "📝 Web Extraction Agent processing and formatting content...")
                content = result["content"][:500] + "..." if len(result["content"]) > 500 else result["content"]
                response_text = f"Content from <b>{url}</b>:<br><br>{content}"
                log_agentic_step('agent_step', "🎉 Root Agent received processed content from Web Extraction Agent")
            else:
                log_agentic_step('result_processed', f"❌ Scraping failed: {result['error_message']}")
                response_text = f"Scraping failed: {result['error_message']}"
                
        elif user_input.lower().startswith("research "):
            topic = user_input[9:]
            log_agentic_step('agent_step', f"🎯 Delegating to Research Agent for topic: '{topic}'")
            log_agentic_step('tool_execution', "🔧 Research Agent preparing deep research tool...")
            tool_trace = f"🔬 Researching: {topic}"
            
            log_agentic_step('api_call', "🌐 Executing Firecrawl deep research API call...")
            result = deep_research(topic)
            
            if result["status"] == "success":
                log_agentic_step('result_processed', f"✅ Research completed - analyzed {result['total_sources']} sources")
                log_agentic_step('agent_step', "📝 Research Agent synthesizing findings and creating summary...")
                response_text = f"Research on '<b>{topic}</b>':<br><br>{result['summary']}<br><br>Sources: {result['total_sources']}"
                log_agentic_step('agent_step', "🎉 Root Agent received research summary from Research Agent")
            else:
                log_agentic_step('result_processed', f"❌ Research failed: {result['error_message']}")
                response_text = f"Research failed: {result['error_message']}"
                
        elif user_input.lower().startswith("generate image"):
            prompt = user_input[15:]
            log_agentic_step('agent_step', f"🎯 Delegating to Image Generation Agent for prompt: '{prompt}'")
            log_agentic_step('tool_execution', "🔧 Image Generation Agent preparing Gemini Imagen model...")
            tool_trace = f"🎨 Generating image: {prompt}"
            
            log_agentic_step('api_call', "🌐 Executing Google Gemini Imagen API call...")
            result = generate_image(prompt)
            
            if result["status"] == "success" and result.get("image_data"):
                log_agentic_step('result_processed', "✅ Image generation completed successfully")
                log_agentic_step('agent_step', "📝 Image Generation Agent processing image data...")
                response_text = f"Image generated successfully! Prompt: <b>{prompt}</b>"
                image_data = result.get("image_data")
                log_agentic_step('agent_step', "🎉 Root Agent received generated image from Image Generation Agent")
            else:
                log_agentic_step('result_processed', f"❌ Image generation failed: {result.get('error_message', 'Unknown error')}")
                response_text = f"Image generation failed: {result.get('error_message', 'Unknown error')}"
                
        elif any(word in user_input.lower() for word in ["weather", "current", "latest", "news", "today's", "now"]):
            log_agentic_step('agent_step', f"🎯 Detected current info request, delegating to Search Agent")
            log_agentic_step('tool_execution', "🔧 Search Agent preparing real-time information search...")
            tool_trace = f"🔍 Detected current info request, searching for: {user_input}"
            
            log_agentic_step('api_call', "🌐 Executing Firecrawl web search for current information...")
            result = web_search(user_input)
            
            if result["status"] == "success":
                log_agentic_step('result_processed', f"✅ Current info search completed - found {len(result['results'])} results")
                log_agentic_step('agent_step', "📝 Search Agent filtering most relevant current information...")
                response_text = f"Current information for '<b>{user_input}</b>':<br><br>"
                for i, item in enumerate(result["results"][:3], 1):
                    response_text += f"{i}. <b>{item['title']}</b><br>🔗 <a href='{item['url']}' target='_blank'>{item['url']}</a><br>{item['description'][:150]}...<br><br>"
                log_agentic_step('agent_step', "🎉 Root Agent received current information from Search Agent")
            else:
                log_agentic_step('result_processed', f"❌ Current info search failed: {result['error_message']}")
                response_text = f"Search failed: {result['error_message']}"
        else:
            # Regular chat
            log_agentic_step('agent_step', "💬 Processing as general conversation with Root Agent")
            log_agentic_step('api_call', "🧠 Executing Google Gemini model for general response...")
            response = st.session_state.chat.send_message(user_input)
            response_text = response.text
            log_agentic_step('result_processed', "✅ General response generated successfully")
            log_agentic_step('agent_step', "📝 Root Agent formatted response for user")
            
    except Exception as e:
        log_agentic_step('result_processed', f"❌ Error during processing: {str(e)}")
        response_text = f"❌ Error: {e}"

    # Save tool trace
    if tool_trace:
        st.session_state.tool_trace.append(tool_trace)

    # Final log entry
    log_agentic_step('agent_step', "🏁 Task completed - response ready for user")

    # Save assistant response with timestamp
    assistant_message = {
        'role': 'assistant',
        'content': response_text,
        'image_data': image_data,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    st.session_state.chat_history.append(assistant_message)
    
    # Auto-save session after each interaction (this will update existing sessions properly)
    if len(st.session_state.chat_history) >= 2:  # At least one exchange
        save_current_session()

    st.experimental_rerun()

# --- Footer ---
st.markdown('<div class="custom-footer">✨ AgenticBot &copy; 2025 &mdash; <a href="https://github.com/nerdy1texan/AgenticBot.git" style="color:#90caf9; text-decoration:none;">GitHub</a> | Built with Google Generative AI, Firecrawl, and Streamlit</div>', unsafe_allow_html=True) 