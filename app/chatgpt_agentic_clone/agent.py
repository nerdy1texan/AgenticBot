"""
AgenticBot: A ChatGPT-like clone using Google ADK
Based on the Firecrawl tutorial for multi-agent systems
"""

import os
import base64
from typing import Dict, Optional, Any
from firecrawl import FirecrawlApp
import google.generativeai as genai
from google.adk import Agent

# Load environment variables from .env file if it exists
def load_env_file():
    """Load environment variables from .env file."""
    # Check current directory first, then parent directory
    env_paths = ['.env', '../.env']
    
    for env_path in env_paths:
        if os.path.exists(env_path):
            try:
                with open(env_path, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            # Remove quotes if present
                            value = value.strip().strip("'\"")
                            os.environ[key.strip()] = value
                break  # Stop after finding the first .env file
            except Exception:
                pass  # Silently ignore errors

# Load .env file when module is imported
load_env_file()

# Model configurations
MODEL_GEMINI_2_0_FLASH = "gemini-2.0-flash-exp"
GEMINI_IMAGE_GEN_MODEL = "imagen-3.0-generate-001"

# Initialize Firecrawl (API key will be loaded from environment)
def get_firecrawl_app():
    """Get Firecrawl app instance with API key from environment."""
    api_key = os.getenv("FIRECRAWL_API_KEY")
    if not api_key:
        raise ValueError("FIRECRAWL_API_KEY environment variable is required")
    return FirecrawlApp(api_key=api_key)

# Initialize Gemini (API key will be loaded from environment)
def setup_gemini():
    """Setup Gemini with API key from environment."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is required")
    genai.configure(api_key=api_key)

# Tool Functions
def web_search(query: str) -> Dict:
    """Searches the web for current information using Firecrawl."""
    print(f"--- Tool: web_search called for query: {query} ---")
    
    try:
        app = get_firecrawl_app()
        # THE SEARCH HAPPENS IN THIS LINE
        result = app.search(query, limit=10)
        
        if result.success:
            formatted_results = []
            for item in result.data:
                formatted_results.append({
                    "title": item.get("title", "No title"),
                    "url": item.get("url", "No URL"),
                    "description": item.get("description", "No description"),
                })
                
            return {"status": "success", "results": formatted_results}
        else:
            return {
                "status": "error",
                "error_message": f"Search failed: {result.error or 'Unknown error'}",
            }
            
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error during web search: {str(e)}",
        }

def scrape_webpage(url: str, extract_format: str = "markdown") -> Dict:
    """Scrapes content from a webpage using Firecrawl."""
    print(f"--- Tool: scrape_webpage called for URL: {url} ---")
    
    try:
        app = get_firecrawl_app()
        result = app.scrape_url(url, formats=[extract_format])
        
        if result.success and result.data:
            content = result.data.get(extract_format, "")
            metadata = result.data.get("metadata", {})
            
            return {
                "status": "success",
                "content": content,
                "metadata": {
                    "title": metadata.get("title", "No title"),
                    "description": metadata.get("description", "No description"),
                    "url": url,
                    "format": extract_format
                }
            }
        else:
            return {
                "status": "error",
                "error_message": f"Scraping failed: {result.error if hasattr(result, 'error') else 'Unknown error'}",
            }
            
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error scraping webpage: {str(e)}",
        }

def deep_research(topic: str, max_depth: int = 5, time_limit: int = 180) -> Dict:
    """Performs comprehensive research using Firecrawl."""
    print(f"--- Tool: deep_research called for topic: {topic} ---")
    
    try:
        app = get_firecrawl_app()
        result = app.deep_research(topic, max_depth=max_depth, time_limit=time_limit)
        
        if result.success and result.data:
            research_data = result.data
            
            # Extract research findings
            findings = research_data.get("findings", [])
            sources = research_data.get("sources", [])
            summary = research_data.get("summary", "No summary available")
            
            return {
                "status": "success",
                "summary": summary,
                "findings": findings,
                "sources": sources,
                "total_sources": len(sources)
            }
        else:
            return {
                "status": "error",
                "error_message": f"Deep research failed: {result.error if hasattr(result, 'error') else 'Unknown error'}",
            }
            
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error during deep research: {str(e)}",
        }

def generate_image(prompt: str, model: str = GEMINI_IMAGE_GEN_MODEL) -> Dict:
    """Generates an image using Gemini's image generation models."""
    print(f"--- Tool: generate_image called for prompt: {prompt} ---")
    
    try:
        setup_gemini()
        
        # For image generation, we need to use the imagen model directly
        # Let's try a safer, family-friendly prompt
        safe_prompt = f"A family-friendly, wholesome illustration of: {prompt}. Digital art style, appropriate for all ages."
        
        try:
            # Try using the Imagen model directly
            import google.generativeai as genai
            
            # Create the model for image generation
            model_instance = genai.GenerativeModel('gemini-2.0-flash-exp')
            
            # Try generating with the text model first to get a safe description
            safe_description_response = model_instance.generate_content(
                f"Create a safe, family-friendly, detailed description for generating an image of: {prompt}. "
                f"Make it appropriate for all ages, avoiding any potentially inappropriate content. "
                f"Focus on wholesome, creative, and artistic elements."
            )
            
            if safe_description_response and safe_description_response.text:
                safe_description = safe_description_response.text
                print(f"Generated safe description: {safe_description}")
                
                # Now try image generation with the safer description
                # Note: This might not work directly as Gemini text models don't generate images
                # This is a placeholder for when proper image generation is available
                return {
                    "status": "partial_success",
                    "message": f"Image generation is being processed. Description: {safe_description}",
                    "safe_prompt": safe_description,
                    "original_prompt": prompt,
                    "note": "Image generation capability is currently limited. The system has created a safe description that could be used with image generation services."
                }
            
        except Exception as text_error:
            print(f"Text model approach failed: {text_error}")
        
        # Alternative approach: Try direct image generation (this might not work with current setup)
        try:
            # Initialize the specific image generation model
            generation_model = genai.GenerativeModel(model)
            
            # Generate the image with safety-first prompt
            response = generation_model.generate_content(safe_prompt)
            
            if response and hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]
                if hasattr(candidate, 'content') and candidate.content.parts:
                    for part in candidate.content.parts:
                        if hasattr(part, 'inline_data'):
                            # Extract image data
                            image_data = part.inline_data.data
                            mime_type = part.inline_data.mime_type
                            
                            return {
                                "status": "success",
                                "image_data": image_data,
                                "mime_type": mime_type,
                                "prompt": prompt,
                                "safe_prompt": safe_prompt,
                                "message": "Image generated successfully"
                            }
                
                # If no image data but response exists, return the text response
                if hasattr(candidate, 'content') and candidate.content.parts:
                    text_content = ""
                    for part in candidate.content.parts:
                        if hasattr(part, 'text'):
                            text_content += part.text
                    
                    if text_content:
                        return {
                            "status": "text_response",
                            "message": text_content,
                            "prompt": prompt,
                            "safe_prompt": safe_prompt,
                            "note": "The model provided a text response instead of generating an image."
                        }
        
        except Exception as image_error:
            print(f"Direct image generation failed: {image_error}")
        
        return {
            "status": "error",
            "error_message": "Image generation is not currently available with this model configuration. The model may have safety restrictions or the image generation feature may not be enabled.",
            "prompt": prompt,
            "suggestion": "Try a different prompt or use an external image generation service."
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error generating image: {str(e)}",
            "prompt": prompt
        }

