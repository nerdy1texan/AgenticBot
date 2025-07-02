"""
Test alternative approaches to interact with the agent
"""

import asyncio
import os
from dotenv import load_dotenv
from google.adk import Agent
from google.adk.sessions import InMemorySessionService
from google.adk import Runner

async def test_alternative_approach():
    """Test alternative approaches to interact with the agent."""
    
    print("=== Testing Alternative Approaches ===")
    
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
    await session_service.create_session(
        app_name="test_app",
        user_id="test_user",
        session_id="test_session"
    )
    
    test_query = "Hello, how are you?"
    
    print(f"\n--- Testing with query: '{test_query}' ---")
    
    # Try creating a minimal object with only the required attributes
    class MinimalContent:
        def __init__(self, text):
            # Only include the parts attribute that the API seems to expect
            self.parts = [{"text": text}]
            # Don't include any other attributes that might cause validation errors
    
    try:
        content_obj = MinimalContent(test_query)
        print(f"Content object: {content_obj}")
        print(f"Content object attributes: {dir(content_obj)}")
        
        async for event in runner.run_async(
            user_id="test_user",
            session_id="test_session",
            new_message=content_obj
        ):
            print(f"✅ MinimalContent worked!")
            # Extract the text content
            if hasattr(event, 'content') and event.content:
                if hasattr(event.content, 'parts'):
                    for part in event.content.parts:
                        if hasattr(part, 'text'):
                            print(f"Response: {part.text}")
            break
    except Exception as e:
        print(f"❌ MinimalContent failed: {e}")
        
        # Try to understand what the error is telling us
        if "user_content" in str(e):
            print("The error suggests the API expects a user_content field")
            # Try with a different structure
            try:
                class UserContentWrapper:
                    def __init__(self, text):
                        self.user_content = {"text": text}
                
                wrapper_obj = UserContentWrapper(test_query)
                async for event in runner.run_async(
                    user_id="test_user",
                    session_id="test_session",
                    new_message=wrapper_obj
                ):
                    print(f"✅ UserContentWrapper worked!")
                    break
            except Exception as e2:
                print(f"❌ UserContentWrapper also failed: {e2}")

if __name__ == "__main__":
    asyncio.run(test_alternative_approach())