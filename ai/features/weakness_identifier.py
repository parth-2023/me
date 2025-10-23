"""
Weakness Identifier - Non-API AI Feature
Identifies weak areas and categorizes subjects by performance.
"""

from typing import Dict, List, Tuple
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.constants import VIT_GRADE_THRESHOLDS
from utils.formatters import print_section, print_box


def categorize_subject_type(course_code: str, course_name: str) -> str:
    """
    Categorize subject type based on course code and name.
    
    Categories:
    - CORE: Core CS subjects (BCSE)
    - THEORY: Pure theory subjects
    - LAB: Lab/Practical subjects
    - MATH: Mathematics subjects (BMAT)
    - SOFT_SKILL: Soft skills (BSTS)
    - ELECTIVE: Elective subjects
    - PROJECT: Projects
    - OTHER: Others
    
    Args:
        course_code: Course code (e.g., BCSE302L)
        course_name: Course name
        
    Returns:
        Category string
    """
    code_upper = course_code.upper()
    name_lower = course_name.lower()
    
    # Lab subjects
    if code_upper.endswith('P') or 'lab' in name_lower or 'practical' in name_lower:
        return "LAB"
    
    # Math subjects
    if code_upper.startswith('BMAT') or 'mathematics' in name_lower or 'calculus' in name_lower:
        return "MATH"
    
    # Soft skills
    if code_upper.startswith('BSTS') or 'soft skill' in name_lower or 'communication' in name_lower:
        return "SOFT_SKILL"
    
    # Core CS subjects
    if code_upper.startswith('BCSE'):
        # Check if it's elective (typically 3XX range for electives)
        course_num = int(''.join(filter(str.isdigit, code_upper[4:7]))) if len(code_upper) >= 7 else 0
        if course_num >= 350:
            return "ELECTIVE"
        return "CORE"
    
    # Projects
    if 'project' in name_lower or 'capstone' in name_lower:
        return "PROJECT"
    
    return "OTHER"


def calculate_performance_score(
    cat1: float,
    cat2: float,
    quiz: float,
    da: float,
    attendance_percent: float
) -> Tuple[float, str]:
    """
    Calculate overall performance score for a subject.
    
    Score factors:
    - Internal marks: 60%
    - Attendance: 40%
    
    Args:
        cat1: CAT1 weightage marks
        cat2: CAT2 weightage marks
        quiz: Quiz weightage marks
        da: DA weightage marks
        attendance_percent: Attendance percentage
        
    Returns:
        Tuple of (score, performance_level)
    """
    # Calculate internal marks percentage
    # Total internal: CAT1(15) + CAT2(15) + Quiz/DA(10) = 40 marks
    total_internal = cat1 + cat2 + max(quiz, da)
    internal_percent = (total_internal / 40) * 100
    
    # Composite score
    score = (internal_percent * 0.6) + (attendance_percent * 0.4)
    
    # Determine performance level
    if score >= 85:
        level = "EXCELLENT"
    elif score >= 70:
        level = "GOOD"
    elif score >= 55:
        level = "AVERAGE"
    elif score >= 40:
        level = "WEAK"
    else:
        level = "CRITICAL"
    
    return round(score, 2), level


def identify_weak_components(
    cat1_percent: float,
    cat2_percent: float,
    quiz_percent: float,
    da_percent: float
) -> List[str]:
    """
    Identify which components are weak.
    
    Args:
        cat1_percent: CAT1 percentage (out of 100)
        cat2_percent: CAT2 percentage (out of 100)
        quiz_percent: Quiz percentage (out of 100)
        da_percent: DA percentage (out of 100)
        
    Returns:
        List of weak component names
    """
    weak_components = []
    threshold = 60  # Below 60% is considered weak
    
    if cat1_percent > 0 and cat1_percent < threshold:
        weak_components.append(f"CAT1 ({cat1_percent:.1f}%)")
    if cat2_percent > 0 and cat2_percent < threshold:
        weak_components.append(f"CAT2 ({cat2_percent:.1f}%)")
    if quiz_percent > 0 and quiz_percent < threshold:
        weak_components.append(f"Quiz ({quiz_percent:.1f}%)")
    if da_percent > 0 and da_percent < threshold:
        weak_components.append(f"DA ({da_percent:.1f}%)")
    
    return weak_components


