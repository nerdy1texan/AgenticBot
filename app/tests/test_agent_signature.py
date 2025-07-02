"""
Test to understand the agent's run_async method signature
"""

import asyncio
import os
import inspect
from dotenv import load_dotenv
from google.adk import Agent

async def test_agent_signature():
    """Test to understand the agent's run_async method signature."""
    
    print("=== Testing Agent run_async Signature ===")
    
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
    
    # Check the run_async method signature
    sig = inspect.signature(simple_agent.run_async)
    print(f"run_async signature: {sig}")
    
    # Check the parameters
    for param_name, param in sig.parameters.items():
        print(f"Parameter: {param_name} = {param.default} (type: {param.annotation})")
    
    # Try to understand what the first parameter expects
    first_param = list(sig.parameters.keys())[0]
    first_param_type = sig.parameters[first_param].annotation
    
    print(f"\nFirst parameter: {first_param} (type: {first_param_type})")
    
    # Try to create an object of the expected type
    if first_param_type != inspect.Parameter.empty:
        print(f"Expected type: {first_param_type}")
        
        # Try to import the type if it's a string
        if isinstance(first_param_type, str):
            try:
                # Try to import the type
                module_name, class_name = first_param_type.rsplit('.', 1)
                module = __import__(module_name, fromlist=[class_name])
                expected_type = getattr(module, class_name)
                print(f"Imported type: {expected_type}")
                
                # Try to create an instance
                try:
                    instance = expected_type()
                    print(f"Created instance: {instance}")
                except Exception as e:
                    print(f"Could not create instance: {e}")
            except Exception as e:
                print(f"Could not import type: {e}")

if __name__ == "__main__":
    asyncio.run(test_agent_signature())