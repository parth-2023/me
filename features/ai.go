package features

import (
	"cli-top/helpers"
	"cli-top/types"
	"errors"
	"fmt"
	"time"
)

const cgpaHistoryURL = "https://vtop.vit.ac.in/vtop/examinations/examGradeView/StudentGradeHistory"

// BuildAIData aggregates VTOP datasets into a single payload for the AI subsystem.
func BuildAIData(regNo string, cookies types.Cookies) (types.VTOPAIData, error) {
	var data types.VTOPAIData

	// ensure slices stay non-nil so downstream JSON marshalling emits [] instead of null
	data.Marks = make([]types.CourseMarksSummary, 0)
	data.Attendance = make([]types.AttendanceRecord, 0)
	data.Exams = make([]types.ExamEvent, 0)
	data.Timetable = make([]types.TimetableEntry, 0)
	data.Assignments = make([]types.AssignmentSummary, 0)
	data.Leaves = make([]types.LeaveApplication, 0)
	data.CGPATrend = make([]types.CGPASnapshot, 0)

	if !helpers.ValidateLogin(cookies) {
		return data, errors.New("invalid login session")
	}

	data.RegNo = regNo
	data.GeneratedAt = time.Now()

	semesters, err := helpers.GetSemDetails(cookies, regNo)
	if err != nil {
		return data, err
	}
	if len(semesters) > 0 {
		// Use the LAST semester (most recent/current) instead of first (oldest)
		data.Semester = semesters[len(semesters)-1].SemName
	}

	var resultErr error

	if snapshot, err := FetchCgpaSnapshot(regNo, cookies, cgpaHistoryURL); err != nil {
		resultErr = errors.Join(resultErr, fmt.Errorf("cgpa snapshot: %w", err))
	} else {
		data.CGPA = snapshot.CGPA
		data.CGPATrend = append(data.CGPATrend, snapshot)
	}

	if marks, err := FetchMarksSummary(regNo, cookies); err != nil {
		resultErr = errors.Join(resultErr, fmt.Errorf("marks summary: %w", err))
	} else if len(marks) > 0 {
		data.Marks = marks
	}

	if attendance, err := FetchAttendanceSummary(regNo, cookies); err != nil {
		resultErr = errors.Join(resultErr, fmt.Errorf("attendance summary: %w", err))
	} else if len(attendance) > 0 {
		data.Attendance = attendance
	}

	if exams, err := FetchExamScheduleData(regNo, cookies); err != nil {
		resultErr = errors.Join(resultErr, fmt.Errorf("exam schedule: %w", err))
	} else if len(exams) > 0 {
		data.Exams = exams
	}

	if timetable, err := FetchTimetableEntries(regNo, cookies); err != nil {
		resultErr = errors.Join(resultErr, fmt.Errorf("timetable: %w", err))
	} else if len(timetable) > 0 {
		data.Timetable = timetable
	}

	if assignments, err := FetchPendingAssignments(regNo, cookies); err != nil {
		resultErr = errors.Join(resultErr, fmt.Errorf("assignments: %w", err))
	} else if len(assignments) > 0 {
		data.Assignments = assignments
	}

	if leaves, err := FetchLeaveStatusSummary(regNo, cookies); err != nil {
		resultErr = errors.Join(resultErr, fmt.Errorf("leave status: %w", err))
	} else if len(leaves) > 0 {
		data.Leaves = leaves
	}

	return data, resultErr
}
