#!/usr/bin/env python3
"""
Voice Assistant - Gemini 2.5 Flash Live with Voice Interaction
Execute all CLI-TOP features using voice commands with real-time feedback
"""

import json
import sys
import os
import subprocess
import threading
import queue
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import google.generativeai as genai
    from config import GOOGLE_API_KEY, GEMINI_LIVE_MODEL
except ImportError:
    print("❌ Error: google-generativeai not installed")
    print("   Run: pip install -r ai/requirements.txt")
    sys.exit(1)

# Check for speech dependencies
try:
    import speech_recognition as sr
    import pyttsx3
    SPEECH_AVAILABLE = True
except ImportError:
    print("⚠️  Warning: Speech libraries not installed")
    print("   Install with: pip install SpeechRecognition pyttsx3 pyaudio")
    SPEECH_AVAILABLE = False

class VoiceAssistant:
    """AI Voice Assistant powered by Gemini 2.5 Flash Live"""
    
    def __init__(self, vtop_data=None):
        """Initialize voice assistant"""
        self.vtop_data = vtop_data
        
        if not GOOGLE_API_KEY:
            print("❌ Error: GOOGLE_API_KEY not configured")
            sys.exit(1)
        
        # Configure Gemini
        genai.configure(api_key=GOOGLE_API_KEY)
        # Use standard model for text chat, Live model would be for streaming voice
        from config import GEMINI_MODEL
        self.model = genai.GenerativeModel(GEMINI_MODEL)
        
        # Initialize speech engines
        if SPEECH_AVAILABLE:
            self.recognizer = sr.Recognizer()
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', 175)  # Speed
            self.tts_engine.setProperty('volume', 0.9)  # Volume
        
        # Available commands
        self.commands = {
            'vtop': [
                'marks', 'grades', 'cgpa', 'attendance', 'timetable', 
                'exams', 'profile', 'hostel', 'library', 'receipts',
                'leave', 'nightslip', 'messages', 'assignments', 
                'syllabus', 'course materials', 'calendar', 'facility'
            ],
            'ai': [
                'run all ai', 'grade predictor', 'attendance calculator',
                'cgpa analyzer', 'recovery plan', 'exam readiness',
                'study allocator', 'performance trends', 'weakness finder',
                'target planner'
            ],
            'gemini': [
                'chatbot', 'career advice', 'study plan', 'insights',
                'study guide'
            ]
        }
        
        # Build context if vtop_data available
        self.context = self._build_context() if vtop_data else ""
    
    def _build_context(self):
        """Build context from VTOP data"""
        if not self.vtop_data:
            return ""
        
        context = f"""
You are a voice-activated AI assistant for CLI-TOP, helping VIT students manage their academics.

STUDENT DATA:
- Registration: {self.vtop_data.get('reg_no', 'N/A')}
- Semester: {self.vtop_data.get('semester', 'N/A')}
- CGPA: {self.vtop_data.get('cgpa', 'N/A')}
- Total Courses: {len(self.vtop_data.get('marks', []))}

CAPABILITIES:
1. VTOP Features: {', '.join(self.commands['vtop'][:8])} and more
2. AI Features: {', '.join(self.commands['ai'][:5])} and more
3. Gemini Features: {', '.join(self.commands['gemini'])}

You can execute any CLI-TOP feature using voice commands.
Respond naturally and conversationally.
"""
        return context
    
    def speak(self, text):
        """Text-to-speech output"""
        print(f"\n🔊 Assistant: {text}\n")
        if SPEECH_AVAILABLE:
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except Exception as e:
                print(f"⚠️  TTS Error: {e}")
    
    def listen(self):
        """Voice recognition input"""
        if not SPEECH_AVAILABLE:
            return input("You: ").strip()
        
        print("🎤 Listening...")
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            print("🔄 Processing...")
            text = self.recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        
        except sr.WaitTimeoutError:
            print("⏱️  No speech detected")
            return ""
        except sr.UnknownValueError:
            print("❓ Could not understand audio")
            return ""
        except Exception as e:
            print(f"❌ Error: {e}")
            return ""
    
    def parse_command(self, user_input):
        """Parse user input to determine action - with smart context understanding"""
        user_input_lower = user_input.lower()
        
        # Check for exit commands
        if any(word in user_input_lower for word in ['exit', 'quit', 'bye', 'stop']):
            return 'exit', None
        
        # Check for help
        if any(word in user_input_lower for word in ['help', 'what can you do']):
            return 'help', None
        
        # Smart context-aware command detection
        # "Can I leave classes?" → attendance + advice
        if any(phrase in user_input_lower for phrase in ['can i leave', 'should i skip', 'can i skip', 'can i bunk', 'should i attend']):
            return 'smart', 'attendance_advice'
        
        # "Am I doing well?" → marks + cgpa + insights
        if any(phrase in user_input_lower for phrase in ['am i doing well', 'how am i doing', 'my performance']):
            return 'smart', 'performance_overview'
        
        # "What should I focus on?" → weakness finder + study plan
        if any(phrase in user_input_lower for phrase in ['what should i focus', 'what to study', 'where to improve']):
            return 'smart', 'focus_advisor'
        
        # "Will I pass?" → exam readiness + grade predictor
        if any(phrase in user_input_lower for phrase in ['will i pass', 'can i pass', 'exam ready']):
            return 'smart', 'exam_prediction'
        
        # Check for VTOP features
        for cmd in self.commands['vtop']:
            if cmd in user_input_lower:
                return 'vtop', cmd
        
        # Check for AI features
        if 'run all ai' in user_input_lower or 'all ai features' in user_input_lower:
            return 'ai', 'run-all'
        
        for cmd in self.commands['ai']:
            if cmd.replace(' ', '') in user_input_lower.replace(' ', ''):
                return 'ai', cmd
        
        # Check for Gemini features
        for cmd in self.commands['gemini']:
            if cmd in user_input_lower:
                return 'gemini', cmd
        
        # Default to conversation
        return 'chat', user_input
    
    def execute_vtop_feature(self, feature):
        """Execute VTOP feature with interactive support"""
        self.speak(f"Executing {feature}. Please wait.")
        
        # Map friendly names to CLI commands
        cmd_map = {
            'marks': 'marks',
            'grades': 'grades',
            'cgpa': 'cgpa',
            'attendance': 'attendance',
            'timetable': 'timetable',
            'exams': 'exams',
            'profile': 'profile',
            'hostel': 'hostel',
            'library': 'library-dues',
            'receipts': 'receipts',
            'leave': 'leave',
            'nightslip': 'nightslip',
            'messages': 'msg',
            'assignments': 'da',
            'syllabus': 'syllabus',
            'calendar': 'calendar',
            'facility': 'facility'
        }
        
        cli_cmd = cmd_map.get(feature, feature)
        cli_path = Path(__file__).parent.parent.parent / 'cli-top'
        
        # Commands that require interactive selection (semester, etc.)
        interactive_commands = ['marks', 'grades', 'attendance', 'da', 'syllabus']
        
        try:
            if cli_cmd in interactive_commands:
                # Use interactive mode - let user interact directly
                print("\n" + "="*70)
                print(f"🎤 Launching {feature} (interactive mode)")
                print("="*70 + "\n")
                
                # Run in foreground with TTY
                result = subprocess.run(
                    [str(cli_path), cli_cmd],
                    stdin=sys.stdin,
                    stdout=sys.stdout,
                    stderr=sys.stderr
                )
                
                print("\n" + "="*70 + "\n")
                if result.returncode == 0:
                    self.speak(f"{feature} completed successfully.")
                else:
                    self.speak(f"There was an error executing {feature}.")
            else:
                # Non-interactive commands can capture output
                result = subprocess.run(
                    [str(cli_path), cli_cmd],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                
                if result.returncode == 0:
                    print("\n" + "="*70)
                    print(result.stdout)
                    print("="*70 + "\n")
                    self.speak(f"{feature} completed successfully. Check the output above.")
                else:
                    print(f"❌ Error: {result.stderr}")
                    self.speak(f"There was an error executing {feature}.")
        
        except Exception as e:
            print(f"❌ Execution error: {e}")
            self.speak(f"Failed to execute {feature}.")
    
    def execute_ai_feature(self, feature):
        """Execute AI feature with interactive support"""
        self.speak(f"Running AI analysis for {feature}. This may take a moment.")
        
        cli_path = Path(__file__).parent.parent.parent / 'cli-top'
        
        if feature == 'run-all':
            cmd = [str(cli_path), 'ai', 'run-all']
        else:
            # Map to CLI commands - comprehensive mapping
            cmd_map = {
                'grade predictor': ['ai', 'grade', 'predict'],
                'attendance calculator': ['ai', 'attendance', 'buffer'],
                'cgpa analyzer': ['ai', 'grade', 'cgpa'],
                'recovery plan': ['ai', 'attendance', 'recover'],
                'exam readiness': ['ai', 'exam', 'ready'],
                'study allocator': ['ai', 'study', 'allocate'],
                'performance trends': ['ai', 'trend'],
                'weakness finder': ['ai', 'weakness'],
                'target planner': ['ai', 'target']
            }
            
            # If not in map, try direct command
            if feature in cmd_map:
                cmd = [str(cli_path)] + cmd_map[feature]
            else:
                # Try to parse the feature name
                feature_parts = feature.replace(' ', '-').split('-')
                cmd = [str(cli_path), 'ai'] + feature_parts
        
        # AI features that might need interaction
        interactive_ai = ['grade predictor', 'run-all', 'recovery plan']
        
        try:
            if feature in interactive_ai:
                # Interactive mode for features that might prompt
                print("\n" + "="*70)
                print(f"🤖 Running {feature} (interactive mode)")
                print("="*70 + "\n")
                
                result = subprocess.run(
                    cmd,
                    stdin=sys.stdin,
                    stdout=sys.stdout,
                    stderr=sys.stderr,
                    timeout=120
                )
                
                print("\n" + "="*70 + "\n")
                if result.returncode == 0:
                    self.speak("AI analysis complete.")
                else:
                    self.speak("There was an error during analysis.")
            else:
                # Non-interactive AI features
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=120
                )
                
                if result.returncode == 0:
                    print("\n" + "="*70)
                    print(result.stdout)
                    print("="*70 + "\n")
                    self.speak("AI analysis complete. Check the detailed output above.")
                else:
                    print(f"❌ Error executing {feature}")
                    if result.stderr:
                        print(result.stderr)
                    self.speak(f"There was an error running {feature}.")
        
        except Exception as e:
            print(f"❌ Error: {e}")
            self.speak("Failed to complete AI analysis.")
    
    def execute_gemini_feature(self, feature):
        """Execute Gemini AI feature with interactive support"""
        self.speak(f"Activating Gemini AI for {feature}.")
        
        cli_path = Path(__file__).parent.parent.parent / 'cli-top'
        
        cmd_map = {
            'chatbot': ['ai', 'chatbot'],
            'career advice': ['ai', 'career'],
            'study plan': ['ai', 'study-plan'],
            'insights': ['ai', 'insights'],
            'study guide': ['ai', 'study-guide']
        }
        
        cmd = [str(cli_path)] + cmd_map.get(feature, ['ai', 'chatbot'])
        
        # Gemini features are typically interactive
        try:
            print("\n" + "="*70)
            print(f"✨ Launching {feature} (interactive mode)")
            print("="*70 + "\n")
            
            result = subprocess.run(
                cmd,
                stdin=sys.stdin,
                stdout=sys.stdout,
                stderr=sys.stderr,
                timeout=120
            )
            
            print("\n" + "="*70 + "\n")
            if result.returncode == 0:
                self.speak("Gemini AI session complete.")
            else:
                self.speak("There was an error with Gemini feature.")
        except Exception as e:
            print(f"❌ Error: {e}")
            self.speak("Failed to execute Gemini feature.")
    
    def execute_smart_command(self, smart_type):
        """Execute smart context-aware multi-tool commands with AI advice"""
        
        if smart_type == 'attendance_advice':
            self.speak("Let me check your attendance and advise you.")
            print("\n" + "="*70)
            print("🧠 SMART ANALYSIS: Can I Leave Classes?")
            print("="*70 + "\n")
            
            # Run attendance feature
            self.execute_vtop_feature('attendance')
            
            # Run attendance calculator
            print("\n📊 Running AI Attendance Analysis...\n")
            self.execute_ai_feature('attendance calculator')
            
            # Provide AI advice
            self.speak("Based on your attendance, here's my advice:")
            advice_prompt = """
You are an academic advisor. Based on the attendance data shown above, provide concise advice:
1. Can the student afford to miss classes?
2. Which subjects are critical (below 75%)?
3. Specific recommendations (3-4 sentences max)

Be direct and actionable.
"""
            try:
                response = self.model.generate_content(advice_prompt)
                advice = response.text
                print("\n💡 AI ADVICE:\n")
                print(advice)
                self.speak(advice)
            except Exception as e:
                self.speak("I've shown your attendance data. Please review it carefully.")
        
        elif smart_type == 'performance_overview':
            self.speak("Let me analyze your overall academic performance.")
            print("\n" + "="*70)
            print("🧠 SMART ANALYSIS: Performance Overview")
            print("="*70 + "\n")
            
            # Show CGPA
            self.execute_vtop_feature('cgpa')
            
            # Run performance analyzer
            print("\n📊 Running AI Performance Analysis...\n")
            self.execute_ai_feature('performance trends')
            
            # Get Gemini insights
            print("\n✨ Getting Gemini Insights...\n")
            self.execute_gemini_feature('insights')
            
            self.speak("I've provided a complete performance overview with AI insights.")
        
        elif smart_type == 'focus_advisor':
            self.speak("Let me identify areas that need your attention.")
            print("\n" + "="*70)
            print("🧠 SMART ANALYSIS: Focus Areas")
            print("="*70 + "\n")
            
            # Run weakness identifier
            print("\n🔍 Identifying Weak Areas...\n")
            self.execute_ai_feature('weakness finder')
            
            # Generate study plan
            print("\n📚 Generating Study Plan...\n")
            self.execute_gemini_feature('study plan')
            
            self.speak("I've identified your weak areas and created a focused study plan.")
        
        elif smart_type == 'exam_prediction':
            self.speak("Let me assess your exam readiness and predict outcomes.")
            print("\n" + "="*70)
            print("🧠 SMART ANALYSIS: Exam Prediction")
            print("="*70 + "\n")
            
            # Check exam readiness
            print("\n📝 Checking Exam Readiness...\n")
            self.execute_ai_feature('exam readiness')
            
            # Run grade predictor
            print("\n🎯 Predicting Grades...\n")
            self.execute_ai_feature('grade predictor')
            
            # Provide advice
            advice_prompt = """
Based on the exam readiness scores and grade predictions shown above, provide:
1. Overall verdict (Pass/At Risk/Need Improvement)
2. Which exams need most focus
3. Specific action items (3-4 points max)

Be encouraging but realistic.
"""
            try:
                response = self.model.generate_content(advice_prompt)
                advice = response.text
                print("\n💡 AI EXAM ADVICE:\n")
                print(advice)
                self.speak(advice)
            except Exception as e:
                self.speak("Please review the exam analysis above carefully.")
    
    def chat(self, user_message):
        """Chat with Gemini AI"""
        try:
            prompt = self.context + f"\n\nUser: {user_message}\n\nRespond naturally and concisely."
            response = self.model.generate_content(prompt)
            reply = response.text
            self.speak(reply)
        except Exception as e:
            print(f"❌ Chat error: {e}")
            self.speak("I'm having trouble understanding. Please try again.")
    
    def show_help(self):
        """Show available commands"""
        help_text = """
I can help you with:

🧠 Smart Commands (AI-Powered Multi-Tool):
   Say: "Can I leave classes?" - Checks attendance + provides advice
   Say: "How am I doing?" - Shows performance overview with insights
   Say: "What should I focus on?" - Identifies weak areas + study plan
   Say: "Will I pass?" - Exam readiness + grade predictions

📊 VTOP Features:
   Say: "Show my marks", "Check attendance", "View timetable", "Exam schedule"

🤖 AI Features:
   Say: "Run all AI features", "Grade predictor", "Attendance calculator"
   Say: "Exam readiness", "Weakness finder", "Performance trends"

✨ Gemini Features:
   Say: "Open chatbot", "Career advice", "Study plan", "Performance insights"

💬 Chat:
   Ask me anything about your academic performance!

🚪 Exit:
   Say: "Exit", "Quit", or "Bye"
"""
        print(help_text)
        self.speak("I've displayed all available commands, including smart multi-tool features. What would you like to do?")
    
    def run(self):
        """Main voice assistant loop"""
        print("="*70)
        print("🎙️  CLI-TOP VOICE ASSISTANT")
        print("="*70)
        print("Powered by Gemini 2.5 Flash Live")
        print()
        
        if not SPEECH_AVAILABLE:
            print("⚠️  Running in text mode (speech libraries not installed)")
        
        self.speak("Hello! I'm your CLI-TOP voice assistant. How can I help you today?")
        
        while True:
            try:
                # Get user input
                user_input = self.listen()
                
                if not user_input:
                    continue
                
                # Parse command
                action, param = self.parse_command(user_input)
                
                if action == 'exit':
                    self.speak("Goodbye! Have a great day!")
                    break
                
                elif action == 'help':
                    self.show_help()
                
                elif action == 'smart':
                    self.execute_smart_command(param)
                
                elif action == 'vtop':
                    self.execute_vtop_feature(param)
                
                elif action == 'ai':
                    self.execute_ai_feature(param)
                
                elif action == 'gemini':
                    self.execute_gemini_feature(param)
                
                elif action == 'chat':
                    self.chat(user_input)
                
                # Brief pause between interactions
                print()
            
            except KeyboardInterrupt:
                print("\n")
                self.speak("Interrupted. Goodbye!")
                break
            
            except Exception as e:
                print(f"❌ Error: {e}")
                self.speak("An error occurred. Let's try again.")

def main():
    """Main entry point"""
    # Load VTOP data if available
    vtop_data = None
    
    if len(sys.argv) > 1:
        data_file = sys.argv[1]
        try:
            with open(data_file, 'r') as f:
                vtop_data = json.load(f)
            print(f"✅ Loaded VTOP data from {data_file}")
        except Exception as e:
            print(f"⚠️  Could not load data: {e}")
    else:
        # Try to fetch data automatically
        print("🔄 Fetching fresh VTOP data...")
        try:
            from fetch_vtop_data import fetch_vtop_data
            import tempfile
            
            temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
            temp_file.close()
            vtop_data = fetch_vtop_data(temp_file.name)
            print("✅ VTOP data loaded successfully")
        except Exception as e:
            print(f"⚠️  Running without VTOP data: {e}")
    
    # Initialize and run assistant
    assistant = VoiceAssistant(vtop_data)
    assistant.run()

if __name__ == '__main__':
    main()
