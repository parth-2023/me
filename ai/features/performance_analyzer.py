"""
Performance Trend Analyzer - Non-API AI Feature
Analyzes performance trends across semesters and predicts trajectory.
"""

from typing import Dict, List, Optional
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.formatters import print_section, print_box


def calculate_trend(data_points: List[float]) -> Dict:
    """
    Calculate trend from data points using simple linear regression.
    
    Args:
        data_points: List of values over time
        
    Returns:
        Dictionary with trend analysis
    """
    if len(data_points) < 2:
        return {
            "trend": "INSUFFICIENT_DATA",
            "slope": 0.0,
            "direction": "STABLE",
            "r_squared": 0.0,
            "confidence": "LOW"
        }
    
    n = len(data_points)
    x = list(range(n))
    y = data_points
    
    # Calculate slope using simple linear regression
    x_mean = sum(x) / n
    y_mean = sum(y) / n
    
    numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
    denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
    
    if denominator == 0:
        slope = 0
    else:
        slope = numerator / denominator
    
    # Determine trend direction
    if slope > 0.1:
        direction = "IMPROVING"
    elif slope < -0.1:
        direction = "DECLINING"
    else:
        direction = "STABLE"
    
    # Calculate R-squared (goodness of fit)
    predicted = [y_mean + slope * (x[i] - x_mean) for i in range(n)]
    ss_res = sum((y[i] - predicted[i]) ** 2 for i in range(n))
    ss_tot = sum((y[i] - y_mean) ** 2 for i in range(n))
    
    r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
    
    return {
        "trend": direction,
        "slope": round(slope, 4),
        "direction": direction,
        "r_squared": round(r_squared, 4),
        "confidence": "HIGH" if r_squared > 0.7 else "MEDIUM" if r_squared > 0.4 else "LOW"
    }


def analyze_cgpa_trend(cgpa_history: List[Dict]) -> Dict:
    """
    Analyze CGPA trend over semesters.
    
    Args:
        cgpa_history: List of semester CGPA records
        
    Returns:
        Trend analysis with predictions
    """
    if not cgpa_history:
        return {"error": "No CGPA history available"}
    
    # Extract CGPA values
    cgpa_values = [sem.get("cgpa", 0.0) for sem in cgpa_history]
    
    # Calculate trend
    trend_info = calculate_trend(cgpa_values)
    
    # Predict next semester
    if len(cgpa_values) >= 2 and trend_info["slope"] != 0:
        last_cgpa = cgpa_values[-1]
        predicted_next = last_cgpa + trend_info["slope"]
        predicted_next = max(0.0, min(10.0, predicted_next))
    else:
        predicted_next = cgpa_values[-1]
    
    # Calculate statistics
    avg_cgpa = sum(cgpa_values) / len(cgpa_values)
    max_cgpa = max(cgpa_values)
    min_cgpa = min(cgpa_values)
    
    return {
        "current_cgpa": cgpa_values[-1],
        "trend": trend_info["direction"],
        "slope": trend_info["slope"],
        "confidence": trend_info["confidence"],
        "r_squared": trend_info["r_squared"],
        "predicted_next": round(predicted_next, 2),
        "statistics": {
            "average": round(avg_cgpa, 2),
            "maximum": max_cgpa,
            "minimum": min_cgpa,
            "volatility": round(max_cgpa - min_cgpa, 2)
        },
        "semester_count": len(cgpa_values)
    }


def analyze_attendance_consistency(attendance_data: List[Dict]) -> Dict:
    """
    Analyze attendance consistency across courses.
    
    Args:
        attendance_data: List of attendance records
        
    Returns:
        Consistency analysis
    """
    if not attendance_data:
        return {"error": "No attendance data available"}
    
    percentages = [att.get("percentage", att.get("attendance_percentage", 0)) for att in attendance_data]
    
    avg_attendance = sum(percentages) / len(percentages)
    max_attendance = max(percentages)
    min_attendance = min(percentages)
    
    # Calculate standard deviation
    variance = sum((x - avg_attendance) ** 2 for x in percentages) / len(percentages)
    std_dev = variance ** 0.5
    
    # Determine consistency level
    if std_dev < 5:
        consistency = "VERY_CONSISTENT"
    elif std_dev < 10:
        consistency = "CONSISTENT"
    elif std_dev < 15:
        consistency = "MODERATE"
    else:
        consistency = "INCONSISTENT"
    
    # Count critical courses
    critical_count = sum(1 for p in percentages if p < 75)
    warning_count = sum(1 for p in percentages if 75 <= p < 80)
    
    return {
        "average": round(avg_attendance, 2),
        "maximum": max_attendance,
        "minimum": min_attendance,
        "std_deviation": round(std_dev, 2),
        "consistency": consistency,
        "critical_courses": critical_count,
        "warning_courses": warning_count,
        "safe_courses": len(percentages) - critical_count - warning_count
    }


