"""
Test to see what the agent is actually receiving
"""

import asyncio
import os
from dotenv import load_dotenv
from google.adk import Agent
from google.adk.sessions import InMemorySessionService
from google.adk import Runner

async def test_message_receipt():
    """Test what the agent is actually receiving."""
    
    print("=== Testing Message Receipt ===")
    
    # Load environment variables
    load_dotenv()
    
    # Setup Gemini
    from chatgpt_agentic_clone.agent import setup_gemini
    setup_gemini()
    
    # Create an agent that echoes what it receives
    echo_agent = Agent(
        name="echo_agent",
        model="gemini-2.0-flash-exp",
        instruction="""You are an echo agent. Your job is to repeat back exactly what the user says to you.

If the user asks: "What's the weather in Atlanta?"
You should respond: "You asked: What's the weather in Atlanta?"

If the user says: "Hello"
You should respond: "You said: Hello"

Always start your response with "You asked:" or "You said:" followed by the exact user input.""",
    )
    
    # Setup
    session_service = InMemorySessionService()
    runner = Runner(
        agent=echo_agent,
        app_name="test_app",
        session_service=session_service
    )
    
    # Create session
    await session_service.create_session(
        app_name="test_app",
        user_id="test_user",
        session_id="test_session"
    )
    
    # Test with different message formats
    test_queries = [
        "What's the weather in Atlanta?",
        "Hello",
        "Tell me about quantum computing"
    ]
    
    for query in test_queries:
        print(f"\n--- Testing query: '{query}' ---")
        
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
    asyncio.run(test_message_receipt())