"""
Final approach - try to fix the message passing issue
"""

import asyncio
import os
from dotenv import load_dotenv
from google.adk import Agent
from google.adk.sessions import InMemorySessionService
from google.adk import Runner

async def test_final_approach():
    """Final approach to fix the message passing issue."""
    
    print("=== Final Approach ===")
    
    # Load environment variables
    load_dotenv()
    
    # Setup Gemini
    from chatgpt_agentic_clone.agent import setup_gemini
    setup_gemini()
    
    # Create an agent with a very specific instruction
    simple_agent = Agent(
        name="simple_agent",
        model="gemini-2.0-flash-exp",
        instruction="""You are a helpful assistant. 

IMPORTANT: When you receive a user message, respond to it directly. Do not ask for System Instructions or wait for further input.

If someone asks "What is 2+2?", respond with "2+2 equals 4."
If someone asks about weather, tell them you would need to search for that information.
If someone says "Hello", respond with "Hello! How can I help you today?"

Always respond to the user's actual question or statement.""",
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
    
    # Use the MinimalContent object that we know works
    class MinimalContent:
        def __init__(self, text):
            self.parts = [{"text": text}]
    
    try:
        content_obj = MinimalContent(test_query)
        
        # Try to debug what's happening
        print(f"Sending content object: {content_obj}")
        print(f"Content object parts: {content_obj.parts}")
        
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=content_obj
        ):
            print(f"✅ Agent responded!")
            # Extract the text content
            if hasattr(event, 'content') and event.content:
                if hasattr(event.content, 'parts'):
                    for part in event.content.parts:
                        if hasattr(part, 'text'):
                            print(f"Response: {part.text}")
            break
    except Exception as e:
        print(f"❌ Failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_final_approach())