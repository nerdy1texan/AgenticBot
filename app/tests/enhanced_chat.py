"""
Enhanced chat with tools integration
"""

import asyncio
import os
from dotenv import load_dotenv
import google.generativeai as genai
from chatgpt_agentic_clone.agent import web_search, scrape_webpage, deep_research, generate_image, setup_gemini

async def enhanced_chat():
    """Enhanced chat with tools integration."""
    
    print("=== Enhanced Chat with Tools ===")
    
    # Load environment variables
    load_dotenv()
    
    # Setup Gemini
    setup_gemini()
    
    # Create a model
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    # Start a chat
    chat = model.start_chat(history=[])
    
    print("\n🤖 Enhanced Chat Bot Ready!")
    print("Capabilities:")
    print("• General questions and conversation")
    print("• Web search (try: 'search for latest AI news')")
    print("• Web scraping (try: 'scrape https://github.com/trending')")
    print("• Deep research (try: 'research quantum computing')")
    print("• Image generation (try: 'generate image of a robot')")
    print("Type 'exit' to quit.")
    print("-" * 60)
    
    while True:
        try:
            # Get user input
            user_input = input("\n💬 You: ").strip()
            
            if user_input.lower() in ["exit", "quit", "bye"]:
                print("\n👋 Goodbye!")
                break
            
            if not user_input:
                continue
            
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
                
                print(f"🤖 Assistant: {response_text}")
                
            elif user_input.lower().startswith("scrape "):
                # Web scraping
                url = user_input[7:]  # Remove "scrape "
                print(f"\n�� Scraping: {url}")
                result = scrape_webpage(url)
                
                if result["status"] == "success":
                    content = result["content"][:500] + "..." if len(result["content"]) > 500 else result["content"]
                    response_text = f"Content from {url}:\n\n{content}"
                else:
                    response_text = f"Scraping failed: {result['error_message']}"
                
                print(f"🤖 Assistant: {response_text}")
                
            elif user_input.lower().startswith("research "):
                # Deep research
                topic = user_input[9:]  # Remove "research "
                print(f"\n🔬 Researching: {topic}")
                result = deep_research(topic)
                
                if result["status"] == "success":
                    response_text = f"Research on '{topic}':\n\n{result['summary']}\n\nSources: {result['total_sources']}"
                else:
                    response_text = f"Research failed: {result['error_message']}"
                
                print(f"🤖 Assistant: {response_text}")
                
            elif user_input.lower().startswith("generate image"):
                # Image generation
                prompt = user_input[15:]  # Remove "generate image "
                print(f"\n🎨 Generating image: {prompt}")
                result = generate_image(prompt)
                
                if result["status"] == "success":
                    response_text = f"Image generated successfully! Prompt: {prompt}"
                    # You could save the image here if needed
                else:
                    response_text = f"Image generation failed: {result['error_message']}"
                
                print(f"🤖 Assistant: {response_text}")
                
            elif any(word in user_input.lower() for word in ["weather", "current", "latest", "news", "today's", "now"]):
                # Auto-detect weather/current info requests
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
                
                print(f"🤖 Assistant: {response_text}")
                
            else:
                # Regular chat
                print("\n🤖 Assistant: ", end="", flush=True)
                response = chat.send_message(user_input)
                print(response.text)
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(enhanced_chat())