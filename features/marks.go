package features

import (
	"bytes"
	"cli-top/debug"
	"cli-top/helpers"
	"cli-top/types"
	"errors"
	"fmt"
	"strconv"
	"strings"

	"github.com/PuerkitoBio/goquery"
)

const (
	MarksTableContentSelector   = "tr.tableContent"
	MarksCustomTableSelector    = "customTable-level1"
	MarksRowsSelector           = "tbody tr"
	MarksCellSelector           = "td"
	MarksGPASpanSelector        = "span[style='font-size: 18px; font-weight: bold;']"
	MarksTitleCellIndex         = 1
	MarksMaxMarkCellIndex       = 2
	MarksWeightageCellIndex     = 3
	MarksStatusCellIndex        = 4
	MarksScoredMarkCellIndex    = 5
	MarksWeightageMarkCellIndex = 6
	CourseCodeCellIndex         = 2
	CourseTitleCellIndex        = 3
	CourseTypeCellIndex         = 4
	CourseFacultyCellIndex      = 6
	CourseSlotCellIndex         = 7
)

// FetchMarksSummary retrieves marks data for the latest available semester without printing to stdout.
func FetchMarksSummary(regNo string, cookies types.Cookies) ([]types.CourseMarksSummary, error) {
	if !helpers.ValidateLogin(cookies) {
		return nil, errors.New("invalid login session")
	}

	semesters, err := helpers.GetSemDetails(cookies, regNo)
	if err != nil {
		return nil, err
	}
	if len(semesters) == 0 {
		return nil, errors.New("no semesters available")
	}

	// Use the LAST semester (most recent/current) instead of first (oldest)
	selectedSem := semesters[len(semesters)-1]
	url := "https://vtop.vit.ac.in/vtop/examinations/doStudentMarkView"

	payload := fmt.Sprintf(
		"------WebKitFormBoundary9yjNZXu7BBjgQK7J\r\nContent-Disposition: form-data; name=\"authorizedID\"\r\n\r\n%s\r\n------WebKitFormBoundary9yjNZXu7BBjgQK7J\r\nContent-Disposition: form-data; name=\"semesterSubId\"\r\n\r\n%s\r\n------WebKitFormBoundary9yjNZXu7BBjgQK7J\r\nContent-Disposition: form-data; name=\"_csrf\"\r\n\r\n%s\r\n------WebKitFormBoundary9yjNZXu7BBjgQK7J--\r\n",
		regNo,
		selectedSem.SemID,
		cookies.CSRF,
	)

	bodyText, err := helpers.FetchReq(regNo, cookies, url, selectedSem.SemID, payload, "POST", "marks")
	if err != nil {
		return nil, err
	}

	doc, err := goquery.NewDocumentFromReader(bytes.NewReader(bodyText))
	if err != nil {
		return nil, err
	}

	courseDetails := subjectDetails(doc)
	elements := findElementsByClass(doc, MarksCustomTableSelector)
	var summaries []types.CourseMarksSummary

	cleanNumber := func(s string) string {
		s = strings.TrimSpace(s)
		s = strings.TrimSuffix(s, "%")
		s = strings.ReplaceAll(s, "%", "")
		s = strings.ReplaceAll(s, ",", "")
		return strings.TrimSpace(s)
	}

	for idx, course := range courseDetails {
		if idx >= len(elements) {
			continue
		}
		componentRows, _, _ := ExtractMarks(elements[idx])
		var components []types.CourseMarksComponent
		var totalWeight float64
		var totalScored float64

		for _, row := range componentRows {
			if len(row) < 6 {
				continue
			}
			component := types.CourseMarksComponent{
				Title:  strings.TrimSpace(row[MarksTitleCellIndex-1]),
				Status: strings.TrimSpace(row[MarksStatusCellIndex-1]),
			}

			if maxMarks, err := strconv.ParseFloat(cleanNumber(row[MarksMaxMarkCellIndex-1]), 64); err == nil {
				component.MaxMarks = maxMarks
			}
			if weightage, err := strconv.ParseFloat(cleanNumber(row[MarksWeightageCellIndex-1]), 64); err == nil {
				component.Weightage = weightage
				totalWeight += weightage
			}
			if scored, err := strconv.ParseFloat(cleanNumber(row[MarksScoredMarkCellIndex-1]), 64); err == nil {
				component.ScoredMarks = scored
			}
			if weightMark, err := strconv.ParseFloat(cleanNumber(row[MarksWeightageMarkCellIndex-1]), 64); err == nil {
				component.WeightageMark = weightMark
				totalScored += weightMark
			}

			components = append(components, component)
		}

		summary := types.CourseMarksSummary{
			CourseCode:  course.CourseCode,
			CourseTitle: course.CourseTitle,
			CourseType:  course.CourseType,
			Faculty:     course.Faculty,
			Slot:        course.Slot,
			Components:  components,
			TotalScored: totalScored,
			TotalWeight: totalWeight,
		}

		summaries = append(summaries, summary)
	}

	return summaries, nil
}

