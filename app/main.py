"""
AgenticBot - ChatGPT Clone with Google Generative AI
A powerful AI assistant with web search, content extraction, deep research, and image generation capabilities.
"""

import os
import asyncio
import base64
from typing import Dict, Any
from dotenv import load_dotenv
import google.generativeai as genai
from chatgpt_agentic_clone.agent import web_search, scrape_webpage, deep_research, generate_image, setup_gemini

# Load environment variables
load_dotenv()

# Setup Gemini API key
setup_gemini()

# Application configuration
APP_NAME = "chatgpt_agentic_clone_app"
USER_ID = "user_1"
SESSION_ID = "session_001"

def check_api_keys():
    """Check if required API keys are set."""
    required_keys = ["GOOGLE_API_KEY", "FIRECRAWL_API_KEY"]
    missing_keys = []
    
    for key in required_keys:
        if not os.getenv(key):
            missing_keys.append(key)
    
    if missing_keys:
        print("❌ Missing required API keys:")
        for key in missing_keys:
            print(f"   - {key}")
        print("\nPlease set these environment variables in your .env file.")
        print("See the README for instructions on getting API keys.")
        return False
    
    print("✅ All API keys are configured!")
    return True

def save_image_data(image_data: str, filename: str) -> str:
    """Save base64 image data to a file."""
    try:
        # Decode base64 data
        decoded_data = base64.b64decode(image_data)
        
        # Create images directory if it doesn't exist
        os.makedirs("images", exist_ok=True)
        
        # Save the image
        filepath = os.path.join("images", filename)
        with open(filepath, "wb") as f:
            f.write(decoded_data)
        
        return filepath
    except Exception as e:
        print(f"Error saving image: {e}")
        return None

async def process_user_query(user_input: str, chat) -> Dict[str, Any]:
    """Process user query and return response with any additional data."""
    
    # Check for tool usage
    if user_input.lower().startswith("search for"):
        # Web search
        query = user_input[11:]  # Remove "search for "
        print(f"\n🔍 Searching for: {query}")
        result = web_search(query)
        
        if result["status"] == "success":
            response_text = f"Search results for '{query}':\n\n"
            for i, item in enumerate(result["results"][:5], 1):
                response_text += f"{i}. {item['title']}\n"
                response_text += f"   URL: {item['url']}\n"
                response_text += f"   {item['description'][:100]}...\n\n"
        else:
            response_text = f"Search failed: {result['error_message']}"
        
        return {"text": response_text, "image_data": None, "image_filename": None}
        
    elif user_input.lower().startswith("scrape "):
        # Web scraping
        url = user_input[7:]  # Remove "scrape "
        print(f"\n📄 Scraping: {url}")
        result = scrape_webpage(url)
        
        if result["status"] == "success":
            content = result["content"][:500] + "..." if len(result["content"]) > 500 else result["content"]
            response_text = f"Content from {url}:\n\n{content}"
        else:
            response_text = f"Scraping failed: {result['error_message']}"
        
        return {"text": response_text, "image_data": None, "image_filename": None}
        
    elif user_input.lower().startswith("research "):
        # Deep research
        topic = user_input[9:]  # Remove "research "
        print(f"\n🔬 Researching: {topic}")
        result = deep_research(topic)
        
        if result["status"] == "success":
            response_text = f"Research on '{topic}':\n\n{result['summary']}\n\nSources: {result['total_sources']}"
        else:
            response_text = f"Research failed: {result['error_message']}"
        
        return {"text": response_text, "image_data": None, "image_filename": None}
        
    elif user_input.lower().startswith("generate image"):
        # Image generation
        prompt = user_input[15:]  # Remove "generate image "
        print(f"\n🎨 Generating image: {prompt}")
        result = generate_image(prompt)
        
        if result["status"] == "success":
            response_text = f"Image generated successfully! Prompt: {prompt}"
            # Save the image
            filename = f"generated_image_{len(os.listdir('images')) if os.path.exists('images') else 0}.png"
            image_path = save_image_data(result["image_data"], filename)
            return {"text": response_text, "image_data": result["image_data"], "image_filename": image_path}
        else:
            response_text = f"Image generation failed: {result['error_message']}"
            return {"text": response_text, "image_data": None, "image_filename": None}
            
    elif any(word in user_input.lower() for word in ["weather", "current", "latest", "news", "today's", "now", "stock", "price"]):
        # Auto-detect current information requests
        print(f"\n🔍 Detected current information request, searching for: {user_input}")
        result = web_search(user_input)
        
        if result["status"] == "success":
            response_text = f"Current information for '{user_input}':\n\n"
            for i, item in enumerate(result["results"][:3], 1):
                response_text += f"{i}. {item['title']}\n"
                response_text += f"   URL: {item['url']}\n"
                response_text += f"   {item['description'][:150]}...\n\n"
        else:
            response_text = f"Search failed: {result['error_message']}"
        
        return {"text": response_text, "image_data": None, "image_filename": None}
        
    else:
        # Regular chat
        print("\n🤖 Processing with AI...")
        response = chat.send_message(user_input)
        return {"text": response.text, "image_data": None, "image_filename": None}

