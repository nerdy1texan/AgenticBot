"""
Test model names and find the exact message format
"""

import asyncio
from google.adk import Runner, Agent
from google.adk.sessions import InMemorySessionService

async def test_models_and_formats():
    """Test different model names and message formats."""
    
    print("=== Testing Models and Message Formats ===")
    
    # Test different model names
    model_names = [
        "models/gemini-2.0-flash-exp",
        "models/gemini-2.0-flash",
        "models/gemini-1.5-flash",
        "models/gemini-1.5-pro",
        "gemini-2.0-flash-exp",
        "gemini-2.0-flash",
        "gemini-1.5-flash",
        "gemini-1.5-pro"
    ]
    
    # Test with a simple agent first
    for model_name in model_names:
        print(f"\n--- Testing model: {model_name} ---")
        try:
            # Create a simple test agent
            test_agent = Agent(
                name="test_agent",
                model=model_name,
                instruction="You are a helpful assistant. Just respond with 'Hello from test agent'."
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
            
            # Test with empty dict (which got furthest)
            try:
                async for event in runner.run_async(
                    user_id="test_user",
                    session_id="test_session", 
                    new_message={}
                ):
                    print(f"✅ Model {model_name} worked with empty dict! Event: {event}")
                    break
            except Exception as e:
                print(f"❌ Model {model_name} failed with empty dict: {e}")
                
        except Exception as e:
            print(f"❌ Could not create agent with model {model_name}: {e}")

if __name__ == "__main__":
    asyncio.run(test_models_and_formats())