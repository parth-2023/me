"""Non-API AI features package."""

from .attendance_calculator import calculate_attendance_buffer, run_attendance_calculator
from .grade_predictor import predict_grade_comprehensive, run_grade_predictor
from .cgpa_analyzer import analyze_cgpa_impact, run_cgpa_analyzer
from .attendance_recovery import generate_recovery_plan, run_attendance_recovery
from .exam_readiness import calculate_exam_readiness, run_exam_readiness

__all__ = [
    "calculate_attendance_buffer",
    "run_attendance_calculator",
    "predict_grade_comprehensive",
    "run_grade_predictor",
    "analyze_cgpa_impact",
    "run_cgpa_analyzer",
    "generate_recovery_plan",
    "run_attendance_recovery",
    "calculate_exam_readiness",
    "run_exam_readiness",
]
