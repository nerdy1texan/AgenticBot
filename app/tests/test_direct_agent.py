"""
Test interacting with the agent directly
"""

import asyncio
import os
from dotenv import load_dotenv
from google.adk import Agent
from google.adk.sessions import InMemorySessionService
from google.adk import Runner

async def test_direct_agent():
    """Test interacting with the agent directly."""
    
    print("=== Testing Direct Agent Interaction ===")
    
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
    
    print(f"Agent created: {simple_agent}")
    print(f"Agent name: {simple_agent.name}")
    print(f"Agent model: {simple_agent.model}")
    print(f"Agent instruction: {simple_agent.instruction}")
    
    # Try to see if there are any other methods on the agent
    agent_methods = [attr for attr in dir(simple_agent) if not attr.startswith('_')]
    print(f"Agent methods: {agent_methods}")
    
    # Try to see if we can call the agent directly
    try:
        # Check if the agent has a run method
        if hasattr(simple_agent, 'run'):
            print("Agent has run method")
            # Try calling it
            result = await simple_agent.run("What is 2+2?")
            print(f"Direct run result: {result}")
        else:
            print("Agent does not have run method")
    except Exception as e:
        print(f"Direct run failed: {e}")
    
    # Try to see if we can use the agent with a different approach
    try:
        # Check if the agent has an invoke method
        if hasattr(simple_agent, 'invoke'):
            print("Agent has invoke method")
            # Try calling it
            result = await simple_agent.invoke("What is 2+2?")
            print(f"Direct invoke result: {result}")
        else:
            print("Agent does not have invoke method")
    except Exception as e:
        print(f"Direct invoke failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_direct_agent())