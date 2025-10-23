package types

import "time"

// CourseMarksComponent represents a single assessment component within a course.
type CourseMarksComponent struct {
	Title         string  `json:"title"`
	MaxMarks      float64 `json:"max_marks"`
	Weightage     float64 `json:"weightage"`
	Status        string  `json:"status"`
	ScoredMarks   float64 `json:"scored_marks"`
	WeightageMark float64 `json:"weightage_mark"`
}

// CourseMarksSummary aggregates all assessment components and metadata for a course.
type CourseMarksSummary struct {
	CourseCode  string                 `json:"course_code"`
	CourseTitle string                 `json:"course_title"`
	CourseType  string                 `json:"course_type"`
	Faculty     string                 `json:"faculty"`
	Slot        string                 `json:"slot"`
	Components  []CourseMarksComponent `json:"components"`
	TotalScored float64                `json:"total_scored"`
	TotalWeight float64                `json:"total_weight"`
}

// AttendanceRecord captures attendance metrics for a single course.
type AttendanceRecord struct {
	CourseCode    string  `json:"course_code"`
	CourseName    string  `json:"course_name"`
	CourseType    string  `json:"course_type"`
	Faculty       string  `json:"faculty"`
	Attended      int     `json:"attended"`
	Total         int     `json:"total"`
	Percentage    float64 `json:"percentage"`
	Buffer        int     `json:"buffer"`
	LastUpdatedAt string  `json:"last_updated_at"`
}

// TimetableEntry describes a single scheduled class occurrence.
type TimetableEntry struct {
	Day        string `json:"day"`
	StartTime  string `json:"start_time"`
	EndTime    string `json:"end_time"`
	Course     string `json:"course"`
	CourseCode string `json:"course_code"`
	Slot       string `json:"slot"`
	Venue      string `json:"venue"`
	Faculty    string `json:"faculty"`
}

// AssignmentSummary stores details about pending or upcoming assignments.
type AssignmentSummary struct {
	CourseCode string    `json:"course_code"`
	CourseName string    `json:"course_name"`
	Title      string    `json:"title"`
	DueDate    time.Time `json:"due_date"`
	Status     string    `json:"status"`
	Link       string    `json:"link"`
}

// LeaveApplication summarises leave status entries.
type LeaveApplication struct {
	VisitPlace string `json:"visit_place"`
	Reason     string `json:"reason"`
	LeaveType  string `json:"leave_type"`
	From       string `json:"from"`
	To         string `json:"to"`
	Status     string `json:"status"`
}

// CGPASnapshot captures CGPA and related grade data for a semester.
type CGPASnapshot struct {
	Semester          string  `json:"semester"`
	CGPA              float64 `json:"cgpa"`
	CreditsRegistered int     `json:"credits_registered"`
	CreditsEarned     int     `json:"credits_earned"`
	SGrades           int     `json:"s_grades"`
	AGrades           int     `json:"a_grades"`
	BGrades           int     `json:"b_grades"`
	CGrades           int     `json:"c_grades"`
	DGrades           int     `json:"d_grades"`
	EGrades           int     `json:"e_grades"`
	FGrades           int     `json:"f_grades"`
	NGrades           int     `json:"n_grades"`
}

// VTOPAIData aggregates all datasets required by the AI assistant subsystem.
type VTOPAIData struct {
	RegNo       string               `json:"reg_no"`
	Semester    string               `json:"semester"`
	CGPA        float64              `json:"cgpa"`
	Marks       []CourseMarksSummary `json:"marks"`
	Attendance  []AttendanceRecord   `json:"attendance"`
	Exams       []ExamEvent          `json:"exams"`
	Timetable   []TimetableEntry     `json:"timetable"`
	Assignments []AssignmentSummary  `json:"assignments"`
	Leaves      []LeaveApplication   `json:"leaves"`
	CGPATrend   []CGPASnapshot       `json:"cgpa_trend"`
	GeneratedAt time.Time            `json:"generated_at"`
}
