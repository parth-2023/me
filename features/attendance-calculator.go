// features/attendance-calculator.go
package features

import (
	"cli-top/debug"
	"cli-top/helpers"
	types "cli-top/types"
	"errors"
	"fmt"
	"math"
	"regexp"
	"strconv"
	"strings"

	"github.com/PuerkitoBio/goquery"
	"golang.org/x/text/cases"
	"golang.org/x/text/language"
)

const (
	AttendanceTableSelector = "table#AttendanceDetailDataTable"
	AttendanceRowsSelector  = "tbody tr"
	AttendanceCellSelector  = "td"
)

var (
	reSubjectName = regexp.MustCompile(`-\s*(.*?)\s*-`)
	reSubjectType = regexp.MustCompile(`[^-]*$`)
	reProfessor   = regexp.MustCompile(`^(.*?)\s*-\s*`)
)

// FetchAttendanceSummary gathers attendance statistics for the latest semester without printing output.
func FetchAttendanceSummary(regNo string, cookies types.Cookies) ([]types.AttendanceRecord, error) {
	if !helpers.ValidateLogin(cookies) {
		return nil, errors.New("invalid login session")
	}

	semDetails, err := helpers.GetSemDetails(cookies, regNo)
	if err != nil {
		return nil, err
	}
	if len(semDetails) == 0 {
		return nil, errors.New("no semesters available")
	}

	url := "https://vtop.vit.ac.in/vtop/processViewStudentAttendance"

	// Start from the LAST semester (most recent/current) instead of first (oldest)
	for i := len(semDetails) - 1; i >= 0; i-- {
		semID := semDetails[i].SemID
		bodyText, err := helpers.FetchReq(regNo, cookies, url, semID, "UTC", "POST", "")
		if err != nil {
			if debug.Debug {
				fmt.Printf("error fetching attendance for semester %s: %v\n", semDetails[i].SemName, err)
			}
			continue
		}

		doc, err := goquery.NewDocumentFromReader(strings.NewReader(string(bodyText)))
		if err != nil {
			if debug.Debug {
				fmt.Printf("error parsing attendance html for semester %s: %v\n", semDetails[i].SemName, err)
			}
			continue
		}

		records := parseAttendanceRecords(doc)
		if len(records) > 0 {
			return records, nil
		}
	}

	return []types.AttendanceRecord{}, nil
}

func GetAttendance(regNo string, cookies types.Cookies, sem_choice int) {
	if !helpers.ValidateLogin(cookies) {
		return
	}
	url := "https://vtop.vit.ac.in/vtop/processViewStudentAttendance"

	semDetails, err := helpers.GetSemDetails(cookies, regNo)
	if err != nil {
		if debug.Debug {
			fmt.Printf("Error fetching semesters: %v\n", err)
		}
		fmt.Println("Please login using the cli-top login command.")
		return
	}

	if len(semDetails) == 0 {
		fmt.Println("No semesters found.")
		return
	}

	var semID string
	var attendanceList [][]string
	found := false

	// Iterate from the latest semester to the earliest
	for i := len(semDetails) - 1; i >= 0; i-- {
		semID = semDetails[i].SemID
		bodyText, err := helpers.FetchReq(regNo, cookies, url, semID, "UTC", "POST", "")
		if err != nil {
			if debug.Debug {
				fmt.Printf("Error fetching attendance for Semester %s: %v\n", semDetails[i].SemName, err)
			}
			continue // Try the previous semester
		}

		doc, err := goquery.NewDocumentFromReader(strings.NewReader(string(bodyText)))
		if err != nil {
			if debug.Debug {
				fmt.Printf("Error parsing HTML document for Semester %s: %v\n", semDetails[i].SemName, err)
			}
			continue // Try the previous semester
		}

		attendanceList = findAndSaveAttendance(doc)

		// Check if attendance data exists (more than header row)
		if len(attendanceList) > 1 {
			found = true
			if debug.Debug {
				fmt.Printf("Selected Semester: %s (%s)\n", semDetails[i].SemName, semID)
			}
			break
		} else {
			if debug.Debug {
				fmt.Printf("No attendance data found for Semester: %s (%s). Trying previous semester.\n", semDetails[i].SemName, semID)
			}
		}
	}

	// If no attendance data found in any semester
	if !found {
		fmt.Println("No attendance data available in any semester.")
		return
	}

	fmt.Println()
	helpers.PrintTable(attendanceList, 1)
	fmt.Println()
}

