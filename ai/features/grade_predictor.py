#!/usr/bin/env python3
"""
Complete Grade Prediction Pipeline

1. Predict missing internal marks (CAT2, DA, Quizzes)
2. Calculate total internal marks
3. Predict grades using historical patterns
4. Show FAT requirements for target grades
"""

import json
import sys
from pathlib import Path

# Simple logger
def log_info(msg):
    print(f"ℹ {msg}")

def log_success(msg):
    print(f"✓ {msg}")

def log_warning(msg):
    print(f"⚠ {msg}")


def categorize_subject_type(course_code: str, course_name: str) -> str:
    """Categorize subject into types."""
    course_name_upper = course_name.upper()
    course_code_upper = course_code.upper()
    
    # LAB subjects - ends with P or contains Lab
    if course_code.endswith('P') or 'LAB' in course_name_upper:
        return "LAB"
    
    # SOFT_SKILL subjects - BSTS codes or specific names
    if (course_code.startswith('BSTS') or 
        'QUALITATIVE' in course_name_upper or
        'SOFT SKILL' in course_name_upper or
        'COMPETITIVE CODING' in course_name_upper or
        'ADVANCED COMPETITIVE CODING' in course_name_upper):
        return "SOFT_SKILL"
    
    # MATH subjects
    if (course_code.startswith('BMAT') or 
        'CALCULUS' in course_name_upper or
        'MATHEMATICS' in course_name_upper or
        'LINEAR ALGEBRA' in course_name_upper or
        'STATISTICS' in course_name_upper or
        'PROBABILITY' in course_name_upper or
        'DIFFERENTIAL EQUATIONS' in course_name_upper or
        'DISCRETE MATH' in course_name_upper):
        return "MATH"
    
    # CORE_CSE - CSE fundamental courses (BCSE 1XX, 2XX, 3XX specific ones)
    core_cse_courses = [
        'DATA STRUCTURES', 'ALGORITHMS', 'OPERATING SYSTEMS', 'COMPUTER NETWORKS',
        'DATABASE', 'COMPILER', 'COMPUTER ARCHITECTURE', 'ARTIFICIAL INTELLIGENCE',
        'CLOUD ARCHITECTURE', 'WEB PROGRAMMING', 'OOP', 'PROGRAMMING'
    ]
    
    if course_code.startswith('BCSE'):
        for core_keyword in core_cse_courses:
            if core_keyword in course_name_upper:
                return "CORE_CSE"
        
        # Electives are typically 4XX or specialized courses
        try:
            course_num = int(course_code.replace('BCSE', '').replace('P', '').replace('E', '').replace('N', '').replace('L', '')[:3])
            if course_num >= 400:
                return "ELECTIVE"
        except:
            pass
    
    # CORE_ENGG - Engineering fundamentals
    core_engg_keywords = [
        'PHYSICS', 'CHEMISTRY', 'ELECTRICAL', 'ELECTRONICS', 'MICROPROCESSOR',
        'DIGITAL SYSTEMS', 'TECHNICAL ENGLISH', 'ENGINEERING'
    ]
    
    if (course_code.startswith(('BPHY', 'BCHY', 'BEEE', 'BECE', 'BENG')) or
        any(keyword in course_name_upper for keyword in core_engg_keywords)):
        return "CORE_ENGG"
    
    return "ELECTIVE"