# Note: Content filtering callback removed for compatibility with current ADK version
# Basic safety will be handled through agent instructions instead

# Specialized Agents
search_agent = Agent(
    name="search_agent",
    model=MODEL_GEMINI_2_0_FLASH,
    instruction="You are a web search specialist. Your role is to search for current information on the web "
    "when users ask about recent events, current facts, or real-time data. "
    "Use the 'web_search' tool to find relevant information, then synthesize and present it clearly. "
    "Always cite your sources by including the URLs. "
    "If the search returns an error, explain the issue to the user and suggest alternatives. "
    "IMPORTANT: Do not assist with harmful, illegal, or unethical requests.",
    tools=[web_search],
)

web_extraction_agent = Agent(
    name="web_extraction_agent",
    model=MODEL_GEMINI_2_0_FLASH,
    instruction="You are a web content extraction specialist. Your role is to extract and analyze content "
    "from specific URLs when users provide them. "
    "Use the 'scrape_webpage' tool to get content from the provided URLs. "
    "Present the extracted information in a clear, structured format. "
    "If extraction fails, explain the issue and suggest alternatives. "
    "Always include the source URL in your response.",
    tools=[scrape_webpage],
)

research_agent = Agent(
    name="research_agent",
    model=MODEL_GEMINI_2_0_FLASH,
    instruction="You are a deep research specialist. Your role is to conduct comprehensive, multi-source "
    "research on complex topics that require analysis from multiple perspectives. "
    "Use the 'deep_research' tool to gather information from various sources and synthesize findings. "
    "Present your research in a structured format with key findings, analysis, and source citations. "
    "If research fails, explain the limitations and provide what information you can.",
    tools=[deep_research],
)

image_generation_agent = Agent(
    name="image_generation_agent",
    model=MODEL_GEMINI_2_0_FLASH,
    instruction="You are an image generation specialist. Your role is to create images based on user descriptions. "
    "Use the 'generate_image' tool to create images from text prompts. "
    "When generating images, be creative and detailed in your interpretation of the user's request. "
    "If image generation fails, explain the issue and suggest modifications to the prompt. "
    "Always describe what you've generated for the user.",
    tools=[generate_image],
)

# Root Agent (Main Coordinator)
root_agent = Agent(
    name="chatgpt_agentic_clone",
    model=MODEL_GEMINI_2_0_FLASH,
    instruction="You are a versatile AI assistant similar to ChatGPT. Your primary job is to be helpful, harmless, and honest. "
    "You have several specialized capabilities through your sub-agents: "
    "1. 'search_agent': Use for current events, facts, weather, sports scores, or any real-time information. "
    "2. 'web_extraction_agent': Use when asked to extract or analyze content from specific URLs. "
    "3. 'research_agent': Use for in-depth research on complex topics requiring analysis of multiple sources. "
    "4. 'image_generation_agent': Use when asked to create or generate images. "
    "Important guidelines: "
    "- For general knowledge queries, respond directly using your built-in knowledge. "
    "- For current events or real-time information, delegate to 'search_agent'. "
    "- If asked to get content from a specific URL, delegate to 'web_extraction_agent'. "
    "- If asked for deep research with multiple sources, delegate to 'research_agent'. "
    "- If asked to create or generate an image, delegate to 'image_generation_agent'. "
    "- Be conversational, helpful, and concise. "
    "- NEVER assist with harmful, illegal, unethical, or dangerous requests. "
    "- Refuse to help with anything that could cause harm to people or property. "
    "- Admit when you don't know something rather than making up information.",
    sub_agents=[
        search_agent,
        web_extraction_agent,
        research_agent,
        image_generation_agent,
    ],
) 