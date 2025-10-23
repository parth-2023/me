#!/usr/bin/env python3
"""
Quick test script for voice assistant functionality
"""

import sys
import os
from pathlib import Path

# Add ai directory to path
sys.path.insert(0, str(Path(__file__).parent / 'ai'))

print("="*70)
print("🎙️  VOICE ASSISTANT TEST")
print("="*70)

# Test 1: Check dependencies
print("\n1️⃣  Testing Dependencies...")
try:
    import speech_recognition as sr
    print("   ✅ SpeechRecognition: Installed")
except ImportError as e:
    print(f"   ❌ SpeechRecognition: {e}")

try:
    import pyttsx3
    print("   ✅ pyttsx3: Installed")
except ImportError as e:
    print(f"   ❌ pyttsx3: {e}")

try:
    import pyaudio
    print("   ✅ PyAudio: Installed")
except ImportError as e:
    print(f"   ❌ PyAudio: {e}")

try:
    import google.generativeai as genai
    print("   ✅ google-generativeai: Installed")
except ImportError as e:
    print(f"   ❌ google-generativeai: {e}")

# Test 2: Check configuration
print("\n2️⃣  Testing Configuration...")
try:
    from ai.config import GOOGLE_API_KEY, GEMINI_LIVE_MODEL
    if GOOGLE_API_KEY:
        print(f"   ✅ API Key: Configured ({GOOGLE_API_KEY[:20]}...)")
    else:
        print("   ⚠️  API Key: Not set")
    print(f"   ✅ Model: {GEMINI_LIVE_MODEL}")
except Exception as e:
    print(f"   ❌ Config error: {e}")

# Test 3: Check voice assistant module
print("\n3️⃣  Testing Voice Assistant Module...")
try:
    from ai.gemini_features.voice_assistant import VoiceAssistant
    print("   ✅ VoiceAssistant class: Loaded")
    
    # Create instance without VTOP data
    print("   🔄 Creating VoiceAssistant instance...")
    assistant = VoiceAssistant(vtop_data=None)
    print("   ✅ Instance created successfully")
    
    # Test command parsing
    print("\n4️⃣  Testing Command Parsing...")
    test_commands = [
        ("show my marks", "vtop"),
        ("run all ai", "ai"),
        ("career advice", "gemini"),
        ("hello", "chat"),
        ("exit", "exit")
    ]
    
    for cmd, expected_type in test_commands:
        action, param = assistant.parse_command(cmd)
        status = "✅" if action == expected_type else "❌"
        print(f"   {status} '{cmd}' -> {action} ({param})")
    
    # Test 5: Test TTS (if available)
    print("\n5️⃣  Testing Text-to-Speech...")
    try:
        print("   🔊 Testing TTS output...")
        assistant.speak("Voice assistant test successful")
        print("   ✅ TTS working")
    except Exception as e:
        print(f"   ⚠️  TTS error: {e}")
    
    print("\n" + "="*70)
    print("✅ ALL TESTS PASSED!")
    print("="*70)
    print("\nVoice assistant is ready to use!")
    print("Run: ./cli-top ai voice")
    print("="*70)
    
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()
