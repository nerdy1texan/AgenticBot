"""
Test using session events to pass messages
"""

import asyncio
import os
from dotenv import load_dotenv
from google.adk import Agent
from google.adk.sessions import InMemorySessionService
from google.adk import Runner

async def test_session_events():
    """Test using session events to pass messages."""
    
    print("=== Testing Session Events ===")
    
    # Load environment variables
    load_dotenv()
    
    # Setup Gemini
    from chatgpt_agentic_clone.agent import setup_gemini
    setup_gemini()
    
    # Create a simple agent
    simple_agent = Agent(
        name="simple_agent",
        model="gemini-2.0-flash-exp",
        instruction="You are a helpful assistant. Answer questions directly.",
    )
    
    # Setup
    session_service = InMemorySessionService()
    runner = Runner(
        agent=simple_agent,
        app_name="test_app",
        session_service=session_service
    )
    
    # Create session
    session_id = f"test_session_{asyncio.get_event_loop().time()}"
    user_id = f"test_user_{asyncio.get_event_loop().time()}"
    
    session = await session_service.create_session(
        app_name="test_app",
        user_id=user_id,
        session_id=session_id
    )
    
    test_query = "What is 2+2?"
    
    print(f"\n--- Testing with query: '{test_query}' ---")
    
    # Try appending an event to the session first
    try:
        # Append a user event to the session
        await session_service.append_event(
            app_name="test_app",
            user_id=user_id,
            session_id=session_id,
            event={
                "role": "user",
                "content": test_query
            }
        )
        
        print("✅ Event appended to session")
        
        # Now try running the agent
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message={}  # Empty since we added the event to session
        ):
            print(f"✅ Agent responded!")
            if hasattr(event, 'content') and event.content:
                if hasattr(event.content, 'parts'):
                    for part in event.content.parts:
                        if hasattr(part, 'text'):
                            print(f"Response: {part.text}")
            break
    except Exception as e:
        print(f"❌ Session events failed: {e}")
        
        # Try a different approach - maybe we need to use a different method
        print("\n--- Trying direct session interaction ---")
        try:
            # Try to get the session and see what's in it
            session = await session_service.get_session(
                app_name="test_app",
                user_id=user_id,
                session_id=session_id
            )
            print(f"Session: {session}")
            
            # Try running without any message
            async for event in runner.run_async(
                user_id=user_id,
                session_id=session_id,
                new_message={}
            ):
                print(f"✅ Direct session worked!")
                if hasattr(event, 'content') and event.content:
                    if hasattr(event.content, 'parts'):
                        for part in event.content.parts:
                            if hasattr(part, 'text'):
                                print(f"Response: {part.text}")
                break
        except Exception as e2:
            print(f"❌ Direct session also failed: {e2}")

if __name__ == "__main__":
    asyncio.run(test_session_events())