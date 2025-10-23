#!/usr/bin/env python3
"""
Performance Insights - Deep analysis of academic performance using Gemini
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import google.generativeai as genai
    from config import GOOGLE_API_KEY, GEMINI_MODEL
except ImportError:
    print("❌ Error: google-generativeai not installed")
    print("   Run: pip install -r ai/requirements.txt")
    sys.exit(1)

def analyze_performance(vtop_data):
    """Generate comprehensive performance analysis"""
    
    if not GOOGLE_API_KEY:
        return "❌ Error: GOOGLE_API_KEY not configured"
    
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel(GEMINI_MODEL)
    
    prompt = f"""
As an academic performance analyst, provide a comprehensive analysis of this student's performance.

STUDENT PROFILE:
- Registration: {vtop_data.get('reg_no', 'N/A')}
- Semester: {vtop_data.get('semester', 'N/A')}
- CGPA: {vtop_data.get('cgpa', 'N/A')}

DETAILED COURSE PERFORMANCE:
"""
    
    for course in vtop_data.get('marks', []):
        prompt += f"\n{course.get('course_code', 'N/A')} - {course.get('course_name', 'N/A')}:"
        prompt += f"\n  Credits: {course.get('credits', 'N/A')}"
        prompt += f"\n  CAT1: {course.get('cat1', 'N/A')}, CAT2: {course.get('cat2', 'N/A')}"
        prompt += f"\n  Quiz: {course.get('quiz', 'N/A')}, Assignment: {course.get('assignment', 'N/A')}"
        prompt += f"\n  FAT: {course.get('fat', 'N/A')}, Total: {course.get('total', 'N/A')}/100"
    
    prompt += "\n\nATTENDANCE PATTERN:\n"
    for att in vtop_data.get('attendance', []):
        prompt += f"{att.get('course_code', 'N/A')}: {att.get('attendance_percentage', 'N/A')}% "
        prompt += f"({att.get('attended', 0)}/{att.get('total_classes', 0)})\n"
    
    prompt += """

Provide a detailed analysis with:

1. **Overall Performance Assessment**: 
   - Current standing (excellent/good/average/needs improvement)
   - Comparison with typical VIT standards
   - Grade prediction for this semester

2. **Strengths Identification**:
   - Best performing subjects
   - Consistent performance patterns
   - Strong assessment types (CAT1/CAT2/Quiz/Assignment/FAT)

3. **Areas of Concern**:
   - Underperforming subjects
   - Weak assessment types
   - Attendance issues
   - Declining trends

4. **Performance Patterns**:
   - Theory vs Practical performance
   - Core vs Elective performance
   - Assessment type preferences
   - Study consistency

5. **Specific Recommendations**:
   - Which subjects need immediate attention
   - Study approach changes needed
   - Time management improvements
   - Resource utilization suggestions

6. **Motivational Insights**:
   - Positive achievements to celebrate
   - Realistic improvement goals
   - Encouragement based on strengths

7. **Risk Analysis**:
   - Subjects at risk of poor grades
   - Attendance risks
   - Overall CGPA impact

Be honest but encouraging. Provide specific, actionable insights with numbers and comparisons.
"""
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Error: {str(e)}"

def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python performance_insights.py <vtop_data.json>")
        sys.exit(1)
    
    with open(sys.argv[1], 'r') as f:
        vtop_data = json.load(f)
    
    print("=" * 70)
    print("📊 PERFORMANCE INSIGHTS - COMPREHENSIVE ACADEMIC ANALYSIS")
    print("=" * 70)
    print()
    
    analysis = analyze_performance(vtop_data)
    print(analysis)
    print()
    print("=" * 70)
    print("💡 Powered by Gemini AI")
    print("=" * 70)

if __name__ == '__main__':
    main()
