"""
Study Time Allocator - Non-API AI Feature
Allocates study time based on course difficulty and current performance.
"""

from typing import Dict, List
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.constants import VIT_GRADE_THRESHOLDS
from utils.formatters import print_section, print_box


def calculate_course_priority(
    current_score: float,
    attendance_percent: float,
    credits: int = 3
) -> Dict:
    """
    Calculate priority score for a course.
    
    Priority factors:
    - Low current score = Higher priority
    - Low attendance = Higher priority
    - More credits = Higher priority
    
    Args:
        current_score: Current total score (0-100)
        attendance_percent: Attendance percentage
        credits: Course credits
        
    Returns:
        Dictionary with priority metrics
    """
    # Score factor: Lower score = higher priority
    # Scale: 100 (lowest) to 0 (highest)
    score_factor = max(0, 100 - current_score)
    
    # Attendance factor: Lower attendance = higher priority
    # Scale: 0 (perfect) to 100 (critical)
    if attendance_percent >= 90:
        attendance_factor = 0
    elif attendance_percent >= 80:
        attendance_factor = 20
    elif attendance_percent >= 75:
        attendance_factor = 50
    else:
        attendance_factor = 100
    
    # Credit factor: More credits = slightly higher priority
    credit_factor = credits * 5
    
    # Calculate composite priority (0-300 scale)
    priority = (score_factor * 0.6) + (attendance_factor * 0.3) + (credit_factor * 0.1)
    
    # Determine urgency level
    if priority >= 70:
        urgency = "CRITICAL"
    elif priority >= 50:
        urgency = "HIGH"
    elif priority >= 30:
        urgency = "MEDIUM"
    else:
        urgency = "LOW"
    
    return {
        "priority_score": round(priority, 2),
        "urgency": urgency,
        "factors": {
            "score_component": round(score_factor * 0.6, 2),
            "attendance_component": round(attendance_factor * 0.3, 2),
            "credit_component": round(credit_factor * 0.1, 2)
        }
    }


def allocate_study_time(
    courses: List[Dict],
    total_hours: int = 40
) -> List[Dict]:
    """
    Allocate weekly study time across courses based on priority.
    
    Args:
        courses: List of course dictionaries with scores and attendance
        total_hours: Total study hours per week (default: 40)
        
    Returns:
        List of courses with allocated study time
    """
    if not courses:
        return []
    
    # Calculate priority for each course
    course_priorities = []
    total_priority = 0
    
    for course in courses:
        priority_info = calculate_course_priority(
            course.get("current_score", 0),
            course.get("attendance_percent", 100),
            course.get("credits", 3)
        )
        
        course_priorities.append({
            "course": course,
            "priority": priority_info["priority_score"],
            "urgency": priority_info["urgency"],
            "factors": priority_info["factors"]
        })
        total_priority += priority_info["priority_score"]
    
    # Sort by priority (highest first)
    course_priorities.sort(key=lambda x: x["priority"], reverse=True)
    
    # Allocate time proportionally
    allocations = []
    remaining_hours = total_hours
    
    for i, item in enumerate(course_priorities):
        if total_priority > 0:
            # Proportional allocation
            allocated = (item["priority"] / total_priority) * total_hours
            
            # Ensure minimum 2 hours per course
            allocated = max(2, allocated)
            
            # For last course, use remaining hours
            if i == len(course_priorities) - 1:
                allocated = max(2, remaining_hours)
            
            remaining_hours -= allocated
        else:
            # Equal allocation if all priorities are 0
            allocated = total_hours / len(course_priorities)
        
        allocations.append({
            "course_code": item["course"].get("course_code", ""),
            "course_name": item["course"].get("course_name", ""),
            "priority": item["priority"],
            "urgency": item["urgency"],
            "allocated_hours": round(allocated, 1),
            "daily_hours": round(allocated / 7, 1),
            "factors": item["factors"]
        })
    
    return allocations