def run_performance_analyzer(vtop_data: Dict) -> Dict:
    """
    Run comprehensive performance trend analysis.
    
    Args:
        vtop_data: Dictionary containing VTOP data
        
    Returns:
        Complete analysis results
    """
    print_section("PERFORMANCE TREND ANALYZER")
    
    cgpa_history = vtop_data.get("cgpa_trend", [])
    attendance = vtop_data.get("attendance", [])
    
    results = {}
    
    # Analyze CGPA trend
    if cgpa_history:
        cgpa_analysis = analyze_cgpa_trend(cgpa_history)
        
        if "error" in cgpa_analysis:
            print(f"  ℹ️  {cgpa_analysis['error']}")
            print()
        else:
            results["cgpa_trend"] = cgpa_analysis
            
            lines = [
                f"Current CGPA: {cgpa_analysis['current_cgpa']}",
                f"Trend: {cgpa_analysis['trend']}",
                f"Slope: {cgpa_analysis['slope']} per semester",
                f"Confidence: {cgpa_analysis['confidence']} (R² = {cgpa_analysis['r_squared']})",
                "",
                f"Predicted Next Semester: {cgpa_analysis['predicted_next']}",
                "",
                "Statistics:",
                f"  • Average: {cgpa_analysis['statistics']['average']}",
                f"  • Maximum: {cgpa_analysis['statistics']['maximum']}",
                f"  • Minimum: {cgpa_analysis['statistics']['minimum']}",
                f"  • Volatility: {cgpa_analysis['statistics']['volatility']}"
            ]
            
            icon = "📈" if cgpa_analysis['trend'] == "IMPROVING" else "📉" if cgpa_analysis['trend'] == "DECLINING" else "➡️"
            print_box(f"{icon} CGPA Trend", lines)
            print()
    
    # Analyze attendance consistency
    if attendance:
        att_analysis = analyze_attendance_consistency(attendance)
        
        if "error" in att_analysis:
            print(f"  ℹ️  {att_analysis['error']}")
            print()
        else:
            results["attendance_consistency"] = att_analysis
            
            lines = [
                f"Average Attendance: {att_analysis['average']}%",
                f"Consistency: {att_analysis['consistency']}",
                f"Standard Deviation: {att_analysis['std_deviation']}%",
                "",
                "Course Distribution:",
                f"  🟢 Safe (≥80%): {att_analysis['safe_courses']} courses",
                f"  🟡 Warning (75-80%): {att_analysis['warning_courses']} courses",
                f"  🔴 Critical (<75%): {att_analysis['critical_courses']} courses"
            ]
            
            print_box("📊 Attendance Consistency", lines)
            print()
    
    # Generate insights
    print_section("KEY INSIGHTS")
    
    cgpa_analysis = results.get("cgpa_trend", {})
    att_analysis = results.get("attendance_consistency", {})
    
    if cgpa_analysis and cgpa_analysis.get('trend') == "IMPROVING":
        print("  ✅ Your CGPA is showing positive improvement")
        print(f"     Predicted to reach {cgpa_analysis['predicted_next']} next semester")
    elif cgpa_analysis and cgpa_analysis.get('trend') == "DECLINING":
        print("  ⚠️  Your CGPA is declining - action needed")
        print("     Review study habits and seek academic support")
    
    if att_analysis and att_analysis.get('critical_courses', 0) > 0:
        print(f"  🚨 {att_analysis['critical_courses']} course(s) below 75% attendance")
        print("     Focus on attendance recovery immediately")
    elif att_analysis and att_analysis.get('consistency') in ["VERY_CONSISTENT", "CONSISTENT"]:
        print("  ✅ Excellent attendance consistency maintained")
    
    print()
    
    return results


if __name__ == "__main__":
    import json
    
    if len(sys.argv) < 2:
        print("Usage: python performance_analyzer.py <data_file.json>")
        sys.exit(1)
    
    # Load data
    with open(sys.argv[1], 'r') as f:
        vtop_data = json.load(f)
    
    # Run analysis
    print_section("PERFORMANCE TREND ANALYZER")
    results = run_performance_analyzer(vtop_data)
    
    if not results:
        print("❌ No performance data available for analysis")
