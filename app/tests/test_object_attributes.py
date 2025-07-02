"""
Test what attributes the API expects on the Content object
"""

import asyncio
from google.adk import Runner, Agent
from google.adk.sessions import InMemorySessionService

async def test_object_attributes():
    """Test different object structures to see what works."""
    
    print("=== Testing Object Attributes ===")
    
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
    
    # Test different object structures
    test_objects = [
        # Test 1: Object with parts attribute
        type('Content', (), {
            'parts': [type('Part', (), {'text': test_query})()],
            'role': 'user'
        })(),
        
        # Test 2: Object with parts as list of dicts
        type('Content', (), {
            'parts': [{'text': test_query}],
            'role': 'user'
        })(),
        
        # Test 3: Object with just parts
        type('Content', (), {
            'parts': [{'text': test_query}]
        })(),
        
        # Test 4: Object with different structure
        type('Content', (), {
            'content': test_query,
            'role': 'user'
        })(),
    ]
    
    for i, obj in enumerate(test_objects, 1):
        print(f"\n--- Test {i}: {type(obj).__name__} ---")
        print(f"Attributes: {dir(obj)}")
        
        try:
            async for event in runner.run_async(
                user_id="test_user",
                session_id="test_session",
                new_message=obj
            ):
                print(f"✅ Test {i} worked!")
                print(f"Response: {event}")
                break
        except Exception as e:
            print(f"❌ Test {i} failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_object_attributes())