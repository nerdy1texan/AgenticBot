"""
Test the runner.run_async API to understand the correct parameters
"""

import asyncio
import inspect
from google.adk import Runner, Agent
from google.adk.sessions import InMemorySessionService

async def test_runner_api():
    """Test the runner API to understand correct parameters."""
    
    print("=== Testing Runner API ===")
    
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
    
    # Check the method signature
    sig = inspect.signature(runner.run_async)
    print(f"run_async signature: {sig}")
    
    # Check the parameters
    for param_name, param in sig.parameters.items():
        print(f"Parameter: {param_name} = {param.default} (type: {param.annotation})")
    
    # Try different ways to call it
    test_query = "Hello, how are you?"
    
    print(f"\n--- Testing different parameter combinations ---")
    
    # Test 1: Try with user_input parameter
    try:
        async for event in runner.run_async(
            user_id="test_user",
            session_id="test_session",
            user_input=test_query
        ):
            print(f"✅ user_input parameter worked!")
            break
    except Exception as e:
        print(f"❌ user_input failed: {e}")
    
    # Test 2: Try with query parameter
    try:
        async for event in runner.run_async(
            user_id="test_user",
            session_id="test_session",
            query=test_query
        ):
            print(f"✅ query parameter worked!")
            break
    except Exception as e:
        print(f"❌ query failed: {e}")
    
    # Test 3: Try with input parameter
    try:
        async for event in runner.run_async(
            user_id="test_user",
            session_id="test_session",
            input=test_query
        ):
            print(f"✅ input parameter worked!")
            break
    except Exception as e:
        print(f"❌ input failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_runner_api())