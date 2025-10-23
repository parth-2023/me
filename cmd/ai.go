package cmd

import (
	"cli-top/features"
	"cli-top/helpers"
	types "cli-top/types"
	"encoding/json"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"strconv"
	"time"

	"github.com/spf13/cobra"
)

var (
	aiOutputPath  string
	aiCompactJSON bool
	aiPythonBin   = "python3"
)

var aiCmd = &cobra.Command{
	Use:   "ai",
	Short: "AI assistant utilities",
	Long:  "Utilities for exporting data and invoking the Python-based AI assistant.",
}

var aiExportCmd = &cobra.Command{
	Use:   "export",
	Short: "Export a consolidated JSON snapshot for AI tooling",
	Run: func(cmd *cobra.Command, args []string) {
		data, err := collectAIData()
		if err != nil {
			fmt.Printf("Failed to build AI dataset: %v\n", err)
			return
		}

		var payload []byte
		if aiCompactJSON {
			payload, err = json.Marshal(data)
		} else {
			payload, err = json.MarshalIndent(data, "", "  ")
		}
		if err != nil {
			fmt.Printf("Failed to encode AI dataset: %v\n", err)
			return
		}

		if aiOutputPath == "-" {
			fmt.Println(string(payload))
			return
		}

		targetPath := aiOutputPath
		if targetPath == "" {
			dir, err := helpers.GetOrCreateDownloadDir(filepath.Join("Other Downloads", "AI"))
			if err != nil {
				fmt.Printf("Failed to prepare AI export directory: %v\n", err)
				return
			}
			targetPath = filepath.Join(dir, fmt.Sprintf("ai-data-%s.json", time.Now().Format("20060102-150405")))
		} else {
			if err := os.MkdirAll(filepath.Dir(targetPath), os.ModePerm); err != nil {
				fmt.Printf("Failed to create output directory: %v\n", err)
				return
			}
		}

		if err := os.WriteFile(targetPath, payload, 0o600); err != nil {
			fmt.Printf("Failed to write AI dataset: %v\n", err)
			return
		}

		fmt.Printf("AI dataset exported to %s\n", targetPath)
	},
}

var aiGradeCmd = &cobra.Command{
	Use:   "grade",
	Short: "Predict grades and CGPA impact",
}

var aiGradePredictCmd = &cobra.Command{
	Use:   "predict",
	Short: "Predict grade using an assumed FAT score",
	Run: func(cmd *cobra.Command, args []string) {
		course, _ := cmd.Flags().GetString("course")
		fat, _ := cmd.Flags().GetFloat64("fat")
		if course == "" {
			fmt.Println("--course is required")
			return
		}
		subArgs := []string{"grade", "predict", "--course", course, "--fat", fmt.Sprintf("%.2f", fat)}
		if err := executePythonWithDataset(subArgs...); err != nil {
			fmt.Printf("Prediction failed: %v\n", err)
		}
	},
}

var aiGradeTargetCmd = &cobra.Command{
	Use:   "target",
	Short: "Calculate required FAT score for a target grade",
	Run: func(cmd *cobra.Command, args []string) {
		course, _ := cmd.Flags().GetString("course")
		grade, _ := cmd.Flags().GetString("grade")
		if course == "" || grade == "" {
			fmt.Println("--course and --grade are required")
			return
		}
		subArgs := []string{"grade", "target", "--course", course, "--grade", grade}
		if err := executePythonWithDataset(subArgs...); err != nil {
			fmt.Printf("Target calculation failed: %v\n", err)
		}
	},
}

var aiGradeCompareCmd = &cobra.Command{
	Use:   "compare",
	Short: "Compare FAT score scenarios",
	Run: func(cmd *cobra.Command, args []string) {
		course, _ := cmd.Flags().GetString("course")
		if course == "" {
			fmt.Println("--course is required")
			return
		}
		subArgs := []string{"grade", "compare", "--course", course}
		if err := executePythonWithDataset(subArgs...); err != nil {
			fmt.Printf("Scenario comparison failed: %v\n", err)
		}
	},
}

var aiGradeCGPACmd = &cobra.Command{
	Use:   "cgpa",
	Short: "Analyse CGPA impact",
	Run: func(cmd *cobra.Command, args []string) {
		if err := executePythonWithDataset("grade", "cgpa"); err != nil {
			fmt.Printf("CGPA analysis failed: %v\n", err)
		}
	},
}