func GetMarks(regNo string, cookies types.Cookies, semID string, semChoice int) {
	if !helpers.ValidateLogin(cookies) {
		return
	}

	url := "https://vtop.vit.ac.in/vtop/examinations/doStudentMarkView"
	semester, err := helpers.SelectSemester(regNo, cookies, semChoice)
	if err != nil {
		helpers.HandleError("fetching semesters", err)
		fmt.Println()
		return
	}

	payload := fmt.Sprintf(
		"------WebKitFormBoundary9yjNZXu7BBjgQK7J\r\nContent-Disposition: form-data; name=\"authorizedID\"\r\n\r\n%s\r\n------WebKitFormBoundary9yjNZXu7BBjgQK7J\r\nContent-Disposition: form-data; name=\"semesterSubId\"\r\n\r\n%s\r\n------WebKitFormBoundary9yjNZXu7BBjgQK7J\r\nContent-Disposition: form-data; name=\"_csrf\"\r\n\r\n%s\r\n------WebKitFormBoundary9yjNZXu7BBjgQK7J--\r\n",
		regNo,
		semester.SemID,
		cookies.CSRF,
	)

	bodyText, err := helpers.FetchReq(regNo, cookies, url, semester.SemID, payload, "POST", "marks")
	if err != nil && debug.Debug {
		fmt.Println(err)
	}

	doc, err := goquery.NewDocumentFromReader(bytes.NewReader(bodyText))
	if err != nil && debug.Debug {
		fmt.Println(err)
	}

	courseDetails := subjectDetails(doc)

	elements := findElementsByClass(doc, MarksCustomTableSelector)

	if len(elements) == 0 {
		fmt.Println()
		in := "No Data Found"
		out := fmt.Sprintf("\033[1;31m%s\033[0m", in)
		fmt.Println(out)
		return
	}

	for idx, course := range courseDetails {
		if idx >= len(elements) {
			if debug.Debug {
				fmt.Printf("No corresponding table found for course: %s\n", course.CourseTitle)
			}
			continue
		}

		selectedElement := elements[idx]
		selectedCourseDetail := courseDetails[idx]

		OneSubTable, weightageMark, maxMarkSum := ExtractMarks(selectedElement)
		if err != nil && debug.Debug {
			fmt.Println(OneSubTable)
			fmt.Println(err)
		}
		if len(OneSubTable) == 0 {
			fmt.Printf("No Data Found for %s\n\n", selectedCourseDetail.CourseTitle)
			continue
		}

		courseDetail := fmt.Sprintf("\033[1;34m%s\033[0m", selectedCourseDetail.CourseTitle)
		fmt.Println(courseDetail)
		fmt.Println()

		headers := []string{"Title", "Max Marks", "Weightage %", "Status", "Scored Mark", "Weightage Mark"}

		tableData := append([][]string{headers}, OneSubTable...)

		helpers.PrintTable(tableData, 0)

		weightageMarkStr := fmt.Sprintf("\033[32m%.2f\033[0m", weightageMark)
		maxMarkSumStr := fmt.Sprintf("\033[32m%d\033[0m", maxMarkSum)
		fmt.Printf("\n%s/%s\n\n", weightageMarkStr, maxMarkSumStr)
	}

	doc.Find(MarksGPASpanSelector).Each(func(i int, s *goquery.Selection) {
		gpa := s.Text()
		fmt.Println("\x1b[32;1mCourse not included in GPA/CGPA\x1b[0m")
		fmt.Println(gpa)
	})
}

