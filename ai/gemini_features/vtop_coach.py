#!/usr/bin/env python3
"""
Feature C: VTOP Motivational Coach
A fun AI feature that motivates students based on their performance
"""

import json
import sys
from pathlib import Path
import random

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import google.generativeai as genai
from config import GOOGLE_API_KEY, GEMINI_MODEL, TEMPERATURE, OUTPUT_DIR


def load_vtop_data(file_path):
    """Load VTOP exported data"""
    with open(file_path, 'r') as f:
        return json.load(f)


def analyze_performance(vtop_data):
    """Analyze overall performance for coaching"""
    total_subjects = len(vtop_data.get('marks', []))
    
    strong_count = 0
    weak_count = 0
    total_internal_pct = 0
    
    attendance_issues = []
    attendance_perfect = []
    
    for course in vtop_data.get('marks', []):
        # Calculate internal percentage
        cat1 = course.get('cat1', 0)
        cat2 = course.get('cat2', 0)
        da = course.get('da', 0)
        quiz1 = course.get('quiz1', 0)
        quiz2 = course.get('quiz2', 0)
        
        internal_total = cat1 + cat2 + da + quiz1 + quiz2
        internal_pct = (internal_total / 60) * 100
        total_internal_pct += internal_pct
        
        if internal_pct >= 80:
            strong_count += 1
        elif internal_pct < 70:
            weak_count += 1
    
    # Check attendance
    for att in vtop_data.get('attendance', []):
        course_code = att.get('course_code', '')
        attended = att.get('attended', 0)
        total = att.get('total', 0)
        percentage = (attended / total * 100) if total > 0 else 0
        
        if percentage < 75:
            attendance_issues.append((course_code, percentage))
        elif percentage >= 95:
            attendance_perfect.append((course_code, percentage))
    
    avg_internal_pct = total_internal_pct / total_subjects if total_subjects > 0 else 0
    
    return {
        'total_subjects': total_subjects,
        'strong_count': strong_count,
        'weak_count': weak_count,
        'avg_internal_pct': avg_internal_pct,
        'attendance_issues': attendance_issues,
        'attendance_perfect': attendance_perfect,
        'cgpa': vtop_data.get('cgpa', 0)
    }


def generate_motivational_message(vtop_data, stats, mode='motivational'):
    """Generate motivational or roast message using Gemini"""
    
    if not GOOGLE_API_KEY:
        return "❌ Error: GOOGLE_API_KEY not configured. Please set it in .env file."
    
    # Configure Gemini
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel(GEMINI_MODEL)
    
    # Build context
    context = f"""
Student Statistics:
- CGPA: {stats['cgpa']}
- Total Subjects: {stats['total_subjects']}
- Strong Subjects (80%+): {stats['strong_count']}
- Weak Subjects (<70%): {stats['weak_count']}
- Average Internal: {stats['avg_internal_pct']:.1f}%
- Attendance Issues (<75%): {len(stats['attendance_issues'])} subjects
- Perfect Attendance (95%+): {len(stats['attendance_perfect'])} subjects
"""
    
    if mode == 'roast':
        prompt = f"""You are a friendly but hilariously honest AI roast master for VIT students. 

{context}

Roast this student's academic performance in a funny, witty, but ultimately encouraging way. Rules:
1. Be SAVAGE but never mean or discouraging
2. Use Gen-Z humor and memes references
3. Point out the funny contradictions (like perfect attendance but failing grades, or vice versa)
4. End with an actually helpful motivational twist
5. Keep it under 300 words
6. Use emojis generously 😂

Example style: "Bro really said 'I have 95% attendance' and then proceeded to score 60% internals 💀 That's not character development, that's a plot hole!"

Now roast this student (but make them laugh and motivate them at the end):
"""
    
    elif mode == 'motivational':
        prompt = f"""You are an energetic, supportive AI motivational coach for VIT students.

{context}

Create an uplifting, motivational message that:
1. Celebrates their wins (even small ones)
2. Acknowledges challenges without dwelling on them
3. Provides 3 specific, actionable tips for improvement
4. Uses powerful, inspiring language
5. Includes a memorable quote or mantra
6. Keep it under 300 words
7. Use motivational emojis ⚡🔥💪

Focus on growth mindset and VIT-specific advice. Make them feel like they can ace the FAT!
"""
    
    else:  # fun facts
        prompt = f"""You are a fun, quirky AI that shares interesting academic facts and study tips.

{context}

Based on their performance, share:
1. A fun fact about learning/memory/studying
2. A lesser-known VIT hack or tip
3. A study technique that might help them
4. A motivational science fact
5. End with an encouraging message

Keep it fun, informative, and under 250 words. Use emojis! 🧠✨
"""
    
    try:
        response = model.generate_content(
            prompt,
            generation_config={
                'temperature': 0.9,  # Higher creativity for fun messages
                'max_output_tokens': 512
            }
        )
        
        return response.text
    
    except Exception as e:
        return f"❌ Error generating message: {str(e)}"


def main():
    if len(sys.argv) < 2:
        print("Usage: python vtop_coach.py <vtop_data.json> [mode]")
        print("Modes: motivational (default), roast, funfacts")
        sys.exit(1)
    
    vtop_file = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else 'motivational'
    
    if not Path(vtop_file).exists():
        print(f"❌ Error: File not found: {vtop_file}")
        sys.exit(1)
    
    mode_emojis = {
        'motivational': '💪 MOTIVATIONAL COACH',
        'roast': '🔥 ROAST MODE ACTIVATED',
        'funfacts': '🧠 VTOP FUN FACTS'
    }
    
    print("="*80)
    print(mode_emojis.get(mode, '🎮 VTOP COACH'))
    print("Powered by Gemini AI")
    print("="*80)
    print()
    
    # Load data
    vtop_data = load_vtop_data(vtop_file)
    
    # Analyze performance
    print("📊 Analyzing your performance...")
    stats = analyze_performance(vtop_data)
    
    # Generate message
    print(f"🤖 Generating {mode} message...\n")
    message = generate_motivational_message(vtop_data, stats, mode)
    
    # Display
    print(message)
    print()
    
    # Save to file
    output_file = OUTPUT_DIR / f'vtop_coach_{mode}.txt'
    
    with open(output_file, 'w') as f:
        f.write("="*80 + "\n")
        f.write(f"{mode_emojis.get(mode, 'VTOP COACH')}\n")
        f.write("Powered by Gemini AI\n")
        f.write("="*80 + "\n\n")
        f.write(message)
        f.write("\n\n" + "="*80 + "\n")
        f.write("* AI-generated for entertainment and motivation.\n")
        f.write("="*80 + "\n")
    
    print(f"✓ Message saved to: {output_file}")
    print()
    
    # Show quick stats
    print("📊 Quick Stats:")
    print(f"   CGPA: {stats['cgpa']}")
    print(f"   Average Internal: {stats['avg_internal_pct']:.1f}%")
    print(f"   Strong Subjects: {stats['strong_count']}/{stats['total_subjects']}")
    print(f"   Needs Attention: {stats['weak_count']}/{stats['total_subjects']}")
    print()


if __name__ == "__main__":
    main()