var aiPlanCmd = &cobra.Command{
	Use:   "plan",
	Short: "Generate a study plan",
	Run: func(cmd *cobra.Command, args []string) {
		days, _ := cmd.Flags().GetInt("days")
		courses, _ := cmd.Flags().GetString("courses")
		subArgs := []string{"plan", "--days", strconv.Itoa(days)}
		if courses != "" {
			subArgs = append(subArgs, "--courses", courses)
		}
		if err := executePythonWithDataset(subArgs...); err != nil {
			fmt.Printf("Study planner failed: %v\n", err)
		}
	},
}

var aiAttendanceCmd = &cobra.Command{
	Use:   "attendance",
	Short: "Get attendance recommendations",
	Run: func(cmd *cobra.Command, args []string) {
		question, _ := cmd.Flags().GetString("question")
		course, _ := cmd.Flags().GetString("course")
		subArgs := []string{"attendance"}
		if question != "" {
			subArgs = append(subArgs, "--question", question)
		}
		if course != "" {
			subArgs = append(subArgs, "--course", course)
		}
		if err := executePythonWithDataset(subArgs...); err != nil {
			fmt.Printf("Attendance advisor failed: %v\n", err)
		}
	},
}

var aiTrendCmd = &cobra.Command{
	Use:   "trend",
	Short: "Analyse academic trends",
	Run: func(cmd *cobra.Command, args []string) {
		question, _ := cmd.Flags().GetString("question")
		fullReport, _ := cmd.Flags().GetBool("full-report")
		subArgs := []string{"trend"}
		if question != "" {
			subArgs = append(subArgs, "--question", question)
		}
		if fullReport {
			subArgs = append(subArgs, "--full-report")
		}
		if err := executePythonWithDataset(subArgs...); err != nil {
			fmt.Printf("Trend analysis failed: %v\n", err)
		}
	},
}

var aiRunAllCmd = &cobra.Command{
	Use:   "run-all",
	Short: "Run all non-API AI features (offline)",
	Long: `Execute all algorithmic AI features without requiring API keys:
1. Attendance Buffer Calculator
2. Grade Predictor (for courses with missing FAT)
3. CGPA Impact Analyzer
4. Attendance Recovery Planner (for courses < 75%)
5. Exam Readiness Scorer

All features work completely offline with fresh VTOP data.`,
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("🔄 Fetching fresh data from VTOP...")
		fmt.Println()

		// Collect fresh AI data from VTOP
		data, err := collectAIData()
		if err != nil {
			fmt.Printf("❌ Failed to fetch VTOP data: %v\n", err)
			return
		}

		fmt.Printf("✅ Data fetched successfully\n")
		fmt.Printf("   Student: %s\n", data.RegNo)
		fmt.Printf("   Semester: %s\n", data.Semester)
		fmt.Printf("   CGPA: %.2f\n", data.CGPA)
		fmt.Printf("   Courses: %d\n", len(data.Marks))
		fmt.Println()

		// Save to temporary file
		var payload []byte
		payload, err = json.MarshalIndent(data, "", "  ")
		if err != nil {
			fmt.Printf("❌ Failed to encode data: %v\n", err)
			return
		}

		tmpFile, err := os.CreateTemp("", "cli-top-vtop-*.json")
		if err != nil {
			fmt.Printf("❌ Failed to create temp file: %v\n", err)
			return
		}
		defer os.Remove(tmpFile.Name())

		if _, err := tmpFile.Write(payload); err != nil {
			tmpFile.Close()
			fmt.Printf("❌ Failed to write data: %v\n", err)
			return
		}
		tmpFile.Close()

		// Execute Python script
		aiDir := resolveAIFeaturesDir()
		scriptPath := filepath.Join(aiDir, "run_all_features.py")

		if _, err := os.Stat(scriptPath); os.IsNotExist(err) {
			fmt.Printf("❌ AI features script not found at: %s\n", scriptPath)
			fmt.Println("   Please ensure run_all_features.py exists in the ai directory")
			return
		}

		pythonCmd := exec.Command(aiPythonBin, scriptPath, tmpFile.Name())
		pythonCmd.Stdout = os.Stdout
		pythonCmd.Stderr = os.Stderr
		pythonCmd.Dir = aiDir

		fmt.Println("🚀 Running AI features analysis...\n")
		if err := pythonCmd.Run(); err != nil {
			fmt.Printf("\n❌ Analysis failed: %v\n", err)
			return
		}
	},
}

