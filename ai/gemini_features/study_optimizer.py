#!/usr/bin/env python3
"""
Study Optimizer - Personalized study plan generator using Gemini AI
"""

import json
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import google.generativeai as genai
    from config import GOOGLE_API_KEY, GEMINI_MODEL
except ImportError:
    print("FAIL Error: google-generativeai not installed")
    print("   Run: pip install -r ai/requirements.txt")
    sys.exit(1)

def generate_study_plan(vtop_data, days_until_exams=30, daily_hours=6):
    """Generate optimized study plan"""
    
    if not GOOGLE_API_KEY:
        return "FAIL Error: GOOGLE_API_KEY not configured"
    
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel(GEMINI_MODEL)
    
    prompt = f"""
As a study optimization expert, create a personalized study plan for this VIT student.

STUDENT PROFILE:
- CGPA: {vtop_data.get('cgpa', 'N/A')}
- Semester: {vtop_data.get('semester', 'N/A')}
- Days until exams: {days_until_exams}
- Available study hours per day: {daily_hours}

COURSES AND CURRENT PERFORMANCE:
"""
    
    for course in vtop_data.get('marks', []):
        prompt += f"\n{course.get('course_code', 'N/A')} - {course.get('course_name', 'N/A')}:"
        prompt += f"\n  Current Total: {course.get('total', 'N/A')}/100"
        prompt += f"\n  CAT1: {course.get('cat1', 'N/A')}, CAT2: {course.get('cat2', 'N/A')}, FAT: {course.get('fat', 'N/A')}"
    
    prompt += "\n\nATTENDANCE STATUS:\n"
    for att in vtop_data.get('attendance', []):
        prompt += f"{att.get('course_code', 'N/A')}: {att.get('attendance_percentage', 'N/A')}%\n"
    
    prompt += f"""

UPCOMING EXAMS:
"""
    for exam in vtop_data.get('exams', []):
        prompt += f"{exam.get('course_code', 'N/A')} - {exam.get('exam_type', 'N/A')}: {exam.get('date', 'N/A')}\n"
    
    prompt += """

Create a detailed study plan that includes:

1. **Priority Matrix**: Rank courses by urgency and importance (based on marks and exam dates)
2. **Daily Schedule**: Hour-by-hour breakdown for optimal study times
3. **Weekly Goals**: Specific topics/chapters to complete each week
4. **Study Techniques**: Best methods for each subject (active recall, spaced repetition, etc.)
5. **Break Strategy**: When and how to take effective breaks
6. **Resource Recommendations**: Best study materials or online resources for weak areas
7. **Mock Test Schedule**: When to practice tests for each subject
8. **Revision Plan**: Last week intensive revision strategy

Be practical, specific, and time-bound. Consider the student's current performance and upcoming deadlines.
"""
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"FAIL Error: {str(e)}"

def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python study_optimizer.py <vtop_data.json> [days_until_exams] [daily_hours]")
        sys.exit(1)
    
    days = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    hours = int(sys.argv[3]) if len(sys.argv) > 3 else 6
    
    with open(sys.argv[1], 'r') as f:
        vtop_data = json.load(f)
    
    print("=" * 70)
    print("INFO: STUDY OPTIMIZER - AI-POWERED STUDY PLAN GENERATOR")
    print("=" * 70)
    print()
    print(f"Planning for {days} days with {hours} hours/day")
    print()
    
    plan = generate_study_plan(vtop_data, days, hours)
    print(plan)
    print()
    print("=" * 70)
    print("INFO: Powered by Gemini AI")
    print("=" * 70)

if __name__ == '__main__':
    main()
