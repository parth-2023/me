"""Constants for VIT grading and attendance calculations."""

from typing import Dict, List, Tuple

# VIT Attendance Policy
VIT_MIN_ATTENDANCE = 0.75
VIT_EXEMPTION_CGPA = 9.0
ESTIMATED_REMAINING_CLASSES = 10

# VIT Grade Weights
VIT_GRADE_WEIGHTS = {
    "CAT1": 0.15,
    "CAT2": 0.15,
    "ASSIGNMENT": 0.10,
    "FAT": 0.60
}

# VIT Grade Thresholds (Absolute)
VIT_GRADE_THRESHOLDS = {
    "S": 90.0,
    "A": 80.0,
    "B": 70.0,
    "C": 60.0,
    "D": 50.0,
    "F": 0.0
}

# Grade Points for CGPA calculation
GRADE_POINTS = {
    "S": 10,
    "A": 9,
    "B": 8,
    "C": 7,
    "D": 6,
    "F": 0
}

# Grade order for comparison
GRADE_ORDER: List[str] = ["S", "A", "B", "C", "D", "F"]

# Attendance status thresholds
ATTENDANCE_STATUS = {
    "SAFE": 80.0,
    "CAUTION": 75.0,
    "CRITICAL": 0.0
}

__all__ = [
    "VIT_MIN_ATTENDANCE",
    "VIT_EXEMPTION_CGPA",
    "VIT_GRADE_WEIGHTS",
    "VIT_GRADE_THRESHOLDS",
    "GRADE_POINTS",
    "GRADE_ORDER",
    "ATTENDANCE_STATUS",
    "ESTIMATED_REMAINING_CLASSES",
]