def predict_missing_components(course: dict) -> dict:
    """Predict missing internal components based on available data."""
    
    components = course.get('components', [])
    
    # Extract current marks
    cat1 = 0
    cat2 = 0
    da = 0
    quiz1 = 0
    quiz2 = 0
    
    for comp in components:
        title = comp['title'].upper()
        if 'CAT' in title or 'CONTINUOUS ASSESSMENT TEST' in title:
            if 'I' in title or '1' in title:
                cat1 = comp.get('weightage_mark', 0)
            elif 'II' in title or '2' in title:
                cat2 = comp.get('weightage_mark', 0)
        elif 'DIGITAL ASSIGNMENT' in title or 'DA' in title:
            da = comp.get('weightage_mark', 0)
        elif 'QUIZ' in title:
            if 'I' in title or '1' in title:
                quiz1 = comp.get('weightage_mark', 0)
            elif 'II' in title or '2' in title:
                quiz2 = comp.get('weightage_mark', 0)
    
    predictions = {}
    
    # Predict CAT2 if missing (based on CAT1)
    if cat1 > 0 and cat2 == 0:
        if cat1 < 10.5:  # CAT1 < 70%
            predicted_cat2 = max(cat1 - 0.5, cat1 * 0.95)
        else:
            predicted_cat2 = cat1 + 0.3
        predictions['CAT2'] = round(min(predicted_cat2, 15), 1)
    else:
        predictions['CAT2'] = cat2
    
    # Predict DA if missing
    if da == 0:
        if cat1 > 0:
            cat_percentage = (cat1 / 15) * 100
            if cat_percentage >= 80:
                predictions['DA'] = 9.0
            elif cat_percentage >= 70:
                predictions['DA'] = 8.5
            elif cat_percentage >= 60:
                predictions['DA'] = 8.0
            else:
                predictions['DA'] = 7.5
        else:
            predictions['DA'] = 8.0
    else:
        predictions['DA'] = da
    
    # Predict Quizzes (typically easier than CATs)
    cat_avg = (cat1 + predictions['CAT2']) / 2 if cat1 > 0 else 7.5
    
    if quiz1 == 0:
        predictions['Quiz1'] = round(min(cat_avg + 0.5, 10), 1)
    else:
        predictions['Quiz1'] = quiz1
    
    if quiz2 == 0:
        predictions['Quiz2'] = round(min(cat_avg + 0.5, 10), 1)
    else:
        predictions['Quiz2'] = quiz2
    
    # Calculate total internal
    total_internal = cat1 + predictions['CAT2'] + predictions['DA'] + predictions['Quiz1'] + predictions['Quiz2']
    
    return {
        'CAT1': cat1,
        'CAT2': predictions['CAT2'],
        'DA': predictions['DA'],
        'Quiz1': predictions['Quiz1'],
        'Quiz2': predictions['Quiz2'],
        'total_internal': round(total_internal, 1),
        'internal_percentage': round((total_internal / 60) * 100, 1)
    }


def load_historical_patterns():
    """Load historical patterns."""
    patterns_file = Path(__file__).parent.parent / "data" / "historical_grade_patterns.json"
    
    if not patterns_file.exists():
        return {}
    
    with open(patterns_file, 'r') as f:
        return json.load(f)


def predict_grade_from_historical(internal_marks: float, subject_type: str, 
                                  patterns: dict, is_absolute_grading: bool = False) -> dict:
    """Predict grade based on historical patterns."""
    
    internal_percentage = (internal_marks / 60) * 100
    
    # For LAB and SOFT_SKILL subjects, use absolute grading
    if is_absolute_grading:
        if internal_percentage >= 90:
            predicted = "S"
        elif internal_percentage >= 80:
            predicted = "A"
        elif internal_percentage >= 70:
            predicted = "B"
        elif internal_percentage >= 60:
            predicted = "C"
        elif internal_percentage >= 50:
            predicted = "D"
        else:
            predicted = "F"
        
        return {
            "predicted_grade": predicted,
            "confidence": 95,
            "reason": f"{subject_type} - Absolute grading based on {internal_percentage:.1f}% internal",
            "is_absolute": True
        }
    
    # For other subjects, use historical patterns
    if subject_type not in patterns.get("pattern_summary", {}):
        return {
            "predicted_grade": "Unknown",
            "confidence": 0,
            "reason": f"No historical data for {subject_type}",
            "is_absolute": False
        }
    
    type_patterns = patterns["pattern_summary"][subject_type]["grade_patterns"]
    
    # Find closest match
    closest_grades = []
    for grade, pattern in type_patterns.items():
        avg_internal = pattern["avg_internal_percentage"]
        diff = abs(internal_percentage - avg_internal)
        closest_grades.append({
            "grade": grade,
            "diff": diff,
            "avg_internal": avg_internal,
            "count": pattern["count"]
        })
    
    closest_grades.sort(key=lambda x: x["diff"])
    best_match = closest_grades[0]
    
    # Calculate confidence
    if best_match["diff"] <= 5:
        confidence = 90
    elif best_match["diff"] <= 10:
        confidence = 75
    elif best_match["diff"] <= 15:
        confidence = 60
    else:
        confidence = 40
    
    reason = (f"Based on {best_match['count']} historical {subject_type} courses with "
              f"{best_match['avg_internal']:.1f}% internal → Grade {best_match['grade']}. "
              f"Your {internal_percentage:.1f}% is {best_match['diff']:.1f}% away.")
    
    return {
        "predicted_grade": best_match["grade"],
        "confidence": confidence,
        "reason": reason,
        "is_absolute": False,
        "historical_avg": best_match["avg_internal"]
    }


