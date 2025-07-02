"""
Test different message formats to see what the API accepts
"""

import asyncio
from google.adk import Runner
from google.adk.sessions import InMemorySessionService
from chatgpt_agentic_clone.agent import root_agent

async def test_message_formats():
    """Test different message formats."""
    
    print("=== Testing Message Formats ===")
    
    # Setup
    session_service = InMemorySessionService()
    runner = Runner(
        agent=root_agent,
        app_name="test_app",
        session_service=session_service
    )
    
    # Create session
    await session_service.create_session(
        app_name="test_app",
        user_id="test_user",
        session_id="test_session"
    )
    
    # Test different formats
    test_message = "Hello"
    
    formats = [
        ("Simple string", test_message),
        ("Dict with role/content", {"role": "user", "content": test_message}),
        ("Dict with just content", {"content": test_message}),
        ("Dict with parts", {"parts": [{"text": test_message}]}),
    ]
    
    for name, message in formats:
        print(f"\nTesting: {name}")
        try:
            async for event in runner.run_async(
                user_id="test_user",
                session_id="test_session", 
                new_message=message
            ):
                print(f"✅ {name} worked! Event: {event}")
                break
        except Exception as e:
            print(f"❌ {name} failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_message_formats())