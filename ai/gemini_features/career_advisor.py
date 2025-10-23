#!/usr/bin/env python3
"""
Career Advisor - AI-powered career guidance based on academic performance
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

def analyze_career_path(vtop_data):
    """Generate career recommendations based on academic performance"""
    
    if not GOOGLE_API_KEY:
        return "❌ Error: GOOGLE_API_KEY not configured"
    
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel(GEMINI_MODEL)
    
    # Build prompt with student data
    prompt = f"""
As a career advisor for VIT students, analyze this student's academic profile and provide personalized career guidance.

STUDENT PROFILE:
- Registration: {vtop_data.get('reg_no', 'N/A')}
- Semester: {vtop_data.get('semester', 'N/A')}
- CGPA: {vtop_data.get('cgpa', 'N/A')}

COURSE PERFORMANCE:
"""
    
    for course in vtop_data.get('marks', []):
        prompt += f"\n{course.get('course_code', 'N/A')} ({course.get('course_name', 'N/A')}): {course.get('total', 'N/A')}/100"
    
    prompt += """

Please provide:
1. **Academic Strengths Analysis**: Identify the student's strongest subjects and skill areas
2. **Career Path Recommendations**: Suggest 3-5 specific career paths that align with their strengths
3. **Skill Development Plan**: Key skills to develop for each recommended career path
4. **Industry Trends**: Current market demand for these career paths
5. **Next Steps**: Actionable steps the student can take (certifications, projects, internships)
6. **Company Recommendations**: Types of companies or specific companies that match their profile

Be specific, data-driven, and encouraging. Focus on realistic and achievable career goals.
"""
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Error: {str(e)}"

def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python career_advisor.py <vtop_data.json>")
        sys.exit(1)
    
    with open(sys.argv[1], 'r') as f:
        vtop_data = json.load(f)
    
    print("=" * 70)
    print("🎯 CAREER ADVISOR - AI-POWERED CAREER GUIDANCE")
    print("=" * 70)
    print()
    
    advice = analyze_career_path(vtop_data)
    print(advice)
    print()
    print("=" * 70)
    print("💡 Powered by Gemini AI")
    print("=" * 70)

if __name__ == '__main__':
    main()