var aiChatbotCmd = &cobra.Command{
	Use:   "chatbot",
	Short: "Interactive AI chatbot with VTOP context",
	Long: `Start an interactive chat session with Gemini AI that has full access to your VTOP data.
Ask questions about your performance, get study advice, career guidance, and more.

Requires: Gemini API key configured in ai/.env`,
	Run: func(cmd *cobra.Command, args []string) {
		fetch, _ := cmd.Flags().GetBool("fetch")
		question, _ := cmd.Flags().GetString("question")
		
		aiDir := resolveAIFeaturesDir()
		scriptPath := filepath.Join(aiDir, "chatbot.py")

		if _, err := os.Stat(scriptPath); os.IsNotExist(err) {
			fmt.Printf("❌ Chatbot script not found at: %s\n", scriptPath)
			return
		}

		cmdArgs := []string{scriptPath}
		if fetch {
			cmdArgs = append(cmdArgs, "--fetch")
		}
		if question != "" {
			cmdArgs = append(cmdArgs, "--question", question)
		}

		pythonCmd := exec.Command(aiPythonBin, cmdArgs...)
		pythonCmd.Stdout = os.Stdout
		pythonCmd.Stderr = os.Stderr
		pythonCmd.Stdin = os.Stdin
		pythonCmd.Dir = aiDir

		if err := pythonCmd.Run(); err != nil {
			fmt.Printf("❌ Chatbot failed: %v\n", err)
		}
	},
}

var aiCareerCmd = &cobra.Command{
	Use:   "career",
	Short: "Get AI-powered career guidance",
	Long:  `Analyze your academic performance and get personalized career recommendations, skill development plans, and industry insights.`,
	Run: func(cmd *cobra.Command, args []string) {
		executeGeminiFeature("career_advisor.py")
	},
}

var aiStudyPlanCmd = &cobra.Command{
	Use:   "study-plan",
	Short: "Generate optimized study plan",
	Long:  `Create a personalized, time-bound study plan based on your performance, upcoming exams, and available time.`,
	Run: func(cmd *cobra.Command, args []string) {
		days, _ := cmd.Flags().GetInt("days")
		hours, _ := cmd.Flags().GetInt("hours")
		executeGeminiFeatureWithArgs("study_optimizer.py", strconv.Itoa(days), strconv.Itoa(hours))
	},
}

var aiInsightsCmd = &cobra.Command{
	Use:   "insights",
	Short: "Deep performance analysis",
	Long:  `Get comprehensive analysis of your academic performance with strengths, weaknesses, and actionable recommendations.`,
	Run: func(cmd *cobra.Command, args []string) {
		executeGeminiFeature("performance_insights.py")
	},
}

var aiStudyGuideCmd = &cobra.Command{
	Use:   "study-guide",
	Short: "Interactive study guide generator",
	Long:  `Generate comprehensive study guides for your courses with chapter breakdowns, resources, and exam strategies.`,
	Run: func(cmd *cobra.Command, args []string) {
		executeGeminiFeature("study_guide.py")
	},
}

var aiVoiceCmd = &cobra.Command{
	Use:   "voice",
	Short: "Voice-controlled AI assistant (Gemini 2.5 Flash Live)",
	Long: `Start voice-activated assistant that can execute all CLI-TOP features using voice commands.
Powered by Gemini 2.5 Flash Live with speech recognition and text-to-speech.

Features:
- Execute all VTOP features by voice
- Run AI analyses with voice commands
- Use Gemini features hands-free
- Real-time voice interaction
- Display results while speaking

Requires: SpeechRecognition, pyttsx3, PyAudio
Install: pip install SpeechRecognition pyttsx3 pyaudio`,
	Run: func(cmd *cobra.Command, args []string) {
		aiDir := resolveAIFeaturesDir()
		scriptPath := filepath.Join(aiDir, "gemini_features", "voice_assistant.py")

		if _, err := os.Stat(scriptPath); os.IsNotExist(err) {
			fmt.Printf("❌ Voice assistant not found at: %s\n", scriptPath)
			return
		}

		pythonCmd := exec.Command(aiPythonBin, scriptPath)
		pythonCmd.Stdout = os.Stdout
		pythonCmd.Stderr = os.Stderr
		pythonCmd.Stdin = os.Stdin
		pythonCmd.Dir = aiDir

		fmt.Println("🎙️  Starting voice assistant...")
		if err := pythonCmd.Run(); err != nil {
			fmt.Printf("❌ Voice assistant failed: %v\n", err)
		}
	},
}

