#!/usr/bin/env python3
"""
Test script for AgenticBot image generation functionality
"""

import sys
import os
from dotenv import load_dotenv

# Add the app directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Load environment variables
load_dotenv()

from chatgpt_agentic_clone.agent import generate_image, setup_gemini

def test_image_generation():
    print("🧪 Testing AgenticBot Image Generation")
    print("=" * 50)
    
    # Test prompts
    test_prompts = [
        "a cute robot",
        "a friendly robot astronaut on the moon",
        "a simple drawing of a cat",
        "abstract art with colorful shapes"
    ]
    
    print(f"📊 Running {len(test_prompts)} test cases...")
    print()
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"🔍 Test {i}/{len(test_prompts)}: '{prompt}'")
        print("-" * 30)
        
        try:
            result = generate_image(prompt)
            
            print(f"Status: {result.get('status', 'unknown')}")
            print(f"Message: {result.get('message', 'No message')}")
            
            if result.get('error_message'):
                print(f"Error: {result['error_message']}")
            
            if result.get('safe_prompt'):
                print(f"Safe prompt: {result['safe_prompt']}")
            
            if result.get('image_data'):
                print(f"Image data length: {len(result['image_data'])} characters")
                print("✅ Image data received!")
            else:
                print("❌ No image data in response")
                
            if result.get('suggestion'):
                print(f"Suggestion: {result['suggestion']}")
                
        except Exception as e:
            print(f"❌ Exception occurred: {e}")
        
        print()
    
    print("🎉 Test completed!")

def test_basic_setup():
    print("🔧 Testing basic setup...")
    
    try:
        setup_gemini()
        print("✅ Gemini setup successful")
    except Exception as e:
        print(f"❌ Gemini setup failed: {e}")
        return False
    
    # Test environment variables
    google_key = os.getenv("GOOGLE_API_KEY")
    if google_key:
        print(f"✅ Google API key found (length: {len(google_key)})")
    else:
        print("❌ Google API key not found")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 Starting AgenticBot Image Generation Tests")
    print()
    
    if test_basic_setup():
        print()
        test_image_generation()
    else:
        print("❌ Basic setup failed. Please check your configuration.") 