def calculate_fat_requirements(internal_marks: float) -> dict:
    """Calculate FAT required for each grade."""
    fat_reqs = {}
    grade_thresholds = {"S": 90, "A": 80, "B": 70, "C": 60, "D": 50}
    
    for grade, threshold in grade_thresholds.items():
        fat_needed = threshold - internal_marks
        
        if fat_needed <= 0:
            fat_reqs[grade] = {
                "fat_needed": 0,
                "feasibility": "✓ Already achieved",
                "percentage": 0
            }
        elif fat_needed > 40:
            fat_reqs[grade] = {
                "fat_needed": fat_needed,
                "feasibility": "✗ Not achievable",
                "percentage": 100
            }
        else:
            fat_percentage = (fat_needed / 40) * 100
            if fat_percentage >= 90:
                feasibility = "Very difficult (>90%)"
            elif fat_percentage >= 80:
                feasibility = "Challenging (>80%)"
            elif fat_percentage >= 70:
                feasibility = "Moderate"
            else:
                feasibility = "Achievable"
            
            fat_reqs[grade] = {
                "fat_needed": round(fat_needed, 1),
                "feasibility": feasibility,
                "percentage": round(fat_percentage, 1)
            }
    
    return fat_reqs


def main():
    """Main pipeline."""
    
    if len(sys.argv) < 2:
        print("Usage: python complete_prediction.py <vtop_data.json>")
        sys.exit(1)
    
    # Load data
    vtop_file = Path(sys.argv[1])
    with open(vtop_file, 'r') as f:
        vtop_data = json.load(f)
    
    patterns = load_historical_patterns()
    
    print("\n" + "="*90)
    print("COMPLETE GRADE PREDICTION PIPELINE")
    print("="*90)
    print(f"\nStudent: {vtop_data['reg_no']}")
    print(f"Semester: {vtop_data['semester']}")
    print(f"Current CGPA: {vtop_data['cgpa']}")
    print(f"\nAnalyzing {len(vtop_data['marks'])} courses...")
    
    results = []
    
    for course in vtop_data['marks']:
        course_code = course['course_code']
        course_title = course['course_title']
        
        # Step 1: Predict missing marks
        predicted_marks = predict_missing_components(course)
        
        # Step 2: Categorize
        subject_type = categorize_subject_type(course_code, course_title)
        is_absolute = subject_type in ["LAB", "SOFT_SKILL"]
        
        # Step 3: Predict grade
        grade_pred = predict_grade_from_historical(
            predicted_marks['total_internal'],
            subject_type,
            patterns,
            is_absolute
        )
        
        # Step 4: Calculate FAT requirements
        fat_reqs = calculate_fat_requirements(predicted_marks['total_internal'])
        
        results.append({
            'course_code': course_code,
            'course_title': course_title,
            'subject_type': subject_type,
            'marks': predicted_marks,
            'grade': grade_pred,
            'fat_requirements': fat_reqs
        })
    
    # Display results
    print("\n" + "="*90)
    print("DETAILED PREDICTIONS")
    print("="*90)
    
    for i, result in enumerate(results, 1):
        marks = result['marks']
        grade = result['grade']
        
        print(f"\n{i}. {result['course_code']}: {result['course_title']}")
        print(f"   Type: {result['subject_type']} {'[ABSOLUTE GRADING]' if grade['is_absolute'] else ''}")
        
        print(f"\n   Internal Marks Breakdown:")
        print(f"      CAT1:  {marks['CAT1']:.1f}/15")
        print(f"      CAT2:  {marks['CAT2']:.1f}/15 {'(predicted)' if marks['CAT2'] != marks['CAT1'] else ''}")
        print(f"      DA:    {marks['DA']:.1f}/10")
        print(f"      Quiz1: {marks['Quiz1']:.1f}/10")
        print(f"      Quiz2: {marks['Quiz2']:.1f}/10")
        print(f"      ────────────────────")
        print(f"      Total: {marks['total_internal']:.1f}/60 ({marks['internal_percentage']:.1f}%)")
        
        print(f"\n   Predicted Grade: {grade['predicted_grade']} (Confidence: {grade['confidence']}%)")
        print(f"   {grade['reason']}")
        
        if not grade['is_absolute']:
            print(f"\n   FAT Requirements:")
            for g in ['S', 'A', 'B', 'C']:
                req = result['fat_requirements'][g]
                if req['fat_needed'] > 0 and req['fat_needed'] <= 40:
                    print(f"      Grade {g}: {req['fat_needed']:.1f}/40 ({req['percentage']:.1f}%) - {req['feasibility']}")
                elif req['feasibility'] == "✓ Already achieved":
                    print(f"      Grade {g}: {req['feasibility']}")
        
        print(f"   {'-'*86}")
    
    # Summary
    print("\n" + "="*90)
    print("PREDICTION SUMMARY")
    print("="*90)
    
    grade_counts = {}
    for result in results:
        grade = result['grade']['predicted_grade']
        grade_counts[grade] = grade_counts.get(grade, 0) + 1
    
    print("\nPredicted Grade Distribution:")
    for grade in ['S', 'A', 'B', 'C', 'D', 'F']:
        if grade in grade_counts:
            print(f"   {grade}: {grade_counts[grade]} courses")
    
    # Calculate expected GPA
    grade_points = {'S': 10, 'A': 9, 'B': 8, 'C': 7, 'D': 6, 'E': 5, 'F': 0}
    total_credits = sum(course.get('credits', 3) for course in vtop_data['marks'])
    predicted_points = sum(
        grade_points.get(result['grade']['predicted_grade'], 7) * 3
        for result in results
    )
    predicted_gpa = predicted_points / len(results) / 3 * 10 if results else 0
    
    print(f"\nPredicted Semester GPA: {predicted_gpa:.2f}")
    print(f"Current CGPA: {vtop_data['cgpa']}")
    
    print("\n" + "="*90)


