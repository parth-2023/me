# CLI-TOP Dev 2

**Complete VIT Academic Assistant with AI-Powered Insights**

![CLI-TOP](https://img.shields.io/badge/Go-1.23+-00ADD8?style=flat&logo=go)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python)
![Gemini](https://img.shields.io/badge/Gemini-AI-8E75B2?style=flat)

---

## 🚀 Quick Start

```bash
# 1. Build CLI
go build -o cli-top main.go

# 2. Install AI dependencies
pip3 install -r ai/requirements.txt

# 3. Login to VTOP
./cli-top login

# 4. Run features
./cli-top marks              # View marks
./cli-top ai run-all         # Run all AI analyses
./cli-top ai chatbot --fetch # Start AI chatbot
```

---

## ✨ Features

### 📊 VTOP Features (21)
Complete access to all VTOP data: marks, grades, attendance, timetable, exams, course materials, and more.

### 🤖 AI Features (9 - No API Key Required)
- Attendance buffer calculator
- Grade predictor
- CGPA impact analyzer
- Attendance recovery planner
- Exam readiness scorer
- Study time allocator
- Performance trend analyzer
- Grade target planner
- Weakness identifier

### ✨ Gemini AI Features (Requires API Key)
- **AI Chatbot** - Interactive assistant with full VTOP context
- **Career Advisor** - Personalized career guidance
- **Study Optimizer** - Generate optimized study plans
- **Performance Insights** - Deep analysis with recommendations
- **Study Guide Generator** - Comprehensive course study guides
- **Voice Assistant** 🎙️ - Voice-controlled access to ALL features (Gemini 2.5 Flash Live)

### 🌐 Web Interface
Beautiful dashboard to access all features through your browser.

---

## 📖 Documentation

**➡️ See [GUIDE.md](GUIDE.md) for complete documentation**

The guide includes:
- Detailed installation instructions
- Complete feature documentation
- Configuration guide
- Troubleshooting tips
- Development guide
- Full command reference

---

## 🏗️ Project Structure

```
cli-top-dev-2/
├── GUIDE.md              # Complete documentation
├── main.go               # CLI entry point
├── go.mod                # Go dependencies
├── cmd/                  # CLI commands
├── features/             # VTOP features
├── helpers/              # Utilities
├── login/                # VTOP authentication
├── types/                # Type definitions
├── tests/                # Tests
├── ai/                   # AI features
│   ├── features/        # 9 algorithmic AI features
│   ├── gemini_features/ # Gemini-powered features
│   ├── utils/           # AI utilities
│   ├── chatbot.py       # AI chatbot
│   ├── fetch_vtop_data.py
│   ├── run_all_features.py
│   ├── config.py
│   └── requirements.txt
└── website/              # Web interface
    ├── server.py
    ├── index.html
    ├── styles.css
    └── script.js
```

---

## ⚡ Quick Examples

### View Academic Data
```bash
./cli-top profile        # Your profile
./cli-top marks          # Current semester marks
./cli-top grades -s 2    # Semester 2 grades
./cli-top attendance     # Attendance status
```

### AI Analysis
```bash
# Run all AI features (recommended)
./cli-top ai run-all

# Individual features
./cli-top ai grade predict --course CSE1001 --fat 85
./cli-top ai plan --days 7
./cli-top ai attendance --course CSE1001
```

### Gemini AI (Requires API Key)
```bash
# Setup (one-time)
cp ai/.env.example ai/.env
nano ai/.env  # Add your Gemini API key

# Use features (powered by Gemini 2.5 Flash)
./cli-top ai chatbot              # Interactive chat
./cli-top ai career               # Career guidance
./cli-top ai study-plan           # Study plan
./cli-top ai insights             # Performance insights
./cli-top ai study-guide          # Study guide generator

# 🎙️ NEW: Voice Assistant (Gemini 2.5 Flash Live)
./cli-top ai voice                # Voice-controlled everything!
# Say: "Show my marks", "Run all AI", "Career advice", etc.
```

### Web Interface
```bash
cd website
python3 server.py
# Open http://localhost:5555
```

---

## 🔧 Requirements

- **Go 1.23+** - For CLI
- **Python 3.8+** - For AI features
- **VTOP Account** - VIT student credentials
- **Gemini API Key** (Optional) - For Gemini AI features (Gemini 2.5 Flash)
  - Get free key: [Google AI Studio](https://makersuite.google.com/app/apikey)
- **Speech Libraries** (Optional) - For voice assistant
  - `pip install SpeechRecognition pyttsx3 pyaudio`

---

## 📦 Installation

### macOS/Linux
```bash
# Clone and build
git clone <repo-url> cli-top-dev-2
cd cli-top-dev-2
go build -o cli-top main.go

# Install Python dependencies
pip3 install -r ai/requirements.txt

# First run
./cli-top login
```

### Windows
```bash
# Clone and build
git clone <repo-url> cli-top-dev-2
cd cli-top-dev-2
go build -o cli-top.exe main.go

# Install Python dependencies
pip install -r ai/requirements.txt

# First run
cli-top.exe login
```

---

## 🎯 Use Cases

### For Students
- **Daily**: Check attendance, view marks, download materials
- **Weekly**: Run AI analysis to track performance trends
- **Before Exams**: Generate study plans, check exam readiness
- **Career Planning**: Get personalized career guidance
- **Quick Questions**: Use AI chatbot for instant insights

### For Developers
- **Extend Features**: Add new VTOP or AI features
- **Customize AI**: Modify AI algorithms or add new analyses
- **Build Tools**: Use exported data for custom tools
- **Integrate**: Connect with other student tools

---

## 🛡️ Security

- Credentials are **encrypted** and stored locally
- **Never commits** credentials to version control
- API keys stored in `.env` (ignored by git)
- All data stays on your machine
- Web server runs locally only

---

## 🤝 Contributing

Contributions welcome! Please:
1. Read [GUIDE.md](GUIDE.md) for project structure
2. Test your changes thoroughly
3. Follow existing code style
4. Update documentation
5. Submit a pull request

---

## 📄 License

Educational purposes only. Not affiliated with VIT.

---

## 💬 Support

- 📖 Read [GUIDE.md](GUIDE.md) for detailed documentation
- 🐛 Report issues with error messages
- 💡 Suggest features via issues
- 🔍 Check troubleshooting section in guide

---

## 🌟 Highlights

- ✅ **21 VTOP Features** - Complete VTOP access
- ✅ **9 AI Features** - Work offline, no API key needed
- ✅ **6 Gemini Features** - Advanced AI with chatbot & voice
- ✅ **Voice Assistant** 🎙️ - Control everything with voice
- ✅ **Gemini 2.5 Flash** - Latest AI model
- ✅ **Web Interface** - Beautiful dashboard
- ✅ **CLI & Web** - Use however you prefer
- ✅ **Secure** - Encrypted credentials
- ✅ **Fast** - Go-powered CLI
- ✅ **Smart** - AI-powered insights

---

**Made with ❤️ for VIT Students**

**➡️ Get Started: Read [GUIDE.md](GUIDE.md)**
