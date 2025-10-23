# CLI-TOP Dev 2 - Voice Assistant & Gemini 2.5 Flash Update

## 🎉 New Features Added

### 1. **Gemini 2.5 Flash** - Updated AI Model
- ✅ Upgraded from Gemini 2.0 Flash to **Gemini 2.5 Flash**
- ✅ Faster response times
- ✅ More accurate insights
- ✅ Better context understanding

### 2. **Voice Assistant** 🎙️ - Gemini 2.5 Flash Live
A complete voice-controlled interface to access ALL CLI-TOP features!

**Features:**
- 🎤 **Speech Recognition** - Convert your voice to commands
- 🔊 **Text-to-Speech** - Hear responses from the assistant
- 🤖 **Gemini 2.5 Flash** - AI-powered understanding
- 📊 **Execute VTOP Features** - "Show my marks", "Check attendance"
- 🔬 **Run AI Features** - "Run all AI features", "Grade predictor"
- ✨ **Use Gemini Features** - "Career advice", "Study plan"
- 💬 **Conversational** - Ask questions naturally
- 📱 **Hands-free** - Perfect for multitasking
- ✅ **Interactive Mode** - Handles multi-step commands (semester selection, etc.)

**Voice Commands Examples:**
```
"Show my marks"           → Interactive: Select semester, view detailed marks
"Check attendance"        → Interactive: Select semester, view attendance
"View assignments"        → Interactive: Select semester, view DA
"View timetable"          → Direct: Shows today's timetable
"Run all AI features"     → Interactive: Runs all AI analyses
"Give me career advice"   → Interactive: Gemini career guidance
"Generate a study plan"   → Interactive: Custom study planning
"What's my CGPA?"         → Direct: Shows current CGPA
"Which subjects need attention?" → Conversational AI response
"Help" - shows all commands
"Exit" - closes assistant
```

**Interactive vs Direct Commands:**
- **Interactive:** Commands like marks, attendance, DA require semester selection
- **Direct:** Commands like CGPA, profile, timetable show results immediately

### 3. **Enhanced Study Guide Generator**
- ✅ Interactive course selection
- ✅ Comprehensive guides per course
- ✅ Chapter-by-chapter breakdown
- ✅ Resource recommendations
- ✅ Exam strategies

## 📦 Installation

### Install Speech Dependencies (for Voice Assistant)

**macOS:**
```bash
# Install PortAudio first
brew install portaudio

# Install Python packages
pip install SpeechRecognition pyttsx3 pyaudio
```

**Linux (Ubuntu/Debian):**
```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install portaudio19-dev python3-pyaudio espeak

# Install Python packages
pip install SpeechRecognition pyttsx3 pyaudio
```

**Windows:**
```bash
# Install Python packages (PyAudio might need wheel)
pip install SpeechRecognition pyttsx3
pip install pipwin
pipwin install pyaudio
```

## 🚀 Usage

### Voice Assistant

```bash
# Start voice assistant
./cli-top ai voice

# The assistant will:
# 1. Automatically fetch your VTOP data
# 2. Initialize speech engines
# 3. Start listening for commands
# 4. Speak responses and display results
```

**Text Mode** (if speech libraries not installed):
```bash
# Still works in text mode
./cli-top ai voice
# You: Show my marks
```

### Study Guide Generator

```bash
# Interactive mode
./cli-top ai study-guide

# Select from your courses
# Get comprehensive study guide
```

### Updated Gemini Features (Now using 2.5 Flash)

```bash
# All these now use Gemini 2.5 Flash
./cli-top ai chatbot
./cli-top ai career
./cli-top ai study-plan
./cli-top ai insights
./cli-top ai study-guide
```

## 🎯 Voice Assistant Capabilities

### VTOP Features (18 commands)
- marks, grades, cgpa, attendance
- timetable, exams, profile, hostel
- library, receipts, leave, nightslip
- messages, assignments, syllabus, calendar, facility

### AI Features (9 commands)
- run all ai
- grade predictor
- attendance calculator
- cgpa analyzer
- recovery plan
- exam readiness
- study allocator
- performance trends
- weakness finder
- target planner

### Gemini Features (5 commands)
- chatbot
- career advice
- study plan
- insights
- study guide

### Conversational AI
- Ask any question about your academic data
- Get personalized recommendations
- Natural language understanding

## 📝 Configuration

### Update .env file

