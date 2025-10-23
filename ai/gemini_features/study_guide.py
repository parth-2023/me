#!/usr/bin/env python3
"""
Feature B: Personalized Study Guide Generator
Fetches VIT syllabus and creates personalized study plans
"""

import json
import sys
from pathlib import Path
import requests
from bs4 import BeautifulSoup

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import google.generativeai as genai
from config import GOOGLE_API_KEY, GEMINI_MODEL, TEMPERATURE, OUTPUT_DIR


def load_vtop_data(file_path):
    """Load VTOP exported data"""
    with open(file_path, 'r') as f:
        return json.load(f)


def find_subject_marks(vtop_data, subject_name):
    """Find marks for a specific subject"""
    subject_name_lower = subject_name.lower()
    
    for course in vtop_data.get('marks', []):
        course_name = course.get('course_name', '').lower()
        course_code = course.get('course_code', '').lower()
        
        if subject_name_lower in course_name or subject_name_lower in course_code:
            return course
    
    return None


def search_vit_syllabus(subject_name):
    """Search for VIT syllabus online"""
    search_query = f"VIT Vellore {subject_name} syllabus filetype:pdf"
    search_url = f"https://www.google.com/search?q={requests.utils.quote(search_query)}"
    
    try:
        # Add headers to mimic browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # For demo purposes, return generic syllabus structure
        # In production, you might want to scrape actual VIT pages
        
        return f"""
VIT Syllabus for {subject_name}:

Note: This is a generic template. For actual syllabus, please refer to VTOP or VIT official resources.

Typical Course Structure:
- Unit 1: Fundamentals and Introduction
- Unit 2: Core Concepts and Theory
- Unit 3: Advanced Topics
- Unit 4: Applications and Case Studies
- Unit 5: Integration and Best Practices

Assessment:
- CAT1 (15 marks): Units 1-2
- CAT2 (15 marks): Units 3-4
- FAT (40 marks): All units with focus on Units 4-5
- Digital Assignments (10 marks)
- Quizzes (20 marks combined)
"""
    
    except Exception as e:
        return f"Could not fetch syllabus automatically. Error: {str(e)}"


def generate_study_guide(subject_name, subject_marks, syllabus_content, vtop_data):
    """Generate personalized study guide using Gemini"""
    
    if not GOOGLE_API_KEY:
        return "❌ Error: GOOGLE_API_KEY not configured. Please set it in .env file."
    
    # Configure Gemini
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel(GEMINI_MODEL)
    
    # Extract current performance
    if subject_marks:
        cat1 = subject_marks.get('cat1', 0)
        cat2 = subject_marks.get('cat2', 0)
        da = subject_marks.get('da', 0)
        quiz1 = subject_marks.get('quiz1', 0)
        quiz2 = subject_marks.get('quiz2', 0)
        internal_total = cat1 + cat2 + da + quiz1 + quiz2
        internal_pct = (internal_total / 60) * 100
        
        performance_text = f"""
Current Performance in {subject_name}:
- CAT1: {cat1}/15
- CAT2: {cat2}/15
- DA: {da}/10
- Quiz1: {quiz1}/10
- Quiz2: {quiz2}/10
- Internal Total: {internal_total:.1f}/60 ({internal_pct:.1f}%)
"""
    else:
        performance_text = f"No performance data available for {subject_name}"
    
    # Create prompt
    prompt = f"""You are an expert VIT academic tutor. Create a personalized study guide for a student.

SUBJECT: {subject_name}

STUDENT'S CURRENT PERFORMANCE:
{performance_text}

COURSE SYLLABUS:
{syllabus_content}

VIT GRADING CONTEXT:
- Internal: 60 marks (already {internal_total if subject_marks else 0}/60 completed)
- FAT (Final Assessment): 40 marks (upcoming)
- Target: Aim for A grade (80%+) or S grade (90%+)

Please create a comprehensive study guide with:

1. **Performance Analysis**:
   - Identify which assessment types the student excels at
   - Identify which areas need improvement
   - Calculate what FAT score is needed for A and S grades

2. **Syllabus-based Study Plan**:
   - Break down each unit into key topics
   - Identify high-weightage topics for FAT
   - Mark topics likely tested based on VIT patterns

3. **Week-by-Week Study Schedule** (4 weeks to FAT):
   - Week 1: What to cover
   - Week 2: What to cover
   - Week 3: What to cover
   - Week 4: Revision and practice

4. **Focus Areas**:
   - Topics to prioritize (high weightage + student weakness)
   - Concepts to master vs just understand
   - Common VIT question patterns

5. **Study Resources & Techniques**:
   - Recommended resources (YouTube channels, websites)
   - Study techniques for this subject
   - Practice problem sources

6. **Exam Strategy**:
   - How to approach FAT
   - Time management during exam
   - Common mistakes to avoid

Make it actionable, specific to VIT's exam patterns, and encouraging. The student should know exactly what to study each week.
"""
    
    try:
        print(f"🤖 Generating personalized study guide for {subject_name}...")
        response = model.generate_content(
            prompt,
            generation_config={
                'temperature': TEMPERATURE,
                'max_output_tokens': 2048
            }
        )
        
        return response.text
    
    except Exception as e:
        return f"❌ Error generating study guide: {str(e)}"


def main():
    if len(sys.argv) < 3:
        print("Usage: python study_guide.py <vtop_data.json> <subject_name>")
        print('Example: python study_guide.py /tmp/vtop_data.json "Database Systems"')
        sys.exit(1)
    
    vtop_file = sys.argv[1]
    subject_name = sys.argv[2]
    
    if not Path(vtop_file).exists():
        print(f"❌ Error: File not found: {vtop_file}")
        sys.exit(1)
    
    print("="*80)
    print(f"PERSONALIZED STUDY GUIDE: {subject_name}")
    print("Powered by Gemini AI")
    print("="*80)
    print()
    
    # Load data
    vtop_data = load_vtop_data(vtop_file)
    
    # Find subject marks
    subject_marks = find_subject_marks(vtop_data, subject_name)
    
    if not subject_marks:
        print(f"⚠️  Warning: Could not find exact match for '{subject_name}'")
        print("   Available courses:")
        for course in vtop_data.get('marks', []):
            print(f"     - {course.get('course_name', '')} ({course.get('course_code', '')})")
        print()
    
    # Search for syllabus
    print("📚 Fetching VIT syllabus information...")
    syllabus_content = search_vit_syllabus(subject_name)
    print()
    
    # Generate study guide
    study_guide = generate_study_guide(subject_name, subject_marks, syllabus_content, vtop_data)
    
    # Display
    print(study_guide)
    print()
    
    # Save to file
    safe_filename = subject_name.replace(' ', '_').replace('/', '_')
    output_file = OUTPUT_DIR / f'study_guide_{safe_filename}.txt'
    
    with open(output_file, 'w') as f:
        f.write("="*80 + "\n")
        f.write(f"PERSONALIZED STUDY GUIDE: {subject_name}\n")
        f.write("Powered by Gemini AI\n")
        f.write("="*80 + "\n\n")
        f.write(study_guide)
        f.write("\n\n" + "="*80 + "\n")
        f.write("* AI-generated study guide. Adapt to your learning style.\n")
        f.write("* Always refer to official VIT syllabus for accurate information.\n")
        f.write("="*80 + "\n")
    
    print(f"✓ Study guide saved to: {output_file}")
    print()


if __name__ == "__main__":
    main()
