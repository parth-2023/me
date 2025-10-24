"""
Grade Target Planner - Non-API AI Feature
Creates actionable plans to achieve target CGPA goals.
"""

from typing import Dict, List, Optional
import sys
import os
import math

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.constants import VIT_GRADE_THRESHOLDS
from utils.formatters import print_section, print_box


GRADE_POINTS = {
    "S": 10,
    "A": 9,
    "B": 8,
    "C": 7,
    "D": 6,
    "F": 0
}


def calculate_required_sgpa(
    current_cgpa: float,
    target_cgpa: float,
    completed_semesters: int,
    remaining_semesters: int = 1
) -> float:
    """
    Calculate required SGPA to reach target CGPA.
    
    Formula: target_cgpa = (current_cgpa * completed + required_sgpa * remaining) / total
    
    Args:
        current_cgpa: Current CGPA
        target_cgpa: Target CGPA to achieve
        completed_semesters: Number of completed semesters
        remaining_semesters: Number of remaining semesters
        
    Returns:
        Required SGPA for remaining semesters
    """
    total_semesters = completed_semesters + remaining_semesters
    
    # Rearrange formula: required_sgpa = (target * total - current * completed) / remaining
    required_sgpa = (
        (target_cgpa * total_semesters) - (current_cgpa * completed_semesters)
    ) / remaining_semesters
    
    return required_sgpa


def plan_course_grades(
    required_sgpa: float,
    num_courses: int,
    course_credits: Optional[List[int]] = None
) -> List[Dict]:
    """
    Plan individual course grades to achieve required SGPA.
    
    Args:
        required_sgpa: Required semester GPA
        num_courses: Number of courses
        course_credits: List of credits per course (default: all 3 credits)
        
    Returns:
        List of course grade plans
    """
    if course_credits is None:
        course_credits = [3] * num_courses
    
    total_credits = sum(course_credits)
    required_grade_points = required_sgpa * total_credits
    
    # Strategy: Start with average grade, then adjust
    plans = []
    
    # Try to distribute grades reasonably
    for i in range(num_courses):
        credits = course_credits[i]
        # Target grade point per course
        target_gp = required_sgpa
        
        # Find closest grade
        best_grade = None
        min_diff = float('inf')
        
        for grade, gp in sorted(GRADE_POINTS.items(), key=lambda x: x[1], reverse=True):
            diff = abs(gp - target_gp)
            if diff < min_diff:
                min_diff = diff
                best_grade = grade
        
        plans.append({
            "course_num": i + 1,
            "credits": credits,
            "target_grade": best_grade,
            "grade_point": GRADE_POINTS[best_grade]
        })
    
    # Adjust to meet exact requirement
    current_total_gp = sum(p["grade_point"] * p["credits"] for p in plans)
    deficit = required_grade_points - current_total_gp
    
    # If deficit, upgrade some courses
    if deficit > 0:
        for plan in sorted(plans, key=lambda x: x["grade_point"]):
            if deficit <= 0:
                break
            
            current_gp = plan["grade_point"]
            # Try to upgrade
            next_grade = None
            for grade, gp in sorted(GRADE_POINTS.items(), key=lambda x: x[1], reverse=True):
                if gp > current_gp:
                    next_grade = grade
                    next_gp = gp
                    break
            
            if next_grade:
                improvement = (next_gp - current_gp) * plan["credits"]
                if improvement <= deficit:
                    plan["target_grade"] = next_grade
                    plan["grade_point"] = next_gp
                    deficit -= improvement
    
    # Calculate achieved SGPA
    achieved_gp = sum(p["grade_point"] * p["credits"] for p in plans)
    achieved_sgpa = achieved_gp / total_credits
    
    return plans, achieved_sgpa


def generate_action_items(
    required_sgpa: float,
    current_courses: List[Dict],
    grade_plans: List[Dict]
) -> List[str]:
    """
    Generate actionable items to achieve target grades.
    
    Args:
        required_sgpa: Required SGPA
        current_courses: Current course information
        grade_plans: Planned grades for courses
        
    Returns:
        List of action items
    """
    actions = []
    
    # General actions based on required SGPA
    if required_sgpa >= 9.5:
        actions.append("TARGET: Target: EXCELLENCE - Aim for S grades in all courses")
        actions.append("   • Attend all classes (100% attendance)")
        actions.append("   • Complete assignments 2-3 days before deadline")
        actions.append("   • Solve additional practice problems beyond coursework")
        actions.append("   • Form study groups for peer learning")
    elif required_sgpa >= 9.0:
        actions.append("TARGET: Target: HIGH PERFORMANCE - Mix of S and A grades needed")
        actions.append("   • Maintain 95%+ attendance")
        actions.append("   • Focus on understanding concepts, not just memorization")
        actions.append("   • Complete all assignments on time")
        actions.append("   • Allocate 30-35 hours/week for studies")
    elif required_sgpa >= 8.0:
        actions.append("TARGET: Target: GOOD PERFORMANCE - Consistent A grades")
        actions.append("   • Maintain 90%+ attendance")
        actions.append("   • Stay current with lecture material")
        actions.append("   • Review notes weekly")
        actions.append("   • Allocate 25-30 hours/week for studies")
    elif required_sgpa >= 7.0:
        actions.append("TARGET: Target: SATISFACTORY - Mix of A and B grades")
        actions.append("   • Maintain 85%+ attendance")
        actions.append("   • Complete all CATs and assignments")
        actions.append("   • Focus on core concepts")
        actions.append("   • Allocate 20-25 hours/week for studies")
    else:
        actions.append("TARGET: Target: IMPROVEMENT NEEDED - Focus on passing")
        actions.append("   • Maintain minimum 75% attendance")
        actions.append("   • Seek help from professors/TAs")
        actions.append("   • Join study groups")
        actions.append("   • Identify weak areas and work on them")
    
    # Course-specific actions
    if grade_plans:
        s_count = sum(1 for p in grade_plans if p["target_grade"] == "S")
        a_count = sum(1 for p in grade_plans if p["target_grade"] == "A")
        
        if s_count > 0:
            actions.append(f"\nINFO: {s_count} course(s) need S grade:")
            actions.append("   • Score 90%+ in all assessments")
            actions.append("   • Target 45%+ out of 60% in FAT")
        
        if a_count > 0:
            actions.append(f"\nCOURSE {a_count} course(s) need A grade:")
            actions.append("   • Score 80%+ overall")
            actions.append("   • Target 42%+ out of 60% in FAT")
    
    return actions


