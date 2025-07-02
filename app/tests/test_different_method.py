"""
Test different methods to interact with the agent
"""

import asyncio
import os
from dotenv import load_dotenv
from google.adk import Agent
from google.adk.sessions import InMemorySessionService
from google.adk import Runner

async def test_different_method():
    """Test different methods to interact with the agent."""
    
    print("=== Testing Different Methods ===")
    
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
    
    await session_service.create_session(
        app_name="test_app",
        user_id=user_id,
        session_id=session_id
    )
    
    test_query = "What is 2+2?"
    
    print(f"\n--- Testing with query: '{test_query}' ---")
    
    # Try different approaches
    approaches = [
        # Approach 1: Try with None as new_message
        ("None message", None),
        
        # Approach 2: Try with empty dict
        ("Empty dict", {}),
        
        # Approach 3: Try with minimal object
        ("Minimal object", type('Content', (), {'parts': [{'text': test_query}]})()),
        
        # Approach 4: Try calling run_async without new_message
        ("No new_message", "NO_MESSAGE"),
    ]
    
    for approach_name, message in approaches:
        print(f"\n--- Approach: {approach_name} ---")
        try:
            if message == "NO_MESSAGE":
                # Try calling without new_message parameter
                async for event in runner.run_async(
                    user_id=user_id,
                    session_id=session_id
                ):
                    print(f"✅ {approach_name} worked!")
                    if hasattr(event, 'content') and event.content:
                        if hasattr(event.content, 'parts'):
                            for part in event.content.parts:
                                if hasattr(part, 'text'):
                                    print(f"Response: {part.text}")
                    break
            else:
                async for event in runner.run_async(
                    user_id=user_id,
                    session_id=session_id,
                    new_message=message
                ):
                    print(f"✅ {approach_name} worked!")
                    if hasattr(event, 'content') and event.content:
                        if hasattr(event.content, 'parts'):
                            for part in event.content.parts:
                                if hasattr(part, 'text'):
                                    print(f"Response: {part.text}")
                    break
        except Exception as e:
            print(f"❌ {approach_name} failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_different_method())