def generate_study_plan(allocations: List[Dict]) -> List[str]:
    """
    Generate actionable study plan recommendations.
    
    Args:
        allocations: List of time allocations
        
    Returns:
        List of recommendation strings
    """
    recommendations = []
    
    for alloc in allocations:
        course = alloc["course_code"]
        urgency = alloc["urgency"]
        weekly = alloc["allocated_hours"]
        daily = alloc["daily_hours"]
        
        if urgency == "CRITICAL":
            recommendations.append(
                f"🚨 {course}: URGENT - {weekly}h/week ({daily}h/day). Focus on basics, practice problems, seek help."
            )
        elif urgency == "HIGH":
            recommendations.append(
                f"⚠️  {course}: HIGH - {weekly}h/week ({daily}h/day). Review lecture notes, solve assignments, attend doubt sessions."
            )
        elif urgency == "MEDIUM":
            recommendations.append(
                f"📚 {course}: MEDIUM - {weekly}h/week ({daily}h/day). Stay current with lectures, complete assignments on time."
            )
        else:
            recommendations.append(
                f"✅ {course}: LOW - {weekly}h/week ({daily}h/day). Maintain pace, explore advanced topics."
            )
    
    return recommendations


def run_study_allocator(vtop_data: Dict, total_hours: int = 40) -> List[Dict]:
    """
    Run study time allocator for all courses.
    
    Args:
        vtop_data: Dictionary containing VTOP data
        total_hours: Total study hours per week
        
    Returns:
        List of time allocation results
    """
    print_section(f"STUDY TIME ALLOCATOR ({total_hours} hours/week)")
    
    marks = vtop_data.get("marks", [])
    attendance = vtop_data.get("attendance", [])
    
    if not marks:
        print("  ℹ️  No course data found")
        return []
    
    # Build course data
    courses = []
    for mark in marks:
        course_code = mark.get("course_code", "")
        course_name = mark.get("course_title", "")
        current_score = mark.get("total_scored", 0.0)
        
        # Find attendance for this course
        att_percent = 100
        for att in attendance:
            if att.get("course_code") == course_code:
                att_percent = att.get("attendance_percentage", 100)
                break
        
        courses.append({
            "course_code": course_code,
            "course_name": course_name,
            "current_score": current_score,
            "attendance_percent": att_percent,
            "credits": 3  # Default to 3 credits
        })
    
    # Allocate study time
    allocations = allocate_study_time(courses, total_hours)
    
    if not allocations:
        print("  ℹ️  No allocations generated")
        return []
    
    print(f"  📊 Study time allocated across {len(allocations)} courses\n")
    
    # Display allocations
    for alloc in allocations:
        icon = {
            "CRITICAL": "🚨",
            "HIGH": "⚠️",
            "MEDIUM": "📚",
            "LOW": "✅"
        }.get(alloc["urgency"], "📖")
        
        lines = [
            f"Priority Score: {alloc['priority']}/100",
            f"Urgency Level: {alloc['urgency']}",
            "",
            f"Allocated Time:",
            f"  • Weekly: {alloc['allocated_hours']} hours",
            f"  • Daily: {alloc['daily_hours']} hours",
            "",
            f"Priority Breakdown:",
            f"  • Performance: {alloc['factors']['score_component']}",
            f"  • Attendance: {alloc['factors']['attendance_component']}",
            f"  • Credits: {alloc['factors']['credit_component']}"
        ]
        
        print_box(f"{icon} {alloc['course_code']}", lines)
        print()
    
    # Generate and display recommendations
    recommendations = generate_study_plan(allocations)
    print_section("STUDY RECOMMENDATIONS")
    for rec in recommendations:
        print(f"  {rec}")
    print()
    
    return allocations


if __name__ == "__main__":
    import json
    
    if len(sys.argv) < 2:
        print("Usage: python study_allocator.py <data_file.json>")
        sys.exit(1)
    
    # Load data
    with open(sys.argv[1], 'r') as f:
        vtop_data = json.load(f)
    
    # Run analysis
    print_section("STUDY TIME ALLOCATOR")
    allocations = run_study_allocator(vtop_data)
    
    if not allocations:
        print("❌ No courses available for study allocation")
