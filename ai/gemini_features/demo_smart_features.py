#!/usr/bin/env python3
"""
Demo: Smart Context-Aware Voice Features
Demonstrates intelligent multi-tool execution
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

def demo():
    """Demonstrate smart features"""
    
    print("\n" + "="*80)
    print("🧠 CLI-TOP SMART VOICE ASSISTANT - FEATURE DEMONSTRATION")
    print("="*80)
    
    print("""
The voice assistant now includes SMART CONTEXT-AWARE features that understand
your intent and automatically run multiple tools to provide comprehensive analysis.

╔════════════════════════════════════════════════════════════════════════════╗
║                        🎯 SMART FEATURES AVAILABLE                          ║
╠════════════════════════════════════════════════════════════════════════════╣
║                                                                            ║
║  1️⃣  "Can I leave classes?" / "Should I skip classes?"                     ║
║      ↳ Automatically runs:                                                 ║
║         • VTOP Attendance                                                  ║
║         • AI Attendance Calculator (buffer analysis)                       ║
║         • Gemini AI Advice (personalized recommendations)                  ║
║                                                                            ║
║  2️⃣  "How am I doing?" / "Am I doing well?"                                ║
║      ↳ Automatically runs:                                                 ║
║         • VTOP CGPA View                                                   ║
║         • AI Performance Trends Analyzer                                   ║
║         • Gemini Performance Insights                                      ║
║                                                                            ║
║  3️⃣  "What should I focus on?" / "What to study?"                          ║
║      ↳ Automatically runs:                                                 ║
║         • AI Weakness Identifier                                           ║
║         • Gemini Study Plan Generator                                      ║
║                                                                            ║
║  4️⃣  "Will I pass?" / "Am I exam ready?"                                   ║
║      ↳ Automatically runs:                                                 ║
║         • AI Exam Readiness Calculator                                     ║
║         • AI Grade Predictor                                               ║
║         • Gemini AI Exam Advice                                            ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝

🔍 HOW IT WORKS:

   1. You ask a natural question (e.g., "Can I skip classes today?")
   2. The AI understands your intent using pattern matching
   3. Multiple tools are executed automatically:
      • VTOP features for raw data
      • AI features for algorithmic analysis
      • Gemini AI for personalized advice
   4. Results are presented in a unified, actionable format

💡 EXAMPLE USAGE:

   Terminal Command:
   $ ./cli-top ai voice

   Then say or type:
   "Can I leave classes?"

   Voice Assistant will:
   ✅ Show current attendance from VTOP
   ✅ Calculate skip buffer for each subject
   ✅ Generate AI advice: "You can safely skip 3 classes in DBMS,
      but avoid missing Compiler Design (only 1 class buffer)"

🎯 BENEFITS:

   ✓ No need to remember specific commands
   ✓ Natural language understanding
   ✓ Multi-tool execution in one go
   ✓ AI-powered personalized advice
   ✓ Time-saving automation

📝 ALL SUPPORTED SMART PATTERNS:

   Attendance Advice:
   • "Can I leave classes?"
   • "Should I skip classes?"
   • "Can I skip?"
   • "Can I bunk?"
   • "Should I attend?"

   Performance Overview:
   • "How am I doing?"
   • "Am I doing well?"
   • "My performance"

   Focus Advisor:
   • "What should I focus on?"
   • "What to study?"
   • "Where to improve?"

   Exam Prediction:
   • "Will I pass?"
   • "Can I pass?"
   • "Am I exam ready?"

🚀 TRY IT NOW:

   1. Install voice dependencies (optional):
      $ brew install portaudio
      $ pip install SpeechRecognition pyttsx3 pyaudio

   2. Run voice assistant:
      $ ./cli-top ai voice

   3. Try smart commands:
      → "Can I leave classes?"
      → "How am I doing?"
      → "What should I focus on?"
      → "Will I pass?"

   Or use text mode if speech libraries not installed!

""")
    
    print("="*80)
    print("✅ Smart features are ready to use!")
    print("="*80)
    print()

if __name__ == "__main__":
    demo()
