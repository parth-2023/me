# 🎙️ Voice Assistant Quick Start

## What is Voice Assistant?

The CLI-TOP Voice Assistant is a **hands-free, voice-controlled interface** powered by **Gemini 2.5 Flash Live** that lets you access ALL CLI-TOP features using natural voice commands!

## Quick Install

```bash
# Install speech dependencies
pip install SpeechRecognition pyttsx3 pyaudio

# macOS: Install PortAudio first
brew install portaudio

# Linux: Install dependencies
sudo apt-get install portaudio19-dev python3-pyaudio
```

## Quick Start

```bash
# Start voice assistant
./cli-top ai voice

# 🎤 Then just speak naturally!
```

## Voice Commands

### 📊 VTOP Features
```
"Show my marks"
"Check attendance"
"View timetable"
"Show exam schedule"
"What's my CGPA?"
"Show my profile"
"Check library dues"
```

### 🤖 AI Features
```
"Run all AI features"
"Grade predictor"
"Attendance calculator"
"Show performance trends"
```

### ✨ Gemini Features
```
"Give me career advice"
"Generate study plan"
"Show insights"
"Create study guide"
```

### 💬 Ask Questions
```
"How am I doing this semester?"
"Which subjects need attention?"
"Can I get an A grade in CSE1001?"
"What should I study this week?"
```

### 🚪 Control
```
"Help" - Show all commands
"Exit" or "Quit" - Close assistant
```

## Features

✅ **Speech Recognition** - Understands natural speech  
✅ **Text-to-Speech** - Speaks responses back  
✅ **Real-time Processing** - Gemini 2.5 Flash Live  
✅ **Full Feature Access** - All 21 VTOP + 9 AI + 6 Gemini features  
✅ **Smart Commands** - Natural language understanding  
✅ **Visual + Audio** - Displays results AND speaks them  
✅ **Text Fallback** - Works without mic if needed  

## Example Session

```
🎙️  CLI-TOP VOICE ASSISTANT
Powered by Gemini 2.5 Flash Live

🔊 Assistant: Hello! I'm your CLI-TOP voice assistant. How can I help you today?

🎤 Listening...
You said: Show my marks

🔊 Assistant: Executing marks. Please wait.

====================================================================
[Displays your marks table]
====================================================================

🔊 Assistant: Marks completed successfully. Check the output above.

🎤 Listening...
You said: Run all AI features

🔊 Assistant: Running AI analysis. This may take a moment.

[Runs all 9 AI features and displays results]

🔊 Assistant: AI analysis complete. Check the detailed output above.

🎤 Listening...
You said: Give me career advice

🔊 Assistant: Activating Gemini AI for career advice.

[Shows comprehensive career recommendations]

🔊 Assistant: Gemini AI analysis complete.

🎤 Listening...
You said: Exit

🔊 Assistant: Goodbye! Have a great day!
```

## Troubleshooting

### No microphone detected
```bash
# Test mic
python -c "import speech_recognition as sr; print('OK')"

# macOS: Enable mic permission
System Preferences → Privacy → Microphone → Enable Terminal
```

### PyAudio error
```bash
# macOS
brew install portaudio
pip install pyaudio

# Linux
sudo apt-get install portaudio19-dev
pip install pyaudio
```

### Works in text mode
If speech libraries aren't installed, assistant automatically runs in text mode - just type commands!

---

**🎯 Pro Tip**: Use voice assistant while studying or working - completely hands-free academic management!

**Powered by Gemini 2.5 Flash Live** ✨