def generate_improvement_plan(
    performance_level: str,
    weak_components: List[str],
    attendance_percent: float,
    subject_type: str
) -> List[str]:
    """
    Generate actionable improvement plan.
    
    Args:
        performance_level: EXCELLENT/GOOD/AVERAGE/WEAK/CRITICAL
        weak_components: List of weak component names
        attendance_percent: Attendance percentage
        subject_type: Subject category
        
    Returns:
        List of action items
    """
    actions = []
    
    # Performance-based actions
    if performance_level == "CRITICAL":
        actions.append("🚨 URGENT: Immediate intervention required")
        actions.append("   • Schedule meeting with professor")
        actions.append("   • Join peer tutoring sessions")
        actions.append("   • Allocate 2-3 hours daily for this subject")
    elif performance_level == "WEAK":
        actions.append("⚠️  Focus on fundamentals")
        actions.append("   • Review class notes thoroughly")
        actions.append("   • Solve previous year questions")
        actions.append("   • Attend office hours for doubts")
    elif performance_level == "AVERAGE":
        actions.append("📚 Room for improvement")
        actions.append("   • Practice more problems")
        actions.append("   • Focus on weak topics")
    
    # Component-specific actions
    if weak_components:
        actions.append(f"   • Weak areas: {', '.join(weak_components)}")
    
    # Attendance-based actions
    if attendance_percent < 75:
        actions.append("🚨 Attendance below requirement (75%)")
        actions.append("   • Must attend all remaining classes")
    elif attendance_percent < 85:
        actions.append("⚠️  Attendance needs improvement")
        actions.append("   • Aim for 90%+ attendance")
    
    # Subject-type specific actions
    if subject_type == "LAB":
        actions.append("💻 Lab subject tips:")
        actions.append("   • Complete all experiments on time")
        actions.append("   • Understand code, don't just copy")
    elif subject_type == "MATH":
        actions.append("📐 Math subject tips:")
        actions.append("   • Practice derivations daily")
        actions.append("   • Solve theorem proofs multiple times")
    elif subject_type == "CORE":
        actions.append("🎯 Core subject tips:")
        actions.append("   • Focus on conceptual understanding")
        actions.append("   • Relate concepts to real applications")
    
    return actions