```bash
# ai/.env
GOOGLE_API_KEY=your_key_here
GEMINI_MODEL=gemini-2.5-flash
GEMINI_LIVE_MODEL=gemini-2.5-flash-live
```

## 🔧 Troubleshooting

### Voice Assistant Not Working

1. **Check Dependencies:**
```bash
pip list | grep -E "SpeechRecognition|pyttsx3|PyAudio"
```

2. **Test Microphone:**
```bash
python -c "import speech_recognition as sr; print('Microphone OK')"
```

3. **Test Text-to-Speech:**
```bash
python -c "import pyttsx3; engine = pyttsx3.init(); engine.say('Hello'); engine.runAndWait()"
```

4. **macOS Microphone Permission:**
   - System Preferences → Security & Privacy → Microphone
   - Enable for Terminal/iTerm

### PyAudio Installation Issues

**macOS:**
```bash
brew install portaudio
pip install --global-option='build_ext' --global-option='-I/opt/homebrew/include' --global-option='-L/opt/homebrew/lib' pyaudio
```

**Linux:**
```bash
sudo apt-get install portaudio19-dev
pip install pyaudio
```

## 🎓 Example Usage Scenarios

### Scenario 1: Morning Routine
```bash
./cli-top ai voice

You: "Good morning! Show my attendance"
🤖: "Good morning! Fetching attendance... [displays data]"

You: "Do I need to attend any class today?"
🤖: "Based on your attendance, CSE1001 needs attention..."

You: "Show my timetable"
🤖: "Here's your schedule for today..."
```

### Scenario 2: Study Planning
```bash
./cli-top ai voice

You: "I have exams in 2 weeks. Generate a study plan"
🤖: "Creating a 14-day study plan... [generates plan]"

You: "Which subjects need more focus?"
🤖: "Based on your performance, focus on..."

You: "Give me a study guide for Database Systems"
🤖: "Generating comprehensive study guide..."
```

### Scenario 3: Performance Check
```bash
./cli-top ai voice

You: "How am I doing this semester?"
🤖: "Let me analyze your performance... [analyzes]"

You: "Run all AI features"
🤖: "Running all 9 AI analyses... [executes]"

You: "What career paths suit me?"
🤖: "Based on your strengths... [career advice]"
```

## 📊 What Changed

### Files Modified:
- ✅ `ai/config.py` - Updated to Gemini 2.5 Flash
- ✅ `ai/.env.example` - Added new model configs
- ✅ `ai/requirements.txt` - Added speech libraries
- ✅ `cmd/ai.go` - Added voice and study-guide commands

### Files Added:
- ✅ `ai/gemini_features/voice_assistant.py` - Complete voice interface
- ✅ Enhanced `ai/gemini_features/study_guide.py` - Better study guides

### Documentation Updated:
- ✅ `GUIDE.md` - Complete voice assistant documentation
- ✅ `README.md` - Updated feature list
- ✅ `VOICE_FEATURES.md` - This file!

## 🌟 Feature Comparison

### Before:
- Gemini 2.0 Flash
- 4 Gemini features
- Text-only interaction
- Manual command typing

### After:
- **Gemini 2.5 Flash** ⚡
- **6 Gemini features** (including voice)
- **Voice + Text interaction** 🎙️
- **Hands-free operation**
- **Natural language understanding**
- **Real-time speech processing**

## 🎯 Commands Summary

```bash
# New Commands
./cli-top ai voice         # Voice assistant (NEW!)
./cli-top ai study-guide   # Study guide generator (ENHANCED!)

# Updated Commands (now use Gemini 2.5 Flash)
./cli-top ai chatbot       # Faster responses
./cli-top ai career        # Better insights
./cli-top ai study-plan    # Smarter plans
./cli-top ai insights      # Deeper analysis
```

## 💡 Pro Tips

1. **Voice Commands**: Speak clearly and naturally
2. **Background Noise**: Works best in quiet environment
3. **Fallback**: Voice assistant works in text mode too
4. **Multitasking**: Use voice while working on assignments
5. **Quick Checks**: Perfect for checking attendance/marks hands-free
6. **Study Sessions**: Use voice to navigate while studying

## 🚀 Next Steps

1. Install speech dependencies
2. Configure Gemini API key
3. Try voice assistant: `./cli-top ai voice`
4. Say "help" to see all commands
5. Enjoy hands-free CLI-TOP! 🎉

---

**Powered by Gemini 2.5 Flash & Gemini 2.5 Flash Live**

*Made with ❤️ for VIT Students*
