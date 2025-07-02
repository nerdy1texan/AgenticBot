"""
Test passing the message directly without Content object
"""

import asyncio
import os
from dotenv import load_dotenv
from google.adk import Agent
from google.adk.sessions import InMemorySessionService
from google.adk import Runner

async def test_direct_message():
    """Test passing the message directly."""
    
    print("=== Testing Direct Message ===")
    
    # Load environment variables
    load_dotenv()
    
    # Setup Gemini
    from chatgpt_agentic_clone.agent import setup_gemini
    setup_gemini()
    
    # Create a simple agent
    simple_agent = Agent(
        name="simple_agent",
        model="gemini-2.0-flash-exp",
        instruction="You are a helpful assistant. When someone asks you a question, answer it directly. If they ask about weather, tell them you would need to search for that information.",
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
    
    test_query = "What's the weather in Atlanta?"
    
    print(f"\n--- Testing with query: '{test_query}' ---")
    
    # Try different ways to pass the message
    test_methods = [
        ("Direct string", test_query),
        ("Dict with text", {"text": test_query}),
        ("Dict with content", {"content": test_query}),
        ("Dict with message", {"message": test_query}),
        ("Dict with user_input", {"user_input": test_query}),
    ]
    
    for method_name, message in test_methods:
        print(f"\n--- Method: {method_name} ---")
        try:
            async for event in runner.run_async(
                user_id="test_user",
                session_id="test_session",
                new_message=message
            ):
                print(f"✅ {method_name} worked!")
                # Extract the text content
                if hasattr(event, 'content') and event.content:
                    if hasattr(event.content, 'parts'):
                        for part in event.content.parts:
                            if hasattr(part, 'text'):
                                print(f"Response: {part.text}")
                break
        except Exception as e:
            print(f"❌ {method_name} failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_direct_message())