def run_weakness_identifier(vtop_data: Dict) -> Dict:
    """
    Run comprehensive weakness identification analysis.
    
    Args:
        vtop_data: Dictionary containing VTOP data
        
    Returns:
        Analysis results with categorized weaknesses
    """
    print_section("WEAKNESS IDENTIFIER")
    
    marks = vtop_data.get("marks", [])
    attendance = vtop_data.get("attendance", [])
    
    if not marks:
        print("  ℹ️  No course data found")
        return {}
    
    # Build course analysis
    course_analysis = []
    
    for mark in marks:
        course_code = mark.get("course_code", "")
        course_name = mark.get("course_title", "")
        components = mark.get("components", [])
        
        # Find attendance
        att_percent = 100
        for att in attendance:
            if att.get("course_code") == course_code:
                att_percent = att.get("percentage", att.get("attendance_percentage", 100))
                break
        
        # Extract component marks
        cat1_marks = 0
        cat2_marks = 0
        quiz_marks = 0
        da_marks = 0
        
        cat1_weightage = 0
        cat2_weightage = 0
        quiz_weightage = 0
        da_weightage = 0
        
        for comp in components:
            title = comp.get("title", "").lower()
            scored = comp.get("scored_marks", 0)
            weightage = comp.get("weightage_mark", 0)
            max_marks = comp.get("max_marks", 15)
            
            if "continuous assessment test" in title or "cat" in title:
                if "i" in title or "1" in title:
                    cat1_marks = scored
                    cat1_weightage = weightage
                elif "ii" in title or "2" in title:
                    cat2_marks = scored
                    cat2_weightage = weightage
            elif "quiz" in title:
                quiz_marks = scored
                quiz_weightage = weightage
            elif "assignment" in title or "da" in title or "digital" in title:
                da_marks = scored
                da_weightage = weightage
        
        # Calculate percentages (weightage is already scaled, scored is raw marks)
        # weightage_mark is the final score after scaling (e.g., 9.6 out of 15 for CAT1)
        # We need to convert this to percentage
        cat1_percent = (cat1_weightage / 15) * 100 if cat1_weightage > 0 else 0
        cat2_percent = (cat2_weightage / 15) * 100 if cat2_weightage > 0 else 0
        quiz_percent = (quiz_weightage / 10) * 100 if quiz_weightage > 0 else 0
        da_percent = (da_weightage / 10) * 100 if da_weightage > 0 else 0
        
        # Categorize subject
        subject_type = categorize_subject_type(course_code, course_name)
        
        # Calculate performance score
        score, level = calculate_performance_score(
            cat1_weightage, cat2_weightage, quiz_weightage, da_weightage, att_percent
        )
        
        # Identify weak components
        weak_components = identify_weak_components(
            cat1_percent, cat2_percent, quiz_percent, da_percent
        )
        
        course_analysis.append({
            "course_code": course_code,
            "course_name": course_name,
            "subject_type": subject_type,
            "performance_score": score,
            "performance_level": level,
            "cat1_percent": cat1_percent,
            "cat2_percent": cat2_percent,
            "quiz_percent": quiz_percent,
            "da_percent": da_percent,
            "attendance_percent": att_percent,
            "weak_components": weak_components,
            "cat1_weightage": cat1_weightage,
            "cat2_weightage": cat2_weightage,
            "quiz_weightage": quiz_weightage,
            "da_weightage": da_weightage
        })
    
    # Sort by performance score (lowest first)
    course_analysis.sort(key=lambda x: x["performance_score"])
    
    # Categorize by subject type
    by_type = {}
    for course in course_analysis:
        subject_type = course["subject_type"]
        if subject_type not in by_type:
            by_type[subject_type] = []
        by_type[subject_type].append(course)
    
    # Display analysis
    print(f"  📊 Analyzed {len(course_analysis)} courses\n")
    
    # Show weakest courses first
    print_section("PRIORITY COURSES (Weakest First)")
    
    for i, course in enumerate(course_analysis[:5], 1):  # Top 5 weakest
        icon = {
            "CRITICAL": "🚨",
            "WEAK": "⚠️",
            "AVERAGE": "📚",
            "GOOD": "✅",
            "EXCELLENT": "🌟"
        }.get(course["performance_level"], "📖")
        
        lines = [
            f"Rank: #{i} (Performance Score: {course['performance_score']}/100)",
            f"Level: {course['performance_level']}",
            f"Type: {course['subject_type']}",
            "",
            "Component Performance:",
            f"  • CAT1: {course['cat1_percent']:.1f}% ({course['cat1_weightage']:.1f}/15)",
            f"  • CAT2: {course['cat2_percent']:.1f}% ({course['cat2_weightage']:.1f}/15)",
            f"  • Quiz: {course['quiz_percent']:.1f}% ({course['quiz_weightage']:.1f}/10)",
            f"  • DA: {course['da_percent']:.1f}% ({course['da_weightage']:.1f}/10)",
            f"  • Attendance: {course['attendance_percent']:.1f}%",
        ]
        
        if course["weak_components"]:
            lines.append("")
            lines.append("⚠️  Weak Components:")
            for comp in course["weak_components"]:
                lines.append(f"  • {comp}")
        
        print_box(f"{icon} {course['course_code']}", lines)
        print()
    
    # Show analysis by subject type
    print_section("ANALYSIS BY SUBJECT TYPE")
    
    for subject_type, courses in sorted(by_type.items()):
        avg_score = sum(c["performance_score"] for c in courses) / len(courses)
        weak_count = sum(1 for c in courses if c["performance_level"] in ["WEAK", "CRITICAL"])
        
        print(f"  📂 {subject_type}: {len(courses)} course(s)")
        print(f"     Average Score: {avg_score:.1f}/100")
        if weak_count > 0:
            print(f"     ⚠️  {weak_count} course(s) need attention")
        print()
    
    # Generate improvement plans
    print_section("IMPROVEMENT PLANS")
    
    for course in course_analysis:
        if course["performance_level"] in ["CRITICAL", "WEAK", "AVERAGE"]:
            actions = generate_improvement_plan(
                course["performance_level"],
                course["weak_components"],
                course["attendance_percent"],
                course["subject_type"]
            )
            
            print(f"  📘 {course['course_code']} - {course['course_name']}")
            for action in actions:
                print(f"  {action}")
            print()
    
    return {
        "courses": course_analysis,
        "by_type": by_type,
        "total_courses": len(course_analysis),
        "weak_courses": sum(1 for c in course_analysis if c["performance_level"] in ["WEAK", "CRITICAL"]),
        "critical_courses": sum(1 for c in course_analysis if c["performance_level"] == "CRITICAL")
    }


if __name__ == "__main__":
    import json
    
    if len(sys.argv) < 2:
        print("Usage: python weakness_identifier.py <data_file.json>")
        sys.exit(1)
    
    # Load data
    with open(sys.argv[1], 'r') as f:
        vtop_data = json.load(f)
    
    # Run analysis
    print_section("WEAKNESS IDENTIFIER")
    result = run_weakness_identifier(vtop_data)
    
    if not result or result['total_courses'] == 0:
        print("❌ No courses available for weakness analysis")
