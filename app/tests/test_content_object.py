"""
Test creating Content objects manually
"""

import asyncio
from google.adk import Runner, Agent
from google.adk.sessions import InMemorySessionService

async def test_content_objects():
    """Test different ways to create Content objects."""
    
    print("=== Testing Content Object Creation ===")
    
    # Create a simple agent
    test_agent = Agent(
        name="test_agent",
        model="gemini-2.0-flash-exp",
        instruction="You are a helpful assistant. Respond to user queries."
    )
    
    # Setup
    session_service = InMemorySessionService()
    runner = Runner(
        agent=test_agent,
        app_name="test_app",
        session_service=session_service
    )
    
    # Create session
    await session_service.create_session(
        app_name="test_app",
        user_id="test_user",
        session_id="test_session"
    )
    
    test_query = "Hello, how are you?"
    
    # Test 1: Try creating a simple Content-like object
    class SimpleContent:
        def __init__(self, text):
            self.parts = [{"text": text}]
            self.role = "user"
    
    try:
        content_obj = SimpleContent(test_query)
        async for event in runner.run_async(
            user_id="test_user",
            session_id="test_session",
            new_message=content_obj
        ):
            print(f"✅ SimpleContent object worked!")
            print(f"Response: {event}")
            break
    except Exception as e:
        print(f"❌ SimpleContent failed: {e}")
    
    # Test 2: Try with a dict that looks like Content
    try:
        content_dict = {
            "parts": [{"text": test_query}],
            "role": "user"
        }
        async for event in runner.run_async(
            user_id="test_user",
            session_id="test_session",
            new_message=content_dict
        ):
            print(f"✅ Content dict worked!")
            print(f"Response: {event}")
            break
    except Exception as e:
        print(f"❌ Content dict failed: {e}")
    
    # Test 3: Try with just parts
    try:
        parts_dict = {
            "parts": [{"text": test_query}]
        }
        async for event in runner.run_async(
            user_id="test_user",
            session_id="test_session",
            new_message=parts_dict
        ):
            print(f"✅ Parts dict worked!")
            print(f"Response: {event}")
            break
    except Exception as e:
        print(f"❌ Parts dict failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_content_objects())