func collectAIData() (types.VTOPAIData, error) {
	cookies, regNo := readCookiesFromFile()
	data, buildErr := features.BuildAIData(regNo, cookies)
	if buildErr != nil {
		if data.RegNo == "" {
			return data, buildErr
		}
		fmt.Printf("AI dataset built with warnings: %v\n", buildErr)
	}
	return data, nil
}

func prepareDatasetFile(compact bool) (string, func(), error) {
	data, err := collectAIData()
	if err != nil {
		return "", nil, err
	}

	var payload []byte
	if compact {
		payload, err = json.Marshal(data)
	} else {
		payload, err = json.MarshalIndent(data, "", "  ")
	}
	if err != nil {
		return "", nil, err
	}

	tmpFile, err := os.CreateTemp("", "cli-top-ai-*.json")
	if err != nil {
		return "", nil, err
	}

	if _, err := tmpFile.Write(payload); err != nil {
		tmpFile.Close()
		os.Remove(tmpFile.Name())
		return "", nil, err
	}

	if err := tmpFile.Close(); err != nil {
		os.Remove(tmpFile.Name())
		return "", nil, err
	}

	cleanup := func() {
		os.Remove(tmpFile.Name())
	}

	return tmpFile.Name(), cleanup, nil
}

func ensurePythonBinary() error {
	if _, err := exec.LookPath(aiPythonBin); err != nil {
		return fmt.Errorf("python executable %q not found: %w", aiPythonBin, err)
	}
	return nil
}

func resolveAIFeaturesDir() string {
	wd, err := os.Getwd()
	if err != nil {
		return ""
	}
	aiDir := filepath.Join(wd, "ai")
	if info, err := os.Stat(aiDir); err == nil && info.IsDir() {
		return aiDir
	}
	return wd
}

func executeGeminiFeature(scriptName string) {
	data, err := collectAIData()
	if err != nil {
		fmt.Printf("❌ Failed to fetch VTOP data: %v\n", err)
		return
	}

	var payload []byte
	payload, err = json.MarshalIndent(data, "", "  ")
	if err != nil {
		fmt.Printf("❌ Failed to encode data: %v\n", err)
		return
	}

	tmpFile, err := os.CreateTemp("", "cli-top-vtop-*.json")
	if err != nil {
		fmt.Printf("❌ Failed to create temp file: %v\n", err)
		return
	}
	defer os.Remove(tmpFile.Name())

	if _, err := tmpFile.Write(payload); err != nil {
		tmpFile.Close()
		fmt.Printf("❌ Failed to write data: %v\n", err)
		return
	}
	tmpFile.Close()

	aiDir := resolveAIFeaturesDir()
	scriptPath := filepath.Join(aiDir, "gemini_features", scriptName)

	if _, err := os.Stat(scriptPath); os.IsNotExist(err) {
		fmt.Printf("❌ Feature script not found: %s\n", scriptName)
		return
	}

	pythonCmd := exec.Command(aiPythonBin, scriptPath, tmpFile.Name())
	pythonCmd.Stdout = os.Stdout
	pythonCmd.Stderr = os.Stderr
	pythonCmd.Dir = aiDir

	if err := pythonCmd.Run(); err != nil {
		fmt.Printf("❌ Feature failed: %v\n", err)
	}
}