def run_grade_predictor(vtop_data):
    """
    Wrapper function for run_all_features.py compatibility.
    Returns list of prediction results.
    """
    results = []
    
    # Load historical patterns
    historical_db_path = Path(__file__).parent.parent / "data" / "historical_grade_patterns.json"
    
    if not historical_db_path.exists():
        log_warning(f"Historical database not found at {historical_db_path}")
        return results
    
    with open(historical_db_path, 'r') as f:
        historical_data = json.load(f)
    
    for course in vtop_data.get('marks', []):
        course_code = course.get('course_code', '')
        course_name = course.get('course_name', '')
        
        # Predict missing marks
        marks = predict_missing_components(course)
        
        # Categorize subject
        subject_type = categorize_subject_type(course_code, course_name)
        
        # Predict grade
        grade = predict_grade_from_historical(
            marks['internal_percentage'],
            subject_type,
            historical_data
        )
        
        # Calculate FAT requirements
        fat_reqs = calculate_fat_requirements(marks['total_internal'])
        
        results.append({
            'course_code': course_code,
            'course_name': course_name,
            'subject_type': subject_type,
            'marks': marks,
            'grade': grade,
            'fat_requirements': fat_reqs
        })
    
    return results


def predict_grade_comprehensive(vtop_data):
    """
    Alias for run_grade_predictor for backward compatibility.
    """
    return run_grade_predictor(vtop_data)


if __name__ == "__main__":
    main()
