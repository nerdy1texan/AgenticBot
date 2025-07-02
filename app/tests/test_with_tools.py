"""
Test the agent with tools to see if that works better
"""

import asyncio
import os
from dotenv import load_dotenv
from google.adk import Agent
from google.adk.sessions import InMemorySessionService
from google.adk import Runner

async def test_with_tools():
    """Test the agent with tools to see if that works better."""
    
    print("=== Testing Agent with Tools ===")
    
    # Load environment variables
    load_dotenv()
    
    # Setup Gemini
    from chatgpt_agentic_clone.agent import setup_gemini, web_search
    setup_gemini()
    
    # Create an agent with tools
    agent_with_tools = Agent(
        name="agent_with_tools",
        model="gemini-2.0-flash-exp",
        instruction="""You are a helpful assistant with access to web search. 

When users ask questions, answer them directly. If they ask about current information like weather, use the web_search tool to find the answer.

Always respond to the user's actual question.""",
        tools=[web_search],
    )
    
    # Setup
    session_service = InMemorySessionService()
    runner = Runner(
        agent=agent_with_tools,
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
    
    # Test with a weather query that should trigger the tool
    test_query = "What's the weather in Atlanta today?"
    
    print(f"\n--- Testing with query: '{test_query}' ---")
    
    class MinimalContent:
        def __init__(self, text):
            self.parts = [{"text": text}]
    
    try:
        content_obj = MinimalContent(test_query)
        
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
    asyncio.run(test_with_tools())