#!/usr/bin/env python3
"""
All-Features Runner
Executes all non-API AI features sequentially with formatted output
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

# Add features directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Feature imports
from features.attendance_calculator import run_attendance_calculator
from features.grade_predictor import run_grade_predictor
from features.cgpa_analyzer import run_cgpa_analyzer
from features.attendance_recovery import run_attendance_recovery
from features.exam_readiness import run_exam_readiness
from features.study_allocator import run_study_allocator
from features.performance_analyzer import run_performance_analyzer
from features.target_planner import run_target_planner
from features.weakness_identifier import run_weakness_identifier

# Utilities
from utils.formatters import print_header, print_section


def load_vtop_data(json_path: str) -> Dict[str, Any]:
    """Load VTOP data from JSON file."""
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"FAIL Error: File not found: {json_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"FAIL Error: Invalid JSON: {e}")
        sys.exit(1)


def run_all_features(vtop_data: Dict[str, Any]):
    """
    Execute all 9 non-API features sequentially.
    
    Features:
    1. Attendance Buffer Calculator
    2. Grade Predictor (with missing marks prediction)
    3. CGPA Impact Analyzer
    4. Attendance Recovery Planner
    5. Exam Readiness Scorer
    6. Study Time Allocator
    7. Performance Trend Analyzer
    8. Grade Target Planner
    9. Weakness Identifier (by subject type)
    """
    
    print_header("CLI-TOP AI FEATURES - COMPREHENSIVE REPORT")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Student: {vtop_data.get('reg_no', 'N/A')}")
    print(f"Semester: {vtop_data.get('semester', 'N/A')}")
    print(f"CGPA: {vtop_data.get('cgpa', 'N/A')}")
    print("=" * 80)
    print()
    
    feature_count = 0
    
    # Feature 1: Attendance Buffer Calculator
    print_section("1. ATTENDANCE BUFFER ANALYSIS")
    try:
        attendance_results = run_attendance_calculator(vtop_data)
        if attendance_results:
            print(f"  OK Attendance analysis completed for {len(attendance_results)} courses")
            feature_count += 1
        print()
    except Exception as e:
        print(f"  FAIL Failed: {e}")
        print()
    
    # Feature 2: Grade Predictor
    print_section("2. GRADE PREDICTION (Courses with Missing FAT)")
    try:
        grade_results = run_grade_predictor(vtop_data)
        if grade_results:
            print(f"  OK Grade prediction completed for {len(grade_results)} courses")
            feature_count += 1
        print()
    except Exception as e:
        print(f"  FAIL Failed: {e}")
        print()
    
    # Feature 3: CGPA Impact Analyzer
    print_section("3. CGPA IMPACT ANALYSIS (Incomplete Courses)")
    try:
        cgpa_results = run_cgpa_analyzer(vtop_data)
        if cgpa_results:
            print(f"  OK CGPA impact analysis completed")
            feature_count += 1
        print()
    except Exception as e:
        print(f"  FAIL Failed: {e}")
        print()
    
    # Feature 4: Attendance Recovery Planner
    print_section("4. ATTENDANCE RECOVERY PLAN (Courses < 75%)")
    try:
        recovery_results = run_attendance_recovery(vtop_data)
        if recovery_results:
            print(f"  OK Recovery plans generated for {len(recovery_results)} courses")
            feature_count += 1
        print()
    except Exception as e:
        print(f"  FAIL Failed: {e}")
        print()
    
    # Feature 5: Exam Readiness Scorer
    print_section("5. EXAM READINESS ASSESSMENT")
    try:
        readiness_results = run_exam_readiness(vtop_data)
        if readiness_results:
            print(f"  OK Exam readiness analysis completed for {len(readiness_results)} exams")
            feature_count += 1
        print()
    except Exception as e:
        print(f"  FAIL Failed: {e}")
        print()
    
    # Feature 6: Study Time Allocator
    print_section("6. STUDY TIME ALLOCATION")
    try:
        study_results = run_study_allocator(vtop_data, total_hours=40)
        if study_results:
            print(f"  OK Study time allocated across {len(study_results)} courses")
            feature_count += 1
        print()
    except Exception as e:
        print(f"  FAIL Failed: {e}")
        print()
    
    # Feature 7: Performance Trend Analyzer
    print_section("7. PERFORMANCE TRENDS")
    try:
        performance_results = run_performance_analyzer(vtop_data)
        if performance_results:
            print(f"  OK Performance trends analyzed")
            feature_count += 1
        print()
    except Exception as e:
        print(f"  FAIL Failed: {e}")
        print()
    
    # Feature 8: Grade Target Planner
    print_section("8. GRADE TARGET PLANNING (Target: 9.0 CGPA)")
    try:
        target_cgpa = 9.0  # Can be made configurable
        target_results = run_target_planner(vtop_data, target_cgpa=target_cgpa, remaining_semesters=1)
        if target_results:
            print(f"  OK Target plan generated")
            feature_count += 1
        print()
    except Exception as e:
        print(f"  FAIL Failed: {e}")
        print()
    
    # Feature 9: Weakness Identifier
    print_section("9. WEAKNESS IDENTIFICATION")
    try:
        weakness_results = run_weakness_identifier(vtop_data)
        if weakness_results:
            print(f"  OK Weakness analysis completed")
            feature_count += 1
        print()
    except Exception as e:
        print(f"  FAIL Failed: {e}")
        print()
    
    # Summary
    print("=" * 80)
    print_header("SUMMARY")
    print(f"OK Features executed: {feature_count}/9")
    print(f"STATS Total courses: {len(vtop_data.get('marks', []))}")
    print(f"TIME Execution time: <1 second (no API calls)")
    print()
    print("TIP All features work offline without API keys")
    print("=" * 80)


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("=" * 80)
        print("CLI-TOP AI Features Runner (Non-API)")
        print("=" * 80)
        print()
        print("Usage: python run_all_features.py <vtop_data.json>")
        print()
        print("Example:")
        print("  python run_all_features.py sample_data/sample_dataset.json")
        print()
        print("Features:")
        print("  1. Attendance Buffer Calculator")
        print("  2. Grade Predictor (with missing marks prediction)")
        print("  3. CGPA Impact Analyzer")
        print("  4. Attendance Recovery Planner")
        print("  5. Exam Readiness Scorer")
        print("  6. Study Time Allocator")
        print("  7. Performance Trend Analyzer")
        print("  8. Grade Target Planner")
        print("  9. Weakness Identifier (by subject type)")
        print()
        print("Note: All features work offline without API keys")
        print("=" * 80)
        sys.exit(1)
    
    json_path = sys.argv[1]
    vtop_data = load_vtop_data(json_path)
    
    run_all_features(vtop_data)


if __name__ == "__main__":
    main()
