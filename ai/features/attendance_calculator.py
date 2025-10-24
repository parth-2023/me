"""
Feature 1: Attendance Buffer Calculator
Pure algorithmic - No API calls required
"""

import math
from typing import Dict, List, Optional
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.constants import (
    VIT_MIN_ATTENDANCE,
    VIT_EXEMPTION_CGPA,
    ESTIMATED_REMAINING_CLASSES,
)
from utils.formatters import print_box, print_section, format_percentage


def calculate_attendance_buffer(
    attended: int,
    total: int,
    cgpa: Optional[float] = None
) -> Dict:
    """
    Calculate attendance buffer without API calls.
    
    Algorithm:
    1. Calculate minimum required: min_req = ceil(total * 0.75)
    2. Calculate buffer: buffer = attended - min_req
    3. Project scenarios for remaining classes
    4. Determine safe skip count
    5. Check CGPA exemption (>= 9.0)
    
    Args:
        attended: Number of classes attended
        total: Total classes conducted
        cgpa: Student's CGPA (optional, for exemption check)
        
    Returns:
        Dictionary with buffer analysis and scenarios
    """
    # Step 1: Current status
    min_required = math.ceil(total * VIT_MIN_ATTENDANCE)
    current_buffer = attended - min_required
    current_percentage = (attended / total) * 100 if total > 0 else 0
    
    # Step 2: Check exemption
    is_exempted = cgpa is not None and cgpa >= VIT_EXEMPTION_CGPA
    
    if is_exempted:
        return {
            "buffer": float('inf'),
            "can_skip": "UNLIMITED",
            "status": "EXEMPTED",
            "current_status": {
                "percentage": round(current_percentage, 2),
                "buffer": current_buffer,
                "status": "EXEMPTED"
            },
            "message": f"CGPA {cgpa} grants attendance exemption",
            "recommendations": [
                f"CGPA {cgpa} grants attendance exemption",
                "No attendance requirement",
                "Continue maintaining academic excellence"
            ],
            "scenarios": []
        }
    
    # Step 3: Project future scenarios
    total_projected = total + ESTIMATED_REMAINING_CLASSES
    scenarios = []
    
    for skip_count in range(ESTIMATED_REMAINING_CLASSES + 1):
        attended_projected = attended + (ESTIMATED_REMAINING_CLASSES - skip_count)
        final_percentage = (attended_projected / total_projected) * 100
        is_safe = final_percentage >= (VIT_MIN_ATTENDANCE * 100)
        
        scenarios.append({
            "skip": skip_count,
            "final_percentage": round(final_percentage, 2),
            "safe": is_safe
        })
    
    # Step 4: Find safe skip count
    safe_skip_count = 0
    for scenario in scenarios:
        if scenario["safe"]:
            safe_skip_count = scenario["skip"]
        else:
            break
    
    # Step 5: Determine status
    if current_buffer >= 5:
        status = "SAFE"
        recommendation = f"You can skip {safe_skip_count} classes comfortably"
    elif current_buffer > 0:
        status = "CAUTION"
        recommendation = f"Limited buffer. Skip only {safe_skip_count} classes if necessary"
    else:
        status = "CRITICAL"
        recommendation = "Below 75%! Attend ALL remaining classes"
    
    return {
        "current_status": {
            "percentage": round(current_percentage, 2),
            "buffer": current_buffer,
            "status": status
        },
        "can_skip": safe_skip_count,
        "recommendations": [recommendation],
        "scenarios": scenarios
    }


def run_attendance_calculator(vtop_data: Dict) -> List[Dict]:
    """
    Run attendance buffer calculator for all courses.
    
    Args:
        vtop_data: Dictionary containing VTOP data
        
    Returns:
        List of attendance analysis results
    """
    print_section("ATTENDANCE BUFFER CALCULATOR")
    
    attendance_records = vtop_data.get("attendance", [])
    cgpa = vtop_data.get("cgpa", 0.0)
    
    if not attendance_records:
        print("  FAIL No attendance data found")
        return []
    
    results = []
    
    for record in attendance_records:
        course_code = record.get("course_code", "")
        course_name = record.get("course_name", "")
        attended = record.get("attended", 0)
        total = record.get("total", 0)
        
        if total == 0:
            continue
        
        result = calculate_attendance_buffer(attended, total, cgpa)
        result["course_code"] = course_code
        result["course_name"] = course_name
        results.append(result)
        
        # Display result
        status = result["current_status"]["status"]
        icon = "OK" if status == "SAFE" else "WARN" if status == "CAUTION" else "FAIL"
        
        lines = [
            f"Course: {course_code} - {course_name}",
            f"Current: {result['current_status']['percentage']}%",
            f"Status: {icon} {status}",
            f"Buffer: {result['current_status']['buffer']} classes",
            f"Can Skip: {result['can_skip']} classes",
            "",
            "Scenarios:"
        ]
        
        for scenario in result["scenarios"][:6]:  # Show first 6 scenarios
            safe_icon = "OK" if scenario["safe"] else "FAIL"
            lines.append(
                f"  {safe_icon} Skip {scenario['skip']}: {scenario['final_percentage']}%"
            )
        
        print_box(f"{icon} {course_code}", lines)
        print()
    
    return results


if __name__ == "__main__":
    import json
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python attendance_calculator.py <data_file.json>")
        sys.exit(1)
    
    # Load data
    with open(sys.argv[1], 'r') as f:
        vtop_data = json.load(f)
    
    # Run analysis
    print_section("ATTENDANCE BUFFER CALCULATOR")
    results = run_attendance_calculator(vtop_data)
    
    if not results:
        print("FAIL No attendance data available for analysis")


__all__ = ["calculate_attendance_buffer", "run_attendance_calculator"]
