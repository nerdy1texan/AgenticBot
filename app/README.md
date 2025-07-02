# AgenticBot App

This directory contains the main application files for the AgenticBot project, including the Streamlit web interface, agent implementation, and comprehensive test suite.

## 📁 Directory Structure

```
app/
├── streamlit_app.py          # Main Streamlit web application
├── main.py                   # Command-line interface and core logic
├── requirements.txt          # Python dependencies for the app
├── README.md                 # This file
├── chatgpt_agentic_clone/    # Agent implementation
│   ├── __init__.py
│   └── agent.py              # Core agent logic and tools
└── tests/                    # Comprehensive test suite
    ├── working_chat.py       # Working chat implementation
    ├── enhanced_chat.py      # Enhanced chat functionality
    ├── test_simple_chat.py   # Basic chat testing
    ├── test_with_tools.py    # Tool integration testing
    ├── test_agent_signature.py # Agent signature validation
    ├── test_agent_run_async.py # Async agent execution
    ├── test_direct_agent.py  # Direct agent interaction
    ├── test_alternative_api.py # Alternative API approaches
    ├── test_session_events.py # Session event handling
    ├── test_different_method.py # Different testing methods
    ├── test_direct_message.py # Direct message testing
    ├── test_message_receipt.py # Message receipt validation
    ├── test_explicit_agent.py # Explicit agent configuration
    ├── test_tools.py         # Tool functionality testing
    ├── test_object_attributes.py # Object attribute testing
    ├── test_content_object.py # Content object validation
    ├── test_runner_api.py    # Runner API testing
    ├── test_model_and_format.py # Model and format testing
    ├── test_message.py       # Message handling testing
    ├── test_specific_response.py # Specific response testing
    ├── test_final_approach.py # Final approach validation
    └── test_alternative_approach.py # Alternative approach testing
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Conda environment activated (see main README.md for setup)
- Required packages installed (see requirements.txt)

### Running the Streamlit App

1. **Navigate to the app directory:**
   ```bash
   cd app
   ```

2. **Run the Streamlit application:**
   ```bash
   streamlit run streamlit_app.py
   ```

3. **Access the web interface:**
   - Local URL: http://localhost:8501
   - Network URL: http://192.168.1.67:8501 (or your local IP)

### Running the Command-Line Interface

```bash
python main.py
```

## 🔧 Key Files

### `streamlit_app.py`
- **Purpose:** Main web interface for the AgenticBot
- **Features:** 
  - User-friendly chat interface
  - File upload capabilities
  - Real-time agent responses
  - Session management

### `main.py`
- **Purpose:** Command-line interface and core application logic
- **Features:**
  - Direct agent interaction
  - Tool execution
  - Error handling
  - Configuration management

### `chatgpt_agentic_clone/agent.py`
- **Purpose:** Core agent implementation
- **Features:**
  - Google ADK integration
  - Multi-tool support (web search, scraping, research, image generation)
  - Session management
  - Error handling and fallbacks

### `requirements.txt`
- **Purpose:** Python dependencies for the app
- **Key packages:**
  - streamlit
  - google-adk
  - firecrawl-py
  - google-generativeai
  - python-dotenv

## 🧪 Testing

The `tests/` directory contains a comprehensive test suite for validating different aspects of the agent:

- **Basic functionality:** `test_simple_chat.py`, `working_chat.py`
- **Tool integration:** `test_with_tools.py`, `test_tools.py`
- **API interactions:** `test_runner_api.py`, `test_alternative_api.py`
- **Message handling:** `test_message.py`, `test_message_receipt.py`
- **Session management:** `test_session_events.py`
- **Agent configuration:** `test_agent_signature.py`, `test_explicit_agent.py`

### Running Tests
```bash
# Run a specific test
python tests/working_chat.py

# Run all tests (if you have pytest installed)
pytest tests/
```

## 🔑 Environment Variables

Make sure you have a `.env` file in the app directory with:
```
GOOGLE_API_KEY=your_google_api_key_here
FIRECRAWL_API_KEY=your_firecrawl_api_key_here
```

## 🐛 Troubleshooting

### Common Issues

1. **ModuleNotFoundError: No module named 'google.generativeai'**
   ```bash
   pip install google-generativeai
   ```

2. **Streamlit not starting**
   - Check if you're in the correct directory (`app/`)
   - Ensure all dependencies are installed
   - Verify your `.env` file exists

3. **Agent not responding**
   - Check your API keys in `.env`
   - Verify internet connection
   - Check the console for error messages

### Getting Help

- Check the main project README.md for detailed setup instructions
- Review the test files for working examples
- Check the console output for detailed error messages

## 📝 Development

When making changes:
1. Test your changes with the appropriate test files
2. Update this README if you add new features
3. Ensure all dependencies are listed in `requirements.txt`
4. Test both Streamlit and command-line interfaces
