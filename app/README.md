# AgenticBot Application

This directory contains the core AgenticBot application with both CLI and web interfaces.

## 📁 Directory Structure

```
app/
├── main.py                     # CLI application entry point
├── streamlit_app.py           # Streamlit web interface with history
├── history_manager.py         # Chat history persistence manager
├── requirements.txt           # Python dependencies
├── .env.template             # Environment variables template
├── README.md                 # This file
├── history/                  # Chat session storage directory
│   ├── README.md            # History system documentation
│   └── .gitkeep             # Git tracking for empty directory
├── tests/                    # Test files directory
│   ├── test_direct_agent.py # Direct agent testing
│   ├── test_explicit_agent.py # Explicit agent testing
│   └── [other test files]   # Various testing approaches
└── chatgpt_agentic_clone/
    ├── __init__.py          # Package initialization
    └── agent.py             # Multi-agent system implementation
```

## 🚀 Features

### Core Capabilities
- **🤖 Multi-Agent System**: Coordinated specialized agents
- **🌐 Web Search**: Real-time information retrieval
- **📄 Web Scraping**: Content extraction from URLs
- **🔍 Deep Research**: Multi-source research synthesis
- **🎨 Image Generation**: AI-powered image creation
- **💬 Interactive Interfaces**: CLI and web-based chat

### New History Features ✨
- **📚 Persistent Chat History**: Automatic session saving with JSON storage
- **🔍 Smart Search**: Find past conversations by title or content
- **🆕 Session Management**: Easy new chat creation and switching
- **📊 Session Analytics**: Message counts, tools used, and duration tracking
- **🗑️ History Management**: Delete unwanted sessions
- **📥 Export Capabilities**: Save sessions in multiple formats
- **🔄 Session Restoration**: Complete context recovery with agentic logs

## 🎯 Usage

### Streamlit Web Interface

Start the web application:
```bash
streamlit run streamlit_app.py
```

#### History Features:
- **New Chat Button**: Start fresh conversations while preserving current session
- **History Sidebar**: Browse, search, and manage past conversations
- **Auto-Save**: Sessions automatically saved after each interaction
- **Session Info**: Current session title and start time displayed
- **Search History**: Find specific conversations by keywords
- **Delete Sessions**: Remove unwanted chat history
- **Load Sessions**: Restore complete conversation context

#### Special Commands:
- `search for [query]` - Web search
- `scrape [url]` - Extract webpage content
- `research [topic]` - Deep multi-source research
- `generate image [description]` - Create AI images

### CLI Interface

Start the command-line version:
```bash
python main.py
```

## 🔧 History System

### Automatic Features
- **Auto-Save**: Every conversation automatically saved to `history/` directory
- **Smart Titles**: Auto-generated from first user message
- **Timestamping**: All messages include creation timestamps
- **Tool Tracking**: Logs which agents/tools were used in each session
- **Metadata**: Session duration, message counts, and usage statistics

### File Structure
Sessions saved as JSON files with format: `chat_YYYYMMDD_HHMMSS_[session_id].json`

### Search Capabilities
- Search by conversation title
- Search within message content
- Filter by date ranges
- Browse by tools used

## 📊 Session Data Format

Each saved session includes:
```json
{
  "session_id": "unique_identifier",
  "created_at": "2025-01-XX XX:XX:XX",
  "updated_at": "2025-01-XX XX:XX:XX",
  "title": "Auto-generated or custom title",
  "chat_history": [
    {
      "role": "user|assistant",
      "content": "message content",
      "timestamp": "YYYY-MM-DD HH:MM:SS",
      "image_data": "base64_if_present"
    }
  ],
  "agentic_logs": [
    {
      "timestamp": "[HH:MM:SS]",
      "type": "agent_step|tool_execution|api_call|result_processed",
      "message": "detailed log entry"
    }
  ],
  "metadata": {
    "total_messages": 10,
    "tools_used": ["web_search", "image_generation"],
    "session_duration": "00:15:30"
  }
}
```

## 🛠️ Configuration

### Environment Variables
Create `.env` file from template:
```bash
cp .env.template .env
```

Required variables:
- `GOOGLE_API_KEY`: Google AI API key
- `FIRECRAWL_API_KEY`: Firecrawl service API key

### History Settings
The history system is automatically configured with:
- **Storage Location**: `history/` directory
- **Auto-Save**: Enabled by default
- **Max Sessions**: 50 (older sessions auto-deleted)
- **Search Indexing**: Title and content indexed
- **Export Formats**: JSON and TXT supported

## 🔒 Privacy & Security

### Data Handling
- **Local Storage**: All chat history stored locally in `history/` directory
- **No Cloud Sync**: Sessions remain on your machine unless exported
- **Encryption**: Consider encrypting the `history/` directory for sensitive data
- **API Keys**: Stored securely in `.env` file (excluded from version control)

### Cleanup Options
- **Manual Delete**: Remove individual sessions via web interface
- **Auto-Cleanup**: Automatic removal of sessions beyond limit (50 by default)
- **Export Before Delete**: Save important conversations before cleanup

## 🧪 Testing

Run the test suite:
```bash
python -m pytest tests/
```

Test individual components:
```bash
# Test history manager
python -c "from history_manager import HistoryManager; hm = HistoryManager(); print('History system working!')"

# Test agent system
python tests/test_direct_agent.py
```

## 🐛 Troubleshooting

### Common Issues

**History not saving**
- Check write permissions in `history/` directory
- Verify session has at least one complete exchange
- Check console for error messages

**Sessions not loading**
- Ensure JSON files are not corrupted
- Check file permissions in `history/` directory
- Try refreshing the history list

**Search not working**
- Clear search input and try again
- Check if session files contain searchable content
- Verify file structure matches expected format

### Debug Mode
Enable detailed logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📚 Dependencies

Core requirements in `requirements.txt`:
- `streamlit` - Web interface framework
- `google-generativeai` - Google AI integration
- `firecrawl-py` - Web intelligence
- `python-dotenv` - Environment management

## 🤝 Contributing

1. Test new features with existing history system
2. Ensure backward compatibility with saved sessions
3. Update documentation for new history features
4. Add appropriate tests for history functionality

## 📄 License

Same as parent project - MIT License

---

**💡 Tip**: The history system automatically backs up your conversations, so you can experiment freely with AgenticBot knowing your valuable interactions are preserved!