async def interactive_session():
    """Run an interactive session with the AI assistant."""
    
    # Create a model and start chat
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    chat = model.start_chat(history=[])
    
    print("\n" + "="*60)
    print("🚀 Welcome to AgenticBot - ChatGPT Clone with AI")
    print("="*60)
    print("This AI assistant can:")
    print("• Answer general questions using built-in knowledge")
    print("• Search the web for current information")
    print("• Extract content from web pages")
    print("• Conduct deep research on complex topics")
    print("• Generate images from text descriptions")
    print("\nSpecial commands:")
    print("• 'search for [query]' - Web search")
    print("• 'scrape [url]' - Extract web content")
    print("• 'research [topic]' - Deep research")
    print("• 'generate image [description]' - Create images")
    print("\nType 'exit' or 'quit' to end the session.")
    print("Type 'help' for example queries.")
    print("-" * 60)
    
    while True:
        try:
            # Get user input
            user_input = input("\n💬 You: ").strip()
            
            if user_input.lower() in ["exit", "quit", "bye"]:
                print("\n👋 Thanks for using AgenticBot! Goodbye!")
                break
            
            if user_input.lower() == "help":
                print("\n📋 Example queries you can try:")
                print("• General: 'Who was Marie Curie?'")
                print("• Weather: 'What's the weather in London right now?'")
                print("• Web Search: 'search for latest AI developments'")
                print("• Web Extraction: 'scrape https://github.com/trending'")
                print("• Deep Research: 'research quantum computing advances'")
                print("• Image Generation: 'generate image of a robot playing piano'")
                continue
            
            if not user_input:
                print("Please enter a question or command.")
                continue
                
            # Process the user input
            result = await process_user_query(user_input, chat)
            
            # Display the response
            print(f"\n🤖 Assistant: {result['text']}")
            
            # Handle any special content like images
            if result.get('image_filename'):
                print(f"📁 Image saved to: {result['image_filename']}")
                
        except KeyboardInterrupt:
            print("\n\n👋 Session interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try again or type 'exit' to quit.")

async def main():
    """Main function to run the application."""
    print("🔍 Checking API keys...")
    
    # Check if API keys are configured
    if not check_api_keys():
        print("\n📝 To get started:")
        print("1. Create a .env file in the app directory")
        print("2. Add your API keys:")
        print("   GOOGLE_API_KEY=your_google_api_key_here")
        print("   FIRECRAWL_API_KEY=your_firecrawl_api_key_here")
        return
    
    try:
        print("🏗️  Initializing AgenticBot...")
        print("✅ AgenticBot initialized successfully!")
        
        # Start the interactive session
        await interactive_session()
        
    except Exception as e:
        print(f"❌ Failed to initialize AgenticBot: {e}")
        print("Please check your API keys and internet connection.")

if __name__ == "__main__":
    asyncio.run(main()) 