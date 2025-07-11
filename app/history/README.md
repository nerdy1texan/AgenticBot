# Chat History Directory

This directory stores persistent chat session history for AgenticBot.

## Structure

- Each chat session is saved as a JSON file with timestamp-based naming
- Format: `chat_YYYYMMDD_HHMMSS.json`
- Contains complete conversation history, agentic logs, and metadata

## File Format

```json
{
  "session_id": "unique_session_identifier",
  "created_at": "2025-01-XX XX:XX:XX",
  "updated_at": "2025-01-XX XX:XX:XX", 
  "title": "Auto-generated or user-defined title",
  "chat_history": [
    {
      "role": "user|assistant",
      "content": "message content",
      "timestamp": "YYYY-MM-DD HH:MM:SS",
      "image_data": "base64_data_if_present"
    }
  ],
  "agentic_logs": [
    {
      "timestamp": "[HH:MM:SS]",
      "type": "agent_step|tool_execution|api_call|result_processed",
      "message": "log message",
      "full_message": "timestamped log entry"
    }
  ],
  "metadata": {
    "total_messages": 0,
    "tools_used": [],
    "session_duration": "HH:MM:SS"
  }
}
```

## Features

- Automatic session saving after each interaction
- Searchable chat history by title or content
- Session restoration with complete context
- Export capabilities for backup
- Automatic cleanup of old sessions (configurable) 