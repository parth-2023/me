"""
Feature 4: Attendance Recovery Planner
Generate recovery plans for courses below 75% attendance
"""

import sys
from pathlib import Path
from typing import Dict, List

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.constants import VIT_MIN_ATTENDANCE, ESTIMATED_REMAINING_CLASSES
from utils.formatters import print_box, print_section


def generate_recovery_plan(attended: int, total: int) -> Dict:
    """
    Generate attendance recovery plan.
    
    CONSTRAINT: Only for courses < 75% attendance
    
    Args:
        attended: Number of classes attended
        total: Total classes conducted
        
    Returns:
        Dictionary with recovery plan
    """
    current_percentage = (attended / total) * 100 if total > 0 else 0
    
    # Validate: Only for low attendance
    if current_percentage >= (VIT_MIN_ATTENDANCE * 100):
        return {
            "error": "Attendance is already above 75%",
            "current_percentage": current_percentage
        }
    
    # Calculate deficit
    min_required = total * VIT_MIN_ATTENDANCE
    deficit = attended - min_required
    
    # Recovery calculation
    total_projected = total + ESTIMATED_REMAINING_CLASSES
    min_required_final = total_projected * VIT_MIN_ATTENDANCE
    classes_needed = int(min_required_final - attended)
    
    # Check feasibility
    if classes_needed <= ESTIMATED_REMAINING_CLASSES:
        recovery_possible = True
        final_attendance = attended + classes_needed
        final_percentage = (final_attendance / total_projected) * 100
        
        action_items = [
            f"Attend {classes_needed} out of next {ESTIMATED_REMAINING_CLASSES} classes",
            "Set calendar reminders for each class",
            "Sit in front rows to show commitment",
            "Inform faculty about recovery effort",
            "Check VTOP daily for updates"
        ]
    else:
        recovery_possible = False
        final_percentage = None
        
        action_items = [
            "Recovery through regular attendance not possible",
            "Attend ALL remaining classes",
            "Options:",
            "  - Medical certificate (if applicable)",
            "  - HOD petition with valid reason",
            "  - Faculty advisor consultation"
        ]
    
    # Generate weekly schedule
    weeks = ESTIMATED_REMAINING_CLASSES // 2
    weekly_schedule = []
    for week in range(1, weeks + 1):
        if week <= 2:
            status = "CRITICAL"
            attend = "ALL"
        else:
            status = "RECOVERY"
            attend = "MOST"
        
        weekly_schedule.append({
            "week": week,
            "attend": attend,
            "status": status
        })
    
    return {
        "current_status": {
            "percentage": round(current_percentage, 2),
            "deficit": int(deficit),
            "status": "CRITICAL"
        },
        "recovery_plan": {
            "recovery_possible": recovery_possible,
            "classes_to_attend": classes_needed if recovery_possible else ESTIMATED_REMAINING_CLASSES,
            "estimated_remaining": ESTIMATED_REMAINING_CLASSES,
            "final_percentage": round(final_percentage, 2) if final_percentage else None,
            "action_items": action_items
        },
        "weekly_schedule": weekly_schedule
    }


def run_attendance_recovery(vtop_data: Dict) -> List[Dict]:
    """
    Run attendance recovery planner for courses below 75%.
    
    Args:
        vtop_data: Dictionary containing VTOP data
        
    Returns:
        List of recovery plans
    """
    print_section("ATTENDANCE RECOVERY PLANNER (Courses < 75%)")
    
    attendance_records = vtop_data.get("attendance", [])
    
    # Filter low attendance courses
    low_attendance_courses = [
        rec for rec in attendance_records
        if rec.get("percentage", 100) < 75
    ]
    
    if not low_attendance_courses:
        print("  ✅ All courses above 75% attendance")
        print("  No recovery plan needed")
        return []
    
    print(f"  ⚠️ Found {len(low_attendance_courses)} courses below 75%\n")
    
    results = []
    
    for record in low_attendance_courses:
        course_code = record.get("course_code", "")
        course_name = record.get("course_name", "")
        attended = record.get("attended", 0)
        total = record.get("total", 0)
        
        result = generate_recovery_plan(attended, total)
        result["course_code"] = course_code
        result["course_name"] = course_name
        results.append(result)
        
        # Display result
        recovery_possible = result["recovery_plan"]["recovery_possible"]
        icon = "✅" if recovery_possible else "❌"
        
        lines = [
            f"Course: {course_code} - {course_name}",
            f"Current: {result['current_status']['percentage']}%",
            f"Deficit: {result['current_status']['deficit']} classes",
            ""
        ]
        
        if recovery_possible:
            lines.append(f"{icon} Recovery Possible")
            lines.append(f"Attend: {result['recovery_plan']['classes_to_attend']} classes")
            lines.append(f"Final: ~{result['recovery_plan']['final_percentage']}%")
        else:
            lines.append(f"{icon} Standard Recovery Not Possible")
        
        lines.append("")
        lines.append("Action Items:")
        for item in result["recovery_plan"]["action_items"]:
            lines.append(f"  • {item}")
        
        print_box(f"⚠️ {course_code}", lines)
        print()
    
    return results


if __name__ == "__main__":
    import json
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python attendance_recovery.py <data_file.json>")
        sys.exit(1)
    
    # Load data
    with open(sys.argv[1], 'r') as f:
        vtop_data = json.load(f)
    
    # Run analysis
    print_section("ATTENDANCE RECOVERY PLANNER")
    results = run_attendance_recovery(vtop_data)
    
    if not results:
        print("✅ All courses have safe attendance (≥75%)")


__all__ = ["generate_recovery_plan", "run_attendance_recovery"]
