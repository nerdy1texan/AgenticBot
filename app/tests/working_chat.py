"""
Working chat implementation using Google Generative AI directly
"""

import asyncio
import os
from dotenv import load_dotenv
import google.generativeai as genai

async def working_chat():
    """Working chat implementation using Google Generative AI directly."""
    
    print("=== Working Chat Implementation ===")
    
    # Load environment variables
    load_dotenv()
    
    # Setup Gemini
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GOOGLE_API_KEY not found")
        return
    
    genai.configure(api_key=api_key)
    
    # Create a model
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    # Start a chat
    chat = model.start_chat(history=[])
    
    print("\n🤖 Working Chat Bot Ready!")
    print("Type 'exit' to quit.")
    print("-" * 50)
    
    while True:
        try:
            # Get user input
            user_input = input("\n💬 You: ").strip()
            
            if user_input.lower() in ["exit", "quit", "bye"]:
                print("\n👋 Goodbye!")
                break
            
            if not user_input:
                continue
            
            # Send message to the model
            print("\n🤖 Assistant: ", end="", flush=True)
            
            response = chat.send_message(user_input)
            
            # Print the response
            print(response.text)
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(working_chat())