func executeGeminiFeatureWithArgs(scriptName string, extraArgs ...string) {
	data, err := collectAIData()
	if err != nil {
		fmt.Printf("❌ Failed to fetch VTOP data: %v\n", err)
		return
	}

	var payload []byte
	payload, err = json.MarshalIndent(data, "", "  ")
	if err != nil {
		fmt.Printf("❌ Failed to encode data: %v\n", err)
		return
	}

	tmpFile, err := os.CreateTemp("", "cli-top-vtop-*.json")
	if err != nil {
		fmt.Printf("❌ Failed to create temp file: %v\n", err)
		return
	}
	defer os.Remove(tmpFile.Name())

	if _, err := tmpFile.Write(payload); err != nil {
		tmpFile.Close()
		fmt.Printf("❌ Failed to write data: %v\n", err)
		return
	}
	tmpFile.Close()

	aiDir := resolveAIFeaturesDir()
	scriptPath := filepath.Join(aiDir, "gemini_features", scriptName)

	if _, err := os.Stat(scriptPath); os.IsNotExist(err) {
		fmt.Printf("❌ Feature script not found: %s\n", scriptName)
		return
	}

	cmdArgs := append([]string{scriptPath, tmpFile.Name()}, extraArgs...)
	pythonCmd := exec.Command(aiPythonBin, cmdArgs...)
	pythonCmd.Stdout = os.Stdout
	pythonCmd.Stderr = os.Stderr
	pythonCmd.Dir = aiDir

	if err := pythonCmd.Run(); err != nil {
		fmt.Printf("❌ Feature failed: %v\n", err)
	}
}

func executePythonWithDataset(subArgs ...string) error {
	if err := ensurePythonBinary(); err != nil {
		return err
	}

	datasetPath, cleanup, err := prepareDatasetFile(true)
	if err != nil {
		return err
	}
	if cleanup != nil {
		defer cleanup()
	}

	args := append([]string{"-m", "ai_features.main", "--dataset", datasetPath}, subArgs...)
	cmd := exec.Command(aiPythonBin, args...)
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	cmd.Stdin = os.Stdin
	if dir := resolveAIFeaturesDir(); dir != "" {
		cmd.Dir = dir
	}
	return cmd.Run()
}

func init() {
	aiCmd.PersistentFlags().StringVar(&aiPythonBin, "python", aiPythonBin, "Python executable to invoke the AI module")

	aiExportCmd.Flags().StringVarP(&aiOutputPath, "output", "o", "", "Output file path (use '-' for stdout)")
	aiExportCmd.Flags().BoolVar(&aiCompactJSON, "compact", false, "Emit minified JSON instead of pretty-printed output")

	aiChatbotCmd.Flags().Bool("fetch", false, "Fetch fresh VTOP data before starting chat")
	aiChatbotCmd.Flags().StringP("question", "q", "", "Ask a single question (non-interactive)")

	aiStudyPlanCmd.Flags().Int("days", 30, "Number of days until exams")
	aiStudyPlanCmd.Flags().Int("hours", 6, "Available study hours per day")

	aiGradePredictCmd.Flags().String("course", "", "Course code")
	aiGradePredictCmd.Flags().Float64("fat", 80, "Assumed FAT score")
	aiGradeTargetCmd.Flags().String("course", "", "Course code")
	aiGradeTargetCmd.Flags().String("grade", "A", "Target grade (S/A/B/C/D)")
	aiGradeCompareCmd.Flags().String("course", "", "Course code")

	aiPlanCmd.Flags().Int("days", 7, "Number of days to plan")
	aiPlanCmd.Flags().String("courses", "", "Comma separated list of course codes to focus on")

	aiAttendanceCmd.Flags().String("question", "", "Attendance question to analyse")
	aiAttendanceCmd.Flags().String("course", "", "Course code to inspect")

	aiTrendCmd.Flags().String("question", "", "Question for the trend analyzer")
	aiTrendCmd.Flags().Bool("full-report", false, "Generate the full analytical report")

	aiGradeCmd.AddCommand(aiGradePredictCmd, aiGradeTargetCmd, aiGradeCompareCmd, aiGradeCGPACmd)

	aiCmd.AddCommand(aiExportCmd, aiChatbotCmd, aiCareerCmd, aiStudyPlanCmd, aiInsightsCmd, aiStudyGuideCmd, aiVoiceCmd, aiGradeCmd, aiPlanCmd, aiAttendanceCmd, aiTrendCmd, aiRunAllCmd)
}