func findAndSaveAttendance(doc *goquery.Document) [][]string {
	var attendanceList [][]string
	attendanceList = append(attendanceList, []string{"Subject", "Type", "Faculty Name", "Classes Attended", "Percentage", "75% Alert"})

	table := doc.Find(AttendanceTableSelector)
	if table.Length() > 0 {
		table.Find(AttendanceRowsSelector).Each(func(i int, rowSelection *goquery.Selection) {
			sub_name_and_type := rowSelection.Find(AttendanceCellSelector).Eq(2).Find("span").Text()
			var sub_name string
			var sub_type string
			proff := rowSelection.Find(AttendanceCellSelector).Eq(4).Find("span").Text()
			attended := rowSelection.Find(AttendanceCellSelector).Eq(5).Find("span").Text()
			total := rowSelection.Find(AttendanceCellSelector).Eq(6).Find("span").Text()
			percent := rowSelection.Find(AttendanceCellSelector).Eq(7).Find("span").Find("span").Text()

			// Extract Subject Name
			match := reSubjectName.FindStringSubmatch(sub_name_and_type)
			if len(match) > 1 {
				sub_name = strings.TrimSpace(match[1])
			}

			// Extract Subject Type
			matchType := reSubjectType.FindString(sub_name_and_type)
			sub_type = strings.TrimSpace(matchType)

			// Normalize Faculty Name
			matchProf := reProfessor.FindStringSubmatch(proff)

			if len(matchProf) > 1 {
				caser := cases.Title(language.English)
				proff = caser.String(strings.ToLower(matchProf[1]))
			}

			// Classes Attended
			classes_attended := attended + "/" + total

			// Convert attended and total to integers
			attendedInt, err1 := strconv.Atoi(attended)
			totalInt, err2 := strconv.Atoi(total)
			if err1 != nil || err2 != nil {
				if debug.Debug {
					fmt.Printf("Error converting attendance numbers for subject %s: attended='%s', total='%s'\n", sub_name, attended, total)
				}
				return
			}

			// Calculate 75% Alert
			var missOrAttend string
			if sub_type == "Lab Only" || sub_type == "Embedded Lab" {
				attendedInt = attendedInt / 2
				totalInt = totalInt / 2
				missOrAttend = calculateAttendance(attendedInt, totalInt, 1)
			} else {
				missOrAttend = calculateAttendance(attendedInt, totalInt, 0)
			}

			attendanceList = append(attendanceList, []string{sub_name, sub_type, proff, classes_attended, percent, missOrAttend})
		})
	} else {
		if debug.Debug {
			fmt.Println("Table with ID 'AttendanceDetailDataTable' not found.")
		}
		fmt.Println("No attendance table found for the selected semester.")
	}

	return attendanceList
}

func parseAttendanceRecords(doc *goquery.Document) []types.AttendanceRecord {
	var records []types.AttendanceRecord

	table := doc.Find(AttendanceTableSelector)
	if table.Length() == 0 {
		return records
	}

	caser := cases.Title(language.English)
	targetAttendance := 0.7401

	table.Find(AttendanceRowsSelector).Each(func(i int, rowSelection *goquery.Selection) {
		subjectInfo := rowSelection.Find(AttendanceCellSelector).Eq(2).Find("span").Text()
		facultyRaw := rowSelection.Find(AttendanceCellSelector).Eq(4).Find("span").Text()
		attendedText := rowSelection.Find(AttendanceCellSelector).Eq(5).Find("span").Text()
		totalText := rowSelection.Find(AttendanceCellSelector).Eq(6).Find("span").Text()
		percentText := rowSelection.Find(AttendanceCellSelector).Eq(7).Find("span").Find("span").Text()

		if strings.TrimSpace(subjectInfo) == "" {
			return
		}

		parts := strings.Split(subjectInfo, "-")
		courseCode := strings.TrimSpace(parts[0])

		match := reSubjectName.FindStringSubmatch(subjectInfo)
		courseName := ""
		if len(match) > 1 {
			courseName = strings.TrimSpace(match[1])
		}

		courseType := strings.TrimSpace(reSubjectType.FindString(subjectInfo))

		faculty := facultyRaw
		if profMatch := reProfessor.FindStringSubmatch(facultyRaw); len(profMatch) > 1 {
			faculty = caser.String(strings.ToLower(strings.TrimSpace(profMatch[1])))
		}

		attended, err1 := strconv.Atoi(strings.TrimSpace(attendedText))
		total, err2 := strconv.Atoi(strings.TrimSpace(totalText))
		if err1 != nil || err2 != nil || total == 0 {
			return
		}

		adjustedAttended := attended
		adjustedTotal := total
		if courseType == "Lab Only" || courseType == "Embedded Lab" {
			adjustedAttended = attended / 2
			adjustedTotal = total / 2
		}

		percentageText := strings.ReplaceAll(percentText, "%", "")
		percentageText = strings.TrimSpace(percentageText)
		percentage, err := strconv.ParseFloat(percentageText, 64)
		if err != nil {
			percentage = math.Round(float64(attended)/float64(total)*100*100) / 100
		}

		neededAttendance := targetAttendance * float64(adjustedTotal)
		buffer := 0
		if float64(adjustedAttended) >= neededAttendance {
			buffer = int(math.Floor((float64(adjustedAttended) - neededAttendance) / targetAttendance))
		} else {
			buffer = -int(math.Ceil((neededAttendance - float64(adjustedAttended)) / (1 - targetAttendance)))
		}

		records = append(records, types.AttendanceRecord{
			CourseCode: courseCode,
			CourseName: courseName,
			CourseType: courseType,
			Faculty:    faculty,
			Attended:   adjustedAttended,
			Total:      adjustedTotal,
			Percentage: percentage,
			Buffer:     buffer,
		})
	})

	return records
}

func calculateAttendance(attended, total, classtype int) string {
	// Calculate how many more classes need to be attended to meet 74.01% attendance
	targetAttendance := 0.7401
	neededAttendance := targetAttendance * float64(total)

	// If the current attendance is already below the target
	if float64(attended) < neededAttendance {
		// Calculate the exact number of additional classes required to meet 74.01%
		x := (neededAttendance - float64(attended)) / (1 - targetAttendance)
		x = math.Ceil(x) // Round up to ensure they meet the target after attending whole classes
		if classtype == 1 {
			return fmt.Sprintf("\033[31mAttend %d more lab(s)\033[0m", int(x))
		} else {
			return fmt.Sprintf("\033[31mAttend %d more class(es)\033[0m", int(x))
		}
	} else {
		// If already at or above the target, calculate how many can be missed
		canMiss := int(math.Floor((float64(attended) - neededAttendance) / targetAttendance))
		if classtype == 1 {
			return fmt.Sprintf("\033[32mCan miss %d lab(s)\033[0m", canMiss)
		} else {
			return fmt.Sprintf("\033[32mCan miss %d class(es)\033[0m", canMiss)
		}
	}
}
