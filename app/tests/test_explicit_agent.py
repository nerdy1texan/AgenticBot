"""
Test an agent with very explicit instructions to use tools
"""

import asyncio
import os
from dotenv import load_dotenv
from chatgpt_agentic_clone.agent import web_search, setup_gemini
from google.adk import Agent
from google.adk.sessions import InMemorySessionService
from google.adk import Runner

async def test_explicit_agent():
    """Test an agent with very explicit tool usage instructions."""
    
    print("=== Testing Explicit Agent ===")
    
    # Load environment variables
    load_dotenv()
    
    # Setup Gemini
    setup_gemini()
    
    # Create an agent with very explicit instructions
    explicit_agent = Agent(
        name="explicit_agent",
        model="gemini-2.0-flash-exp",
        instruction="""You are a helpful assistant with access to a web_search tool. 

IMPORTANT: When users ask about current information like weather, news, or real-time data, you MUST use the web_search tool to get the answer. Do NOT respond with generic messages.

For weather queries, ALWAYS use web_search to get current weather information and provide the actual weather data to the user.

Example: If someone asks "What's the weather in Atlanta?", you should:
1. Use web_search("weather in Atlanta")
2. Read the search results
3. Provide the actual weather information from the results

Do not say "I understand" or "I'm ready to help" - actually help by using the tools!""",
        tools=[web_search],
    )
    
    # Setup
    session_service = InMemorySessionService()
    runner = Runner(
        agent=explicit_agent,
        app_name="test_app",
        session_service=session_service
    )
    
    # Create session
    await session_service.create_session(
        app_name="test_app",
        user_id="test_user",
        session_id="test_session"
    )
    
    # Test the agent
    query = "What's the weather in Atlanta today?"
    
    class ContentObject:
        def __init__(self, text):
            self.parts = [{"text": text}]
    
    content_message = ContentObject(query)
    
    print(f"\n--- Testing with query: {query} ---")
    
    try:
        async for event in runner.run_async(
            user_id="test_user",
            session_id="test_session",
            new_message=content_message
        ):
            print(f"✅ Agent response: {event}")
            # Extract the text content
            if hasattr(event, 'content') and event.content:
                if hasattr(event.content, 'parts'):
                    for part in event.content.parts:
                        if hasattr(part, 'text'):
                            print(f"Response text: {part.text}")
            break
    except Exception as e:
        print(f"❌ Agent failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_explicit_agent())