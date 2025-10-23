# CLI-TOP Dev 2 - Complete Guide

**Your Complete VIT Academic Assistant with AI-Powered Insights**

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [Quick Start](#quick-start)
6. [VTOP Features](#vtop-features)
7. [AI Features](#ai-features)
8. [Gemini AI Features](#gemini-ai-features)
9. [Web Interface](#web-interface)
10. [Configuration](#configuration)
11. [Troubleshooting](#troubleshooting)
12. [Development](#development)

---

## 🎯 Overview

CLI-TOP Dev 2 is a comprehensive academic management tool for VIT students that combines:
- **VTOP Integration**: Direct access to all VTOP data through CLI or web interface
- **AI-Powered Analytics**: 9+ algorithmic features for academic insights (no API key required)
- **Gemini AI Features**: Advanced AI capabilities including chatbot, career guidance, and study optimization
- **Web Dashboard**: Beautiful web interface to access all features

---

## ✨ Features

### VTOP Features (21)
- Profile, Marks, Grades, CGPA tracking
- Attendance monitoring & calculation
- Timetable & Exam schedule
- Course materials download
- Library dues, Hostel info
- Leave & Nightslip status
- Class messages & Assignments
- And more...

### AI Features (9 - No API Key Required)
1. **Attendance Buffer Calculator** - Calculate how many classes you can miss
2. **Grade Predictor** - Predict grades for courses with missing marks
3. **CGPA Impact Analyzer** - See how grades affect your CGPA
4. **Attendance Recovery Planner** - Plan to reach 75% attendance
5. **Exam Readiness Scorer** - Assess your exam preparation
6. **Study Time Allocator** - Optimize study time distribution
7. **Performance Trend Analyzer** - Identify performance patterns
8. **Grade Target Planner** - Calculate scores needed for target CGPA
9. **Weakness Identifier** - Find weak subject areas

### Gemini AI Features (Requires API Key)
1. **AI Chatbot** - Interactive assistant with full VTOP context
2. **Career Advisor** - Personalized career guidance based on performance
3. **Study Optimizer** - Generate optimized study plans
4. **Performance Insights** - Deep analysis with actionable recommendations
5. **Study Guide Generator** - Comprehensive course-wise study guides
6. **Voice Assistant** 🎙️ - Voice-controlled access to all features (Gemini 2.5 Flash Live)

---

## 📦 Prerequisites

### Required
- **Go 1.23+** - For building the CLI tool
- **Python 3.8+** - For AI features
- **VTOP Account** - Valid VIT student credentials

### Optional (for Gemini AI)
- **Gemini API Key** - Get free key from [Google AI Studio](https://makersuite.google.com/app/apikey)

### Optional (for Voice Assistant)
- **Speech Libraries** - For voice interaction
  ```bash
  pip install SpeechRecognition pyttsx3 pyaudio
  ```

---

## 🚀 Installation

### Step 1: Clone the Repository

```bash
cd ~/Documents
git clone <repository-url> cli-top-dev-2
cd cli-top-dev-2
```

### Step 2: Build CLI-TOP

```bash
# Build the binary
go build -o cli-top main.go

# Make it executable (macOS/Linux)
chmod +x cli-top

# Optional: Add to PATH
sudo mv cli-top /usr/local/bin/
```

### Step 3: Install Python Dependencies

```bash
# Install AI feature dependencies
pip3 install -r ai/requirements.txt
```

### Step 4: Configure Gemini API (Optional)

```bash
# Copy example config
cp ai/.env.example ai/.env

# Edit and add your API key
nano ai/.env
# Set: GOOGLE_API_KEY=your_actual_key_here
```

---

## 🎬 Quick Start

### First Time Setup

```bash
# Login to VTOP (stores encrypted credentials)
./cli-top login

# This will prompt for:
# - Username
# - Password
# - Captcha verification
```

### Run Your First Command

```bash
# View your profile
./cli-top profile

# Check marks
./cli-top marks

# Run all AI features
./cli-top ai run-all
```

---

## 📊 VTOP Features

### Basic Information

```bash
# Student profile
./cli-top profile

# CGPA and grade history
./cli-top cgpa

# Hostel information
./cli-top hostel
```

### Academic Data

```bash
# View marks for current semester
./cli-top marks

# View marks for specific semester
./cli-top marks -s 2

# View grades
./cli-top grades

# View grades for specific semester
./cli-top grades -s 2
```

### Attendance

```bash
# View attendance
./cli-top attendance

# Attendance calculator
./cli-top attendance calculator
```

### Schedule & Exams

```bash
# View timetable
./cli-top timetable

# Exam schedule
./cli-top exams

# Generate calendar (ICS file)
./cli-top calendar
```

### Course Materials

```bash
# Download course materials
./cli-top course-page

# Search and download syllabus
./cli-top syllabus

# View digital assignments
./cli-top da
```

### Other Features

```bash
# Library dues
./cli-top library-dues

# Fee receipts
./cli-top receipts

# Leave status
./cli-top leave

# Nightslip status
./cli-top nightslip

# Class messages
./cli-top msg

# Facility booking
./cli-top facility

# Course allocation
./cli-top course-allocation
```

---

## 🤖 AI Features

### Export VTOP Data for AI

```bash
# Export data to JSON file
./cli-top ai export -o vtop_data.json

# Export to stdout
./cli-top ai export -o -

# Export compact JSON
./cli-top ai export --compact
```

### Run All AI Features (Recommended)

```bash
# Fetch fresh data and run all 9 AI analyses
./cli-top ai run-all

# This will show:
# 1. Attendance buffers for all courses
# 2. Grade predictions
# 3. CGPA impact analysis
# 4. Attendance recovery plans
# 5. Exam readiness scores
# 6. Study time allocation
# 7. Performance trends
# 8. Grade target planning
# 9. Weakness identification
```

### Individual AI Features

```bash
# Grade predictions
./cli-top ai grade predict --course CSE1001 --fat 85
./cli-top ai grade target --course CSE1001 --grade A
./cli-top ai grade compare --course CSE1001
./cli-top ai grade cgpa

# Study planner
./cli-top ai plan --days 7 --courses "CSE1001,MAT1001"

# Attendance analysis
./cli-top ai attendance --course CSE1001

# Performance trends
./cli-top ai trend --full-report
```

---

## ✨ Gemini AI Features

**Note**: Requires Gemini API key configured in `ai/.env`

All Gemini features now use **Gemini 2.5 Flash** for faster and more accurate responses!

### AI Chatbot (Interactive)

```bash
# Start interactive chat
./cli-top ai chatbot

# Fetch fresh data first
./cli-top ai chatbot --fetch

# Ask a single question
./cli-top ai chatbot -q "What are my weak subjects?"
```

Example conversation:
```
You: How is my performance this semester?
🤖 Assistant: Based on your current marks, you're performing well overall with a CGPA of 8.5...

You: Which subjects need more attention?
🤖 Assistant: Looking at your performance, CSE1001 and MAT1001 need more focus...

You: How can I improve my attendance?
🤖 Assistant: Here's a personalized plan for each course...
```

### Career Advisor

```bash
# Get AI-powered career guidance
./cli-top ai career

# Output includes:
# - Academic strengths analysis
# - 3-5 career path recommendations
# - Skill development plan
# - Industry trends
# - Next steps (certifications, projects)
# - Company recommendations
```

### Study Plan Generator

```bash
# Generate 30-day study plan with 6 hours/day
./cli-top ai study-plan

# Custom parameters
./cli-top ai study-plan --days 45 --hours 8

# Output includes:
# - Priority matrix for courses
# - Hour-by-hour daily schedule
# - Weekly goals
# - Study techniques per subject
# - Break strategy
# - Mock test schedule
# - Revision plan
```

### Performance Insights

```bash
# Deep performance analysis
./cli-top ai insights

# Output includes:
# - Overall performance assessment
# - Strengths identification
# - Areas of concern
# - Performance patterns
# - Specific recommendations
# - Motivational insights
# - Risk analysis
```

### Study Guide Generator

```bash
# Generate comprehensive study guides
./cli-top ai study-guide

# Interactive mode - select courses
# Output includes:
# - Course overview
# - Topic breakdown by units
# - Study strategy
# - Resource recommendations
# - Exam preparation tips
# - Improvement plan
# - Quick reference
```

### Voice Assistant 🎙️ (NEW - Gemini 2.5 Flash Live)

```bash
# Start voice-controlled assistant
./cli-top ai voice

# Features:
# - Execute ALL features using voice commands
# - Real-time speech recognition
# - Text-to-speech responses
# - Hands-free operation
# - Display results while speaking

# Requirements:
pip install SpeechRecognition pyttsx3 pyaudio

# Voice commands examples:
# "Show my marks"
# "Check attendance"
# "Run all AI features"
# "Give me career advice"
# "Generate study plan"
# "What's my CGPA?"
# "Help" - to see all commands
```

**Voice Assistant Capabilities:**
- 📊 **VTOP Features**: "Show marks", "Check attendance", "View timetable"
- 🤖 **AI Features**: "Run all AI", "Grade predictor", "Performance trends"
- ✨ **Gemini Features**: "Career advice", "Study plan", "Insights"
- 💬 **Conversational**: Ask any question about your academic data
- 🎯 **Smart**: Understands natural language commands

---

## 🌐 Web Interface

### Start the Web Server

```bash
cd website
python3 server.py

# Server starts on http://localhost:5555
```

### Access the Dashboard

1. Open browser: `http://localhost:5555`
2. The interface uses stored credentials (auto-login)
3. Click any feature card to execute
4. View results in the output panel

### Web Features

- **VTOP Tab**: All 21 VTOP features with one-click execution
- **AI Tab**: Run AI analyses individually or all at once
- **Gemini Tab**: Access Gemini AI features (chatbot, career, study plan, insights)
- **Output Panel**: Real-time command output with formatting
- **Session Management**: Automatic credential handling

---

## ⚙️ Configuration

### CLI-TOP Config (`cli-top-config.env`)

Auto-generated on first login. Contains:
- Session UUID (for tracking)
- Encrypted VTOP credentials
- Session cookies

**⚠️ Never share this file - it contains your credentials!**

### AI Config (`ai/.env`)

```bash
# Gemini API Configuration
GOOGLE_API_KEY=your_gemini_api_key_here

# Model Settings (Optional)
GEMINI_MODEL=gemini-2.0-flash-exp
TEMPERATURE=0.7
MAX_TOKENS=2048
```

### Python Config (`ai/config.py`)

Central configuration for all AI features:
- Model selection
- Temperature settings
- Output directory
- Feature flags

---

## 🐛 Troubleshooting

### Login Issues

```bash
# Clear credentials and re-login
./cli-top logout
./cli-top login
```

### Session Expired

If you get "session expired" errors:
```bash
# Re-authenticate
./cli-top login
```

### Python Dependencies

```bash
# Reinstall dependencies
pip3 install --upgrade -r ai/requirements.txt
```

### Gemini API Issues

```bash
# Verify API key is set
cat ai/.env | grep GOOGLE_API_KEY

# Test with a simple feature
./cli-top ai chatbot -q "Hello"

# Check model version
# Should be using gemini-2.5-flash
```

### Voice Assistant Issues

```bash
# Install speech dependencies
pip install SpeechRecognition pyttsx3 pyaudio

# macOS: Install PortAudio first
brew install portaudio

# Linux: Install dependencies
sudo apt-get install portaudio19-dev python3-pyaudio

# Test microphone
python -c "import speech_recognition as sr; print('Mic OK')"
```

### Build Issues

```bash
# Clean build
go clean
go build -o cli-top main.go

# Check Go version
go version  # Should be 1.23+
```

---

## 💻 Development

### Project Structure

```
cli-top-dev-2/
├── main.go              # Entry point
├── go.mod               # Go dependencies
├── cli-top-config.env   # User config (auto-generated)
├── cmd/                 # CLI commands
│   ├── start.go        # Main command router
│   ├── ai.go           # AI feature commands
│   ├── creds.go        # Credential management
│   └── ...
├── features/            # VTOP feature implementations
│   ├── marks.go
│   ├── attendance.go
│   ├── ai.go           # AI data builder
│   └── ...
├── helpers/             # Utility functions
├── login/               # VTOP login logic
├── types/               # Type definitions
├── tests/               # Unit tests
├── ai/                  # AI features directory
│   ├── config.py       # AI configuration
│   ├── requirements.txt
│   ├── .env            # API keys (create from .env.example)
│   ├── fetch_vtop_data.py
│   ├── chatbot.py
│   ├── run_all_features.py
│   ├── features/       # 9 algorithmic AI features
│   ├── utils/          # AI utilities
│   ├── data/           # Data storage
│   └── gemini_features/ # Gemini-powered features
│       ├── career_advisor.py
│       ├── study_optimizer.py
│       └── performance_insights.py
└── website/             # Web interface
    ├── server.py       # Flask backend
    ├── index.html      # Frontend
    ├── styles.css
    └── script.js
```

### Building

```bash
# Development build
go build -o cli-top main.go

# Production build (optimized)
CGO_ENABLED=0 go build -trimpath -ldflags "-s -w" -o cli-top main.go

# Multi-platform build
GOOS=darwin GOARCH=arm64 go build -o cli-top-mac-arm64 main.go
GOOS=darwin GOARCH=amd64 go build -o cli-top-mac-intel main.go
GOOS=linux GOARCH=amd64 go build -o cli-top-linux main.go
GOOS=windows GOARCH=amd64 go build -o cli-top-windows.exe main.go
```

### Running Tests

```bash
# Go tests
go test ./...

# Python tests (if available)
cd ai
python3 -m pytest tests/
```

### Adding New Features

1. **VTOP Feature**: Add to `features/` and register in `cmd/start.go`
2. **AI Feature**: Add to `ai/features/` and update `run_all_features.py`
3. **Gemini Feature**: Add to `ai/gemini_features/` and register in `cmd/ai.go`

---

## 📝 Command Reference

### Complete Command List

```bash
# Authentication
./cli-top login          # Login to VTOP
./cli-top logout         # Clear stored credentials

# Academic Info
./cli-top profile        # Student profile
./cli-top marks          # View marks
./cli-top grades         # View grades  
./cli-top cgpa           # CGPA tracking
./cli-top attendance     # Attendance status

# Schedule
./cli-top timetable      # Class schedule
./cli-top exams          # Exam schedule
./cli-top calendar       # Generate ICS calendar

# Course Management
./cli-top course-page    # Download course materials
./cli-top syllabus       # Download syllabus
./cli-top da             # Digital assignments
./cli-top msg            # Class messages

# Administrative
./cli-top receipts       # Fee receipts
./cli-top library-dues   # Library dues
./cli-top hostel         # Hostel info
./cli-top leave          # Leave status
./cli-top nightslip      # Nightslip status
./cli-top facility       # Facility booking
./cli-top course-allocation # Course allocation

# AI Features (No API Key)
./cli-top ai export      # Export VTOP data
./cli-top ai run-all     # Run all AI features
./cli-top ai grade       # Grade predictions
./cli-top ai plan        # Study planner
./cli-top ai attendance  # Attendance analysis
./cli-top ai trend       # Performance trends

# Gemini AI (Requires API Key)
./cli-top ai chatbot     # Interactive AI chat
./cli-top ai career      # Career guidance
./cli-top ai study-plan  # Optimized study plan
./cli-top ai insights    # Performance insights
./cli-top ai study-guide # Study guide generator
./cli-top ai voice       # Voice assistant 🎙️

# Utility
./cli-top help           # Show help
./cli-top --version      # Show version
./cli-top --debug        # Enable debug mode
```

---

## 🎓 Tips & Best Practices

### For Students

1. **Run AI analysis weekly** to track performance trends
2. **Use the chatbot** for quick questions about your data
3. **Generate study plans** before exam weeks
4. **Monitor attendance** regularly to avoid shortage
5. **Export your data** periodically for backup

### For Developers

1. **Never commit** `cli-top-config.env` or `ai/.env`
2. **Test features** with debug mode: `--debug` flag
3. **Follow Go conventions** for new VTOP features
4. **Document AI features** with clear docstrings
5. **Update this guide** when adding features

---

## 📄 License

This project is for educational purposes only. Not affiliated with VIT.

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 📞 Support

For issues or questions:
- Check the [Troubleshooting](#troubleshooting) section
- Review command examples above
- Ensure all dependencies are installed
- Verify your Gemini API key (for AI features)

---

## 🎉 Credits

Built with:
- **Go** - CLI framework
- **Python** - AI features
- **Gemini AI** - Advanced insights
- **Flask** - Web backend
- Love for VIT students ❤️

---

**Made with ❤️ for VIT Students**

*Last Updated: October 2025*