def run_target_planner(
    vtop_data: Dict,
    target_cgpa: float,
    remaining_semesters: int = 1
) -> Dict:
    """
    Run grade target planner.
    
    Args:
        vtop_data: Dictionary containing VTOP data
        target_cgpa: Target CGPA to achieve
        remaining_semesters: Number of remaining semesters
        
    Returns:
        Planning results with action items
    """
    print_section(f"GRADE TARGET PLANNER (Target: {target_cgpa} CGPA)")
    
    current_cgpa = vtop_data.get("cgpa", 0.0)
    cgpa_history = vtop_data.get("cgpa_trend", [])
    marks = vtop_data.get("marks", [])
    
    completed_semesters = len(cgpa_history)
    num_courses = len(marks)
    
    # Calculate required SGPA
    required_sgpa = calculate_required_sgpa(
        current_cgpa,
        target_cgpa,
        completed_semesters,
        remaining_semesters
    )
    
    # Check feasibility
    if required_sgpa > 10.0:
        lines = [
            f"Current CGPA: {current_cgpa}",
            f"Target CGPA: {target_cgpa}",
            f"Required SGPA: {required_sgpa:.2f}",
            "",
            "FAIL TARGET NOT ACHIEVABLE",
            "Required SGPA exceeds maximum (10.0)",
            "",
            "Suggestions:",
            f"  • Maximum achievable: {calculate_required_sgpa(current_cgpa, 10.0, completed_semesters, 0) * 0.9:.2f}",
            "  • Consider longer timeline",
            "  • Focus on consistent improvement"
        ]
        print_box("WARNING:  Feasibility Check", lines)
        print()
        
        return {
            "feasible": False,
            "required_sgpa": required_sgpa,
            "reason": "Required SGPA exceeds maximum"
        }
    
    if required_sgpa < 0:
        lines = [
            f"Current CGPA: {current_cgpa}",
            f"Target CGPA: {target_cgpa}",
            "",
            "OK TARGET ALREADY ACHIEVED",
            "Your current CGPA exceeds the target!",
            "",
            f"TIP Maintain current performance or aim higher"
        ]
        print_box("SUCCESS Status", lines)
        print()
        
        return {
            "feasible": True,
            "already_achieved": True,
            "current_cgpa": current_cgpa
        }
    
    # Plan course grades
    grade_plans, achieved_sgpa = plan_course_grades(required_sgpa, num_courses)
    
    # Display plan
    lines = [
        f"Current CGPA: {current_cgpa}",
        f"Target CGPA: {target_cgpa}",
        f"Completed Semesters: {completed_semesters}",
        f"Remaining Semesters: {remaining_semesters}",
        "",
        f"Required SGPA: {required_sgpa:.2f}",
        f"Planned SGPA: {achieved_sgpa:.2f}",
        "",
        "Course Grade Plan:"
    ]
    
    for plan in grade_plans:
        lines.append(
            f"  Course {plan['course_num']}: "
            f"Grade {plan['target_grade']} ({plan['grade_point']} points)"
        )
    
    feasible_icon = "OK" if required_sgpa <= 10.0 else "FAIL"
    print_box(f"{feasible_icon} Target Plan", lines)
    print()
    
    # Generate action items
    actions = generate_action_items(required_sgpa, marks, grade_plans)
    
    print_section("ACTION ITEMS")
    for action in actions:
        print(f"  {action}")
    print()
    
    return {
        "feasible": True,
        "required_sgpa": required_sgpa,
        "planned_sgpa": achieved_sgpa,
        "grade_plans": grade_plans,
        "actions": actions
    }


if __name__ == "__main__":
    import json
    
    if len(sys.argv) < 2:
        print("Usage: python target_planner.py <data_file.json> [target_cgpa]")
        print("Example: python target_planner.py data.json 8.5")
        sys.exit(1)
    
    # Load data
    with open(sys.argv[1], 'r') as f:
        vtop_data = json.load(f)
    
    # Get target CGPA (default to current + 0.5)
    current_cgpa = vtop_data.get('cgpa', 8.0)
    target_cgpa = float(sys.argv[2]) if len(sys.argv) > 2 else min(current_cgpa + 0.5, 10.0)
    
    # Run analysis
    print_section(f"GRADE TARGET PLANNER (Target CGPA: {target_cgpa})")
    result = run_target_planner(vtop_data, target_cgpa)
    
    if not result:
        print("FAIL Unable to create target plan")
