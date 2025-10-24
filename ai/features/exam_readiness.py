"""
Feature 5: Exam Readiness Scorer
Calculate exam readiness based on marks, attendance, and time until exam
"""

import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.formatters import print_box, print_section


def calculate_exam_readiness(
    marks: Dict,
    attendance: Dict,
    exam: Dict
) -> Dict:
    """
    Calculate exam readiness score (0-100).
    
    Score = (marks_strength * 0.4 + attendance_safety * 0.3 + time_factor * 0.3)
    
    Args:
        marks: Course marks data
        attendance: Course attendance data
        exam: Exam information
        
    Returns:
        Dictionary with readiness score and recommendations
    """
    # Extract component scores
    components = marks.get("components", [])
    cat1 = 0
    cat2 = 0
    assignment = 0
    
    for comp in components:
        title = comp.get("title", "").lower()
        scored = comp.get("scored_marks", 0)
        max_marks = comp.get("max_marks", 50)
        
        if "cat-1" in title or "cat1" in title:
            cat1 = (scored / max_marks) * 100 if max_marks > 0 else 0
        elif "cat-2" in title or "cat2" in title:
            cat2 = (scored / max_marks) * 100 if max_marks > 0 else 0
        elif "assignment" in title or "da" in title:
            assignment = scored  # Usually out of 100
    
    # Marks strength (0-100)
    cat_avg = (cat1 + cat2) / 2 if (cat1 or cat2) else 0
    assignment_score = assignment
    marks_strength = (cat_avg + assignment_score) / 2 if assignment_score else cat_avg
    
    # Attendance safety (0-100)
    attendance_percentage = attendance.get("percentage", 0)
    if attendance_percentage >= 85:
        attendance_safety = 100
    elif attendance_percentage >= 75:
        attendance_safety = 80
    else:
        attendance_safety = 50
    
    # Time factor (0-100)
    days_until = exam.get("days_until", 0)
    
    # Try to calculate days_until if not provided
    if days_until == 0 and exam.get("date"):
        try:
            exam_date = datetime.fromisoformat(exam["date"])
            today = datetime.now()
            days_until = (exam_date - today).days
        except:
            days_until = 7  # Default
    
    if days_until >= 14:
        time_factor = 100
    elif days_until >= 7:
        time_factor = 70
    elif days_until >= 3:
        time_factor = 40
    else:
        time_factor = 20
    
    # Overall readiness
    readiness_score = (
        marks_strength * 0.4 +
        attendance_safety * 0.3 +
        time_factor * 0.3
    )
    
    # Status
    if readiness_score >= 80:
        status = "EXCELLENT"
        color = "GREEN"
    elif readiness_score >= 60:
        status = "GOOD"
        color = "YELLOW"
    elif readiness_score >= 40:
        status = "MODERATE"
        color = "🟠"
    else:
        status = "POOR"
        color = "RED"
    
    # Recommendations based on readiness
    recommendations = []
    
    if marks_strength < 60:
        recommendations.append("Focus on weak topics identified in CAT1/CAT2")
    
    if attendance_safety < 80:
        recommendations.append("Improve attendance to avoid complications")
    
    if time_factor < 70:
        recommendations.append(f"Only {days_until} days left - intensify preparation")
    
    if readiness_score >= 80:
        recommendations.append("Excellent preparation - maintain consistency")
    elif readiness_score >= 60:
        recommendations.append("Good progress - focus on advanced topics")
    else:
        recommendations.append("Critical - seek faculty help and study group support")
    
    # Time allocation suggestion
    if days_until <= 3:
        recommendations.append("Allocate 6-8 hours daily for revision")
    elif days_until <= 7:
        recommendations.append("Allocate 4-5 hours daily for preparation")
    else:
        recommendations.append("Allocate 2-3 hours daily for consistent study")
    
    return {
        "course_code": marks.get("course_code", ""),
        "readiness_score": round(readiness_score),
        "status": status,
        "color": color,
        "factors": {
            "marks_strength": round(marks_strength),
            "attendance_safety": attendance_safety,
            "time_available": time_factor
        },
        "days_until_exam": days_until,
        "recommendations": recommendations
    }


def run_exam_readiness(vtop_data: Dict) -> List[Dict]:
    """
    Run exam readiness scorer for all courses with upcoming exams.
    
    Args:
        vtop_data: Dictionary containing VTOP data
        
    Returns:
        List of readiness scores
    """
    print_section("EXAM READINESS ASSESSMENT")
    
    marks = vtop_data.get("marks", [])
    attendance_records = vtop_data.get("attendance", [])
    exams = vtop_data.get("exams", [])
    
    if not exams:
        print("  INFO:  No exam schedule data available")
        return []
    
    # Create lookup dictionaries
    marks_dict = {m.get("course_code"): m for m in marks}
    attendance_dict = {a.get("course_code"): a for a in attendance_records}
    
    results = []
    
    # Filter upcoming exams (next 30 days)
    upcoming_exams = []
    today = datetime.now()
    
    for exam in exams:
        try:
            exam_date = datetime.fromisoformat(exam.get("date", ""))
            days_until = (exam_date - today).days
            if 0 <= days_until <= 30:
                exam["days_until"] = days_until
                upcoming_exams.append(exam)
        except:
            continue
    
    if not upcoming_exams:
        print("  INFO:  No exams in the next 30 days")
        return []
    
    print(f"  📅 Found {len(upcoming_exams)} upcoming exams\n")
    
    for exam in upcoming_exams:
        course_code = exam.get("course_code", "")
        
        # Get marks and attendance
        course_marks = marks_dict.get(course_code, {})
        course_attendance = attendance_dict.get(course_code, {})
        
        if not course_marks:
            continue
        
        result = calculate_exam_readiness(course_marks, course_attendance, exam)
        results.append(result)
        
        # Display result
        lines = [
            f"Course: {result['course_code']} - {exam.get('course_name', '')}",
            f"Exam: {exam.get('exam_type', 'FAT')} on {exam.get('date', '')}",
            f"Days Until: {result['days_until_exam']} days",
            "",
            f"Readiness Score: {result['readiness_score']}/100",
            f"Status: {result['color']} {result['status']}",
            "",
            "Factors:",
            f"  INFO: Marks Strength: {result['factors']['marks_strength']}/100",
            f"  STATS: Attendance Safety: {result['factors']['attendance_safety']}/100",
            f"  ⏰ Time Available: {result['factors']['time_available']}/100",
            "",
            "Recommendations:"
        ]
        
        for rec in result["recommendations"]:
            lines.append(f"  • {rec}")
        
        print_box(f"{result['color']} {course_code}", lines)
        print()
    
    return results


if __name__ == "__main__":
    import json
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python exam_readiness.py <data_file.json>")
        sys.exit(1)
    
    # Load data
    with open(sys.argv[1], 'r') as f:
        vtop_data = json.load(f)
    
    # Run analysis
    results = run_exam_readiness(vtop_data)
    
    if not results:
        print("FAIL No exam readiness data available")


__all__ = ["calculate_exam_readiness", "run_exam_readiness"]
