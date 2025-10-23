#!/usr/bin/env python3
"""
Test smart context-aware features without voice input
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Disable speech to force text mode
import sys
original_modules = sys.modules.copy()
sys.modules['speech_recognition'] = None
sys.modules['pyttsx3'] = None

from voice_assistant import VoiceAssistant

def test_smart_features():
    """Test all smart features"""
    
    print("="*70)
    print("🧪 TESTING SMART CONTEXT-AWARE FEATURES")
    print("="*70)
    print()
    
    # Initialize assistant
    assistant = VoiceAssistant()
    
    # Override speak to just print
    assistant.speak = lambda text: print(f"🔊 {text}\n")
    
    # Test commands
    test_commands = [
        ("Can I leave classes?", "smart", "attendance_advice"),
        ("How am I doing?", "smart", "performance_overview"),
        ("What should I focus on?", "smart", "focus_advisor"),
        ("Will I pass?", "smart", "exam_prediction"),
    ]
    
    for command, expected_action, expected_param in test_commands:
        print(f"\n{'='*70}")
        print(f"📝 Testing: '{command}'")
        print(f"{'='*70}\n")
        
        # Parse command
        action, param = assistant.parse_command(command)
        
        print(f"✅ Parsed as: {action} → {param}")
        
        # Verify correct parsing
        if action == expected_action and param == expected_param:
            print(f"✅ PASS: Correctly identified as smart command\n")
        else:
            print(f"❌ FAIL: Expected ({expected_action}, {expected_param}), got ({action}, {param})\n")
    
    print("\n" + "="*70)
    print("✅ Smart feature parsing tests complete")
    print("="*70)

if __name__ == "__main__":
    test_smart_features()
