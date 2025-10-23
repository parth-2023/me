#!/usr/bin/env python3
"""
Feature A: Semester Insights Analyzer
Analyzes current semester performance using Gemini AI
"""

import json
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import google.generativeai as genai
from config import GOOGLE_API_KEY, GEMINI_MODEL, TEMPERATURE, OUTPUT_DIR


def load_vtop_data(file_path):
    """Load VTOP exported data"""
    with open(file_path, 'r') as f:
        return json.load(f)


def format_course_data(vtop_data):
    """Format course data for Gemini prompt"""
    courses_text = []
    
    for course in vtop_data.get('marks', []):
        course_code = course.get('course_code', '')
        course_name = course.get('course_name', '')
        
        # Get marks
        cat1 = course.get('cat1', 0)
        cat2 = course.get('cat2', 0)
        da = course.get('da', 0)
        quiz1 = course.get('quiz1', 0)
        quiz2 = course.get('quiz2', 0)
        
        # Calculate internal total
        internal_total = cat1 + cat2 + da + quiz1 + quiz2
        internal_percentage = (internal_total / 60) * 100 if internal_total > 0 else 0
        
        course_text = f"""
{course_code}: {course_name}
  - CAT1: {cat1}/15
  - CAT2: {cat2}/15
  - DA: {da}/10
  - Quiz1: {quiz1}/10
  - Quiz2: {quiz2}/10
  - Internal Total: {internal_total:.1f}/60 ({internal_percentage:.1f}%)
"""
        courses_text.append(course_text)
    
    # Get attendance data
    attendance_text = []
    for att in vtop_data.get('attendance', []):
        course_code = att.get('course_code', '')
        attended = att.get('attended', 0)
        total = att.get('total', 0)
        percentage = (attended / total * 100) if total > 0 else 0
        
        attendance_text.append(f"{course_code}: {percentage:.1f}% ({attended}/{total})")
    
    return '\n'.join(courses_text), '\n'.join(attendance_text)


def generate_insights(vtop_data):
    """Generate semester insights using Gemini"""
    
    if not GOOGLE_API_KEY:
        return "❌ Error: GOOGLE_API_KEY not configured. Please set it in .env file."
    
    # Configure Gemini
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel(GEMINI_MODEL)
    
    # Format data
    courses_text, attendance_text = format_course_data(vtop_data)
    student_cgpa = vtop_data.get('cgpa', 'N/A')
    semester = vtop_data.get('semester', 'Current Semester')
    
    # Create prompt
    prompt = f"""You are an academic advisor for VIT (Vellore Institute of Technology) students. Analyze the following student's performance and provide detailed insights.

STUDENT PROFILE:
- Current CGPA: {student_cgpa}
- Semester: {semester}

COURSE PERFORMANCE (Internal Marks out of 60):
{courses_text}

ATTENDANCE RECORDS:
{attendance_text}

VIT GRADING SYSTEM:
- Internal marks: 60 (CAT1: 15, CAT2: 15, DA: 10, Quiz1: 10, Quiz2: 10)
- FAT (Final Assessment Test): 40
- Total: 100
- Grades: S (90+), A (80-89), B (70-79), C (60-69), D (50-59), F (<50)
- VIT requires 75% minimum attendance

Please provide a comprehensive analysis with:

1. **Overall Semester Health**: Rate the semester performance (Excellent/Good/Average/Needs Improvement)

2. **Subject-wise Analysis**:
   - **Strong Subjects**: Which courses are performing well (>80% internal)?
   - **Average Subjects**: Which courses are okay but need attention (70-80%)?
   - **Weak Subjects**: Which courses need urgent improvement (<70%)?

3. **Attendance Status**:
   - Identify any attendance concerns (<75%)
   - Subjects with good attendance buffer

4. **Key Insights**:
   - Patterns in performance (consistent/inconsistent)
   - Strengths and weaknesses identified
   - Any concerning trends

5. **Actionable Recommendations**:
   - Priority subjects to focus on
   - Specific study strategies
   - Time management suggestions
   - How to improve weak areas

Keep the tone encouraging but honest. Focus on actionable advice that a VIT student can implement immediately.
"""
    
    try:
        print("🤖 Generating semester insights with Gemini AI...")
        response = model.generate_content(
            prompt,
            generation_config={
                'temperature': TEMPERATURE,
                'max_output_tokens': 2048
            }
        )
        
        return response.text
    
    except Exception as e:
        return f"❌ Error generating insights: {str(e)}"


def main():
    if len(sys.argv) < 2:
        print("Usage: python semester_insights.py <vtop_data.json>")
        sys.exit(1)
    
    vtop_file = sys.argv[1]
    
    if not Path(vtop_file).exists():
        print(f"❌ Error: File not found: {vtop_file}")
        sys.exit(1)
    
    print("="*80)
    print("SEMESTER INSIGHTS ANALYZER (Powered by Gemini AI)")
    print("="*80)
    print()
    
    # Load data
    vtop_data = load_vtop_data(vtop_file)
    
    # Generate insights
    insights = generate_insights(vtop_data)
    
    # Display
    print(insights)
    print()
    
    # Save to file
    output_file = OUTPUT_DIR / 'semester_insights.txt'
    with open(output_file, 'w') as f:
        f.write("="*80 + "\n")
        f.write("SEMESTER INSIGHTS ANALYZER (Powered by Gemini AI)\n")
        f.write("="*80 + "\n\n")
        f.write(insights)
        f.write("\n\n" + "="*80 + "\n")
        f.write("* AI-generated insights. Results may vary from actual outcomes.\n")
        f.write("="*80 + "\n")
    
    print(f"✓ Insights saved to: {output_file}")
    print()


if __name__ == "__main__":
    main()
