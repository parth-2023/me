#!/usr/bin/env python3
"""
Voice Assistant Demo - Interactive test without requiring VTOP login
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'ai'))

from ai.gemini_features.voice_assistant import VoiceAssistant

def demo_mode():
    """Run voice assistant in demo mode"""
    print("="*70)
    print("🎙️  CLI-TOP VOICE ASSISTANT - DEMO MODE")
    print("="*70)
    print("\n⚠️  Running without VTOP data (demo mode)")
    print("   To use with real data, login first: ./cli-top login\n")
    
    # Create assistant without VTOP data
    assistant = VoiceAssistant(vtop_data=None)
    
    # Show available commands
    assistant.show_help()
    
    print("\n💡 Demo Commands (text mode):")
    print("   - Type 'help' to see all commands")
    print("   - Type 'exit' to quit")
    print("   - Try: 'what features are available?'")
    print("   - Try: 'explain the AI features'")
    print("="*70 + "\n")
    
    # Run the assistant
    try:
        while True:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            action, param = assistant.parse_command(user_input)
            
            if action == 'exit':
                assistant.speak("Goodbye! Have a great day!")
                break
            
            elif action == 'help':
                assistant.show_help()
            
            elif action == 'vtop':
                print(f"\n📊 Would execute: ./cli-top {param}")
                assistant.speak(f"To use {param}, please login first with: cli-top login")
            
            elif action == 'ai':
                print(f"\n🤖 Would execute: ./cli-top ai {param}")
                assistant.speak(f"To use {param} feature, please login first")
            
            elif action == 'gemini':
                print(f"\n✨ Would execute: ./cli-top ai {param}")
                assistant.speak(f"To use {param}, please login first")
            
            elif action == 'chat':
                # This works without login!
                assistant.chat(user_input)
            
            print()
    
    except KeyboardInterrupt:
        print("\n")
        assistant.speak("Interrupted. Goodbye!")

if __name__ == '__main__':
    demo_mode()