func subjectDetails(doc *goquery.Document) []types.CourseDetail {
	var details []types.CourseDetail

	doc.Find(MarksTableContentSelector).Each(func(i int, s *goquery.Selection) {
		if i%2 != 0 {
			return
		}

		td := s.Find(MarksCellSelector)
		courseCode := strings.TrimSpace(td.Eq(CourseCodeCellIndex).Text())
		courseTitle := strings.TrimSpace(td.Eq(CourseTitleCellIndex).Text())
		courseType := strings.TrimSpace(td.Eq(CourseTypeCellIndex).Text())
		faculty := strings.TrimSpace(td.Eq(CourseFacultyCellIndex).Text())
		slot := strings.TrimSpace(td.Eq(CourseSlotCellIndex).Text())

		course := types.CourseDetail{
			CourseCode:  courseCode,
			CourseTitle: courseTitle,
			CourseType:  courseType,
			Faculty:     faculty,
			Slot:        slot,
		}

		details = append(details, course)
	})
	return details
}

func findElementsByClass(doc *goquery.Document, class string) []*goquery.Selection {
	var result []*goquery.Selection

	doc.Find("." + class).Each(func(_ int, selection *goquery.Selection) {
		result = append(result, selection)
	})

	return result
}

func ExtractMarks(element *goquery.Selection) ([][]string, float64, int) {
	var SingleSubTable [][]string
	var weightageMarkSum float64
	var maxSubjectMarksSum int

	element.Find(MarksRowsSelector).Each(func(_ int, rowSelection *goquery.Selection) {
		firstCell := strings.TrimSpace(rowSelection.Find(MarksCellSelector).Eq(0).Text())
		if firstCell == "Sl.No." || firstCell == "Index" || firstCell == "" {
			return
		}

		title := strings.TrimSpace(rowSelection.Find(MarksCellSelector).Eq(MarksTitleCellIndex).Text())
		maxMark := strings.TrimSpace(rowSelection.Find(MarksCellSelector).Eq(MarksMaxMarkCellIndex).Text())
		weightage := strings.TrimSpace(rowSelection.Find(MarksCellSelector).Eq(MarksWeightageCellIndex).Text())
		status := strings.TrimSpace(rowSelection.Find(MarksCellSelector).Eq(MarksStatusCellIndex).Text())
		scoredMark := strings.TrimSpace(rowSelection.Find(MarksCellSelector).Eq(MarksScoredMarkCellIndex).Text())
		weightageMark := strings.TrimSpace(rowSelection.Find(MarksCellSelector).Eq(MarksWeightageMarkCellIndex).Text())

		SingleSubTable = append(SingleSubTable, []string{title, maxMark, weightage, status, scoredMark, weightageMark})

		weightageFloat, err := strconv.ParseFloat(weightageMark, 64)
		if err == nil {
			weightageMarkSum += weightageFloat
		}

		maxMarkInt, err := strconv.Atoi(weightage)
		if err == nil {
			maxSubjectMarksSum += maxMarkInt
		}
	})

	return SingleSubTable, weightageMarkSum, maxSubjectMarksSum
}
