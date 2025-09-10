#!/usr/bin/env python3

import os
import sys
sys.path.append('.')

# Set environment variable
os.environ['GEMINI_API_KEY'] = 'AIzaSyB3Dmh8MGD8VmHuz1nikFAhjVmgpOzNeds'

try:
    from app.ml.gemini_detector import gemini_detector
    
    print("🔧 Gemini Configuration Test")
    print("=" * 40)
    print(f"API Key loaded: {'Yes' if gemini_detector.api_key and gemini_detector.api_key != 'demo_key' else 'No'}")
    print(f"Demo mode: {gemini_detector.is_demo_mode}")
    print(f"API Key (first 20 chars): {gemini_detector.api_key[:20] if gemini_detector.api_key else 'None'}")
    print(f"Model name: {gemini_detector.model_name}")
    
    if not gemini_detector.is_demo_mode:
        print("\n✅ Real Gemini API mode enabled!")
    else:
        print("\n⚠️  Still in demo mode")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()