"""
Test using the agent's run_async method directly
"""

import asyncio
import os
from dotenv import load_dotenv
from google.adk import Agent

async def test_agent_run_async():
    """Test using the agent's run_async method directly."""
    
    print("=== Testing Agent run_async Method ===")
    
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
    
    test_query = "What is 2+2?"
    
    print(f"\n--- Testing with query: '{test_query}' ---")
    
    # Try using the agent's run_async method directly
    try:
        print("Calling agent.run_async directly...")
        async for event in simple_agent.run_async(test_query):
            print(f"✅ Agent run_async worked!")
            print(f"Event: {event}")
            
            # Extract the text content
            if hasattr(event, 'content') and event.content:
                if hasattr(event.content, 'parts'):
                    for part in event.content.parts:
                        if hasattr(part, 'text'):
                            print(f"Response: {part.text}")
            break
    except Exception as e:
        print(f"❌ Agent run_async failed: {e}")
        
        # Try with different parameter formats
        print("\n--- Trying different parameter formats ---")
        
        formats = [
            ("String", test_query),
            ("Dict", {"query": test_query}),
            ("List", [test_query]),
        ]
        
        for format_name, message in formats:
            print(f"\n--- Format: {format_name} ---")
            try:
                async for event in simple_agent.run_async(message):
                    print(f"✅ {format_name} format worked!")
                    if hasattr(event, 'content') and event.content:
                        if hasattr(event.content, 'parts'):
                            for part in event.content.parts:
                                if hasattr(part, 'text'):
                                    print(f"Response: {part.text}")
                    break
            except Exception as e2:
                print(f"❌ {format_name} format failed: {e2}")

if __name__ == "__main__":
    asyncio.run(test_agent_run_async())