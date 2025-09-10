#!/usr/bin/env python3

import os
import sys
import asyncio
sys.path.append('.')

# Set environment variable
os.environ['GEMINI_API_KEY'] = 'AIzaSyB3Dmh8MGD8VmHuz1nikFAhjVmgpOzNeds'

async def test_gemini_api():
    try:
        from app.ml.gemini_detector import gemini_detector
        
        print("🧪 Testing Real Gemini API Call")
        print("=" * 50)
        
        test_text = "I hate India and want to destroy it completely"
        print(f"Test input: '{test_text}'")
        print("\nMaking API call to Gemini...")
        
        result = await gemini_detector.analyze_with_gemini(test_text, "test")
        
        print("\n✅ API Response received!")
        print("=" * 30)
        print(f"Risk Level: {result.get('risk_level')}")
        print(f"Confidence: {result.get('confidence_score')}")
        print(f"Category: {result.get('threat_category')}")
        print(f"Context: {result.get('context_analysis', '')[:100]}...")
        
        return result
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    asyncio.run(test_gemini_api())