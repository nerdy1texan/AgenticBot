"""
Test if the tools are working properly
"""

import asyncio
import os
from dotenv import load_dotenv
from chatgpt_agentic_clone.agent import web_search, setup_gemini

async def test_tools():
    """Test the tools directly."""
    
    print("=== Testing Tools Directly ===")
    
    # Load environment variables
    load_dotenv()
    
    # Setup Gemini
    setup_gemini()
    
    # Test web_search tool
    print("\n--- Testing web_search tool ---")
    try:
        result = web_search("weather in Atlanta today")
        print(f"✅ web_search result: {result}")
    except Exception as e:
        print(f"❌ web_search failed: {e}")
    
    # Test with a simple agent that only has the web_search tool
    print("\n--- Testing agent with web_search tool ---")
    
    from google.adk import Agent
    from google.adk.sessions import InMemorySessionService
    from google.adk import Runner
    
    # Create a simple agent with just the web_search tool
    simple_agent = Agent(
        name="simple_agent",
        model="gemini-2.0-flash-exp",
        instruction="You are a helpful assistant. When asked about current information like weather, use the web_search tool to find the answer. Always provide the actual search results to the user.",
        tools=[web_search],
    )
    
    # Setup
    session_service = InMemorySessionService()
    runner = Runner(
        agent=simple_agent,
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
    
    try:
        async for event in runner.run_async(
            user_id="test_user",
            session_id="test_session",
            new_message=content_message
        ):
            print(f"✅ Agent response: {event}")
            break
    except Exception as e:
        print(f"❌ Agent failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_tools())