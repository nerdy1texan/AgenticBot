#!/usr/bin/env python3
"""
Test script for finding prompts that generate actual images
Focus on simple, safe prompts that are likely to bypass safety filtering
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from chatgpt_agentic_clone.agent import generate_image

def test_image_prompts():
    """Test various prompts to find ones that generate actual images"""
    
    print("🎨 Testing Image Generation with Safe Prompts")
    print("=" * 60)
    
    # Test prompts that are more likely to generate actual images
    test_prompts = [
        "abstract blue and yellow swirls",
        "simple red circle on white background",
        "green and purple geometric pattern",
        "orange sunset over calm water",
        "white clouds in blue sky",
        "colorful rainbow gradient",
        "simple flower with five petals",
        "mountain landscape silhouette",
        "abstract art with circles and squares",
        "peaceful forest scene"
    ]
    
    successful_prompts = []
    text_prompts = []
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n🔍 Test {i}/{len(test_prompts)}: '{prompt}'")
        print("-" * 40)
        
        try:
            # Call the generate_image function directly
            result = generate_image(prompt)
            
            if result['status'] == 'success':
                print("✅ SUCCESS: Actual image generated!")
                successful_prompts.append(prompt)
            elif result['status'] == 'partial_success':
                print("📝 TEXT RESPONSE: Got description instead of image")
                text_prompts.append(prompt)
            else:
                print(f"❌ ERROR: {result.get('message', 'Unknown error')}")
                
        except Exception as e:
            print(f"💥 EXCEPTION: {str(e)}")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    
    print(f"\n✅ Prompts that generated actual images ({len(successful_prompts)}):")
    for prompt in successful_prompts:
        print(f"  • '{prompt}'")
    
    print(f"\n📝 Prompts that gave text descriptions ({len(text_prompts)}):")
    for prompt in text_prompts:
        print(f"  • '{prompt}'")
    
    if successful_prompts:
        print(f"\n🎉 Success rate: {len(successful_prompts)}/{len(test_prompts)} ({len(successful_prompts)/len(test_prompts)*100:.1f}%)")
        print("\n💡 Try using similar prompts to these successful ones!")
    else:
        print("\n⚠️  No prompts generated actual images.")
        print("This is normal with Google's safety filtering.")
        print("The text descriptions are still valuable creative outputs!")
    
    print("\n🔧 To test manually, try running:")
    print("python -c \"from chatgpt_agentic_clone.agent import generate_image; print(generate_image('abstract blue swirls'))\"")

if __name__ == "__main__":
    test_image_prompts() 