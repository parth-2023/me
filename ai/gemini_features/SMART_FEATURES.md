# Smart Context-Aware Voice Features

## Overview

CLI-TOP's voice assistant now includes **intelligent multi-tool execution** that understands context and automatically runs multiple features to provide comprehensive analysis and advice.

## 🎯 What Are Smart Features?

Smart features use natural language understanding to:
1. **Understand your intent** from casual questions
2. **Execute multiple tools** automatically
3. **Aggregate results** from VTOP, AI features, and Gemini AI
4. **Provide actionable advice** using AI-powered analysis

Instead of running 3 separate commands, just ask one natural question!

---

## 📋 Available Smart Features

### 1️⃣ Attendance Advice - "Can I leave classes?"

**Trigger Phrases:**
- "Can I leave classes?"
- "Should I skip classes?"
- "Can I skip?"
- "Can I bunk?"
- "Should I attend?"

**What It Does:**
```
1. Fetches current attendance from VTOP
2. Calculates skip buffer for each subject (AI)
3. Generates personalized advice (Gemini AI)
```

**Example Output:**
```
Current Attendance:
✅ DBMS: 94.44% (Buffer: 7 classes)
⚠️  Compiler Design: 85.71% (Buffer: 3 classes)
❌ Networks Lab: 91.67% (Buffer: 2 classes)

AI Advice:
You can safely skip up to 3 classes in DBMS, but be cautious
with Compiler Design. Avoid missing Networks Lab - only 2 class
buffer remaining. Prioritize attending Compiler Design to maintain
safe attendance levels.
```

---

### 2️⃣ Performance Overview - "How am I doing?"

**Trigger Phrases:**
- "How am I doing?"
- "Am I doing well?"
- "My performance"

**What It Does:**
```
1. Shows CGPA and grade distribution
2. Analyzes performance trends (AI)
3. Provides insights and recommendations (Gemini AI)
```

**Example Output:**
```
Current CGPA: 8.41
Semester Performance:
• A+ Grades: 2 subjects
• A Grades: 3 subjects
• B+ Grades: 2 subjects

Performance Trends:
✅ Improving: Database Systems (+15%)
⚠️  Declining: Compiler Design (-10%)
📊 Stable: AI, Networks

Gemini Insights:
Your CGPA is strong. Focus on Compiler Design to prevent
further decline. Consider forming study groups for challenging
subjects. Target 90%+ in remaining assessments to push toward
8.5+ CGPA.
```

---

### 3️⃣ Focus Advisor - "What should I focus on?"

**Trigger Phrases:**
- "What should I focus on?"
- "What to study?"
- "Where to improve?"

**What It Does:**
```
1. Identifies weak subjects (AI)
2. Generates targeted study plan (Gemini AI)
```

**Example Output:**
```
Weak Areas Identified:
❌ Compiler Design: CAT1 50%, Low quiz scores
⚠️  Computer Networks: CAT1 59%, Missing DAs

Study Plan Generated:
Week 1-2: Compiler Design Fundamentals
• Topics: Lexical analysis, Parsing
• Resources: Lecture notes, DragonBook Ch 1-3
• Practice: 20 problems/week

Week 3: Computer Networks Catch-up
• Complete pending DAs
• Review CAT1 topics
```

---

### 4️⃣ Exam Prediction - "Will I pass?"

**Trigger Phrases:**
- "Will I pass?"
- "Can I pass?"
- "Am I exam ready?"

**What It Does:**
```
1. Calculates exam readiness scores (AI)
2. Predicts final grades based on current performance (AI)
3. Provides exam preparation advice (Gemini AI)
```

**Example Output:**
```
Exam Readiness Scores:
✅ DBMS: 85% ready (Strong preparation)
⚠️  Compiler Design: 62% ready (Needs focus)
❌ Networks Lab: 45% ready (High risk)

Grade Predictions:
• DBMS: Predicted A (85-90%)
• Compiler Design: Predicted B+ (75-80%)
• Networks Lab: Predicted B (70-75%)

AI Exam Advice:
You're on track to pass all subjects. Focus intensive study on
Networks Lab (highest risk). For Compiler Design, prioritize
CAT2 preparation. DBMS is your strongest - use it to boost CGPA.
Allocate 60% study time to weak subjects, 40% to maintaining
strong ones.
```

---

## 🚀 How to Use

### Method 1: Voice Input (with speech libraries)

```bash
# Install speech dependencies
brew install portaudio
pip install SpeechRecognition pyttsx3 pyaudio

# Run voice assistant
./cli-top ai voice

# Speak your question
🎤 "Can I leave classes?"
```

### Method 2: Text Input (no dependencies needed)

```bash
# Run voice assistant
./cli-top ai voice

# Type your question
You: Can I leave classes?
```

---

## 🔧 Technical Implementation

### Architecture

```
User Input → Intent Parser → Multi-Tool Executor → AI Aggregator → Output
```

### Intent Parser

Uses pattern matching to detect smart commands:

```python
def parse_command(self, user_input):
    # Attendance advice
    if 'can i leave' in user_input or 'should i skip' in user_input:
        return 'smart', 'attendance_advice'
    
    # Performance overview
    if 'how am i doing' in user_input:
        return 'smart', 'performance_overview'
    
    # ... more patterns
```

### Multi-Tool Executor

Chains multiple commands automatically:

```python
def execute_smart_command(self, smart_type):
    if smart_type == 'attendance_advice':
        # Run VTOP attendance
        self.execute_vtop_feature('attendance')
        
        # Run AI attendance calculator
        self.execute_ai_feature('attendance calculator')
        
        # Generate Gemini advice
        response = self.model.generate_content(advice_prompt)
        self.speak(response.text)
```

---

## 📊 Comparison: Smart vs Manual

### Manual Approach (OLD)
```bash
./cli-top attendance
# ... check attendance manually

./cli-top ai attendance-calculator
# ... analyze buffer manually

./cli-top ai chatbot
You: Based on this attendance, can I skip classes?
# ... wait for response
```

**Time:** ~2-3 minutes

### Smart Approach (NEW)
```bash
./cli-top ai voice
You: Can I leave classes?
```

**Time:** ~20 seconds (automatic)

---

## 💡 Tips for Best Results

### 1. Use Natural Language
- ✅ "Can I skip classes today?"
- ❌ "execute attendance calculator"

### 2. Be Specific When Needed
- ✅ "What should I focus on for exams?"
- ✅ "Am I doing well in my courses?"

### 3. Combine with Regular Commands
Smart features complement regular commands:
```
You: Can I leave classes?
[Smart analysis runs]

You: Show me detailed syllabus
[Regular command runs]
```

### 4. Voice Mode for Convenience
When driving or busy:
```
🎤 "Hey, am I exam ready?"
🔊 "Your exam readiness scores are..."
```

---

## 🔍 How It Differs from Regular Commands

| Feature | Regular Commands | Smart Features |
|---------|-----------------|----------------|
| **Input** | Exact command names | Natural questions |
| **Tools** | Single tool per command | Multiple tools automatically |
| **Output** | Raw data | Aggregated + AI advice |
| **Workflow** | Manual chaining | Automatic execution |
| **Time** | 2-3 minutes | 20-30 seconds |

---

## 🛠️ Customization

### Adding New Smart Patterns

Edit `voice_assistant.py`:

```python
# In parse_command():
if any(phrase in user_input_lower for phrase in ['new pattern', 'another phrase']):
    return 'smart', 'new_smart_feature'

# Add handler:
def execute_smart_command(self, smart_type):
    if smart_type == 'new_smart_feature':
        # Run your tools
        self.execute_vtop_feature('marks')
        self.execute_ai_feature('grade predictor')
        # Generate advice
```

### Custom Advice Prompts

Modify advice generation:

```python
advice_prompt = """
You are an academic advisor. Provide advice on:
1. Custom point
2. Another point
3. Specific recommendation

Keep it under 100 words.
"""
```

---

## 🧪 Testing

Run test suite:

```bash
cd ai/gemini_features
python3 test_smart_features.py
```

Expected output:
```
✅ PASS: 'Can I leave classes?' → attendance_advice
✅ PASS: 'How am I doing?' → performance_overview
✅ PASS: 'What should I focus on?' → focus_advisor
✅ PASS: 'Will I pass?' → exam_prediction
```

---

## 📝 Known Limitations

1. **Gemini API Required:** Smart advice needs Google API key
2. **Network Needed:** Online for Gemini AI responses
3. **Pattern Matching:** Not full NLP (but covers common phrases)
4. **Voice Recognition:** Requires quiet environment for accurate recognition

---

## 🎯 Future Enhancements

- [ ] Add more smart patterns (timetable conflicts, DA reminders)
- [ ] Implement true NLP with fine-tuned models
- [ ] Offline mode with cached advice
- [ ] Multi-language support
- [ ] Voice command history
- [ ] Proactive notifications ("Your attendance is dropping!")

---

## 📚 Related Documentation

- [VOICE_FEATURES.md](./VOICE_FEATURES.md) - Complete voice assistant guide
- [AI_FEATURES.md](../AI_FEATURES.md) - Individual AI features
- [README.md](../README.md) - AI features overview

---

## ✅ Summary

Smart features transform CLI-TOP from a **command-line tool** into an **intelligent academic assistant**:

✅ Natural language understanding  
✅ Multi-tool automation  
✅ AI-powered advice  
✅ Time-saving workflow  
✅ Voice-enabled (optional)  

**Result:** Ask one question, get complete analysis + actionable advice!
