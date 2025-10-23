#!/usr/bin/env python3
"""
CLI-TOP AI Chatbot
Interactive chatbot powered by Gemini with full VTOP context
"""

import json
import sys
import os
import argparse
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    import google.generativeai as genai
    from config import GOOGLE_API_KEY, GEMINI_MODEL
except ImportError:
    print("❌ Error: Required packages not installed")
    print("   Run: pip install -r ai/requirements.txt")
    sys.exit(1)

class VTOPChatbot:
    """AI Chatbot with VTOP context"""
    
    def __init__(self, vtop_data):
        """Initialize chatbot with VTOP data"""
        self.vtop_data = vtop_data
        self.conversation_history = []
        
        # Configure Gemini
        if not GOOGLE_API_KEY:
            print("❌ Error: GOOGLE_API_KEY not configured")
            print("   Please set it in ai/config.py or environment variable")
            sys.exit(1)
        
        genai.configure(api_key=GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(GEMINI_MODEL)
        
        # Build context
        self.context = self._build_context()
    
    def _build_context(self):
        """Build comprehensive context from VTOP data"""
        context = f"""
You are an AI academic assistant for VIT students. You have access to the student's complete VTOP data.

STUDENT INFORMATION:
- Registration Number: {self.vtop_data.get('reg_no', 'N/A')}
- Current Semester: {self.vtop_data.get('semester', 'N/A')}
- CGPA: {self.vtop_data.get('cgpa', 'N/A')}

COURSES AND MARKS:
"""
        # Add course details
        for course in self.vtop_data.get('marks', []):
            context += f"\n{course.get('course_code', 'N/A')} - {course.get('course_name', 'N/A')}:\n"
            context += f"  Credits: {course.get('credits', 'N/A')}\n"
            context += f"  CAT1: {course.get('cat1', 'N/A')}\n"
            context += f"  CAT2: {course.get('cat2', 'N/A')}\n"
            context += f"  Quiz: {course.get('quiz', 'N/A')}\n"
            context += f"  Assignment: {course.get('assignment', 'N/A')}\n"
            context += f"  FAT: {course.get('fat', 'N/A')}\n"
            context += f"  Total: {course.get('total', 'N/A')}\n"
        
        context += "\nATTENDANCE:\n"
        for att in self.vtop_data.get('attendance', []):
            context += f"{att.get('course_code', 'N/A')}: {att.get('attendance_percentage', 'N/A')}% "
            context += f"({att.get('attended', 0)}/{att.get('total_classes', 0)} classes)\n"
        
        context += "\nUPCOMING EXAMS:\n"
        for exam in self.vtop_data.get('exams', []):
            context += f"{exam.get('course_code', 'N/A')} - {exam.get('exam_type', 'N/A')}: "
            context += f"{exam.get('date', 'N/A')} at {exam.get('time', 'N/A')}\n"
        
        context += "\nPENDING ASSIGNMENTS:\n"
        for assignment in self.vtop_data.get('assignments', []):
            context += f"{assignment.get('course_code', 'N/A')}: {assignment.get('title', 'N/A')} "
            context += f"(Due: {assignment.get('due_date', 'N/A')})\n"
        
        context += """
Your role is to:
1. Answer questions about the student's academic performance
2. Provide study suggestions and time management advice
3. Help with attendance planning and grade predictions
4. Analyze trends and identify areas for improvement
5. Motivate and guide the student towards better performance
6. Provide career guidance based on academic performance

Be friendly, encouraging, and data-driven in your responses.
Use the specific data provided above to give personalized advice.
"""
        return context
    
    def chat(self, user_message):
        """Process user message and generate response"""
        # Add user message to history
        self.conversation_history.append({
            'role': 'user',
            'content': user_message
        })
        
        # Build full prompt with context and history
        full_prompt = self.context + "\n\nCONVERSATION HISTORY:\n"
        for msg in self.conversation_history[-5:]:  # Last 5 messages for context
            full_prompt += f"{msg['role'].upper()}: {msg['content']}\n"
        
        try:
            # Generate response
            response = self.model.generate_content(full_prompt)
            assistant_message = response.text
            
            # Add to history
            self.conversation_history.append({
                'role': 'assistant',
                'content': assistant_message
            })
            
            return assistant_message
        
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def interactive_chat(self):
        """Start interactive chat session"""
        print("=" * 60)
        print("🤖 CLI-TOP AI Chatbot")
        print("=" * 60)
        print()
        print(f"Student: {self.vtop_data.get('reg_no', 'N/A')}")
        print(f"Semester: {self.vtop_data.get('semester', 'N/A')}")
        print(f"CGPA: {self.vtop_data.get('cgpa', 'N/A')}")
        print()
        print("I have your complete VTOP data. Ask me anything!")
        print("Type 'quit', 'exit', or 'bye' to end the conversation")
        print("=" * 60)
        print()
        
        while True:
            try:
                # Get user input
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                # Check for exit commands
                if user_input.lower() in ['quit', 'exit', 'bye', 'q']:
                    print()
                    print("👋 Goodbye! Good luck with your studies!")
                    break
                
                # Get and display response
                print()
                print("🤖 Assistant:", end=" ")
                response = self.chat(user_input)
                print(response)
                print()
            
            except KeyboardInterrupt:
                print("\n\n👋 Chat interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}\n")
    
    def quick_question(self, question):
        """Answer a single question without interactive mode"""
        response = self.chat(question)
        print("=" * 60)
        print("🤖 CLI-TOP AI Assistant")
        print("=" * 60)
        print()
        print(f"Question: {question}")
        print()
        print(f"Answer:")
        print(response)
        print()

def load_vtop_data(file_path):
    """Load VTOP data from JSON file"""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: File not found: {file_path}")
        print("   Run: python ai/fetch_vtop_data.py")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON: {e}")
        sys.exit(1)

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='CLI-TOP AI Chatbot')
    parser.add_argument('--data', type=str, help='Path to VTOP data JSON file')
    parser.add_argument('--fetch', action='store_true', help='Fetch fresh VTOP data first')
    parser.add_argument('--question', '-q', type=str, help='Ask a single question (non-interactive)')
    
    args = parser.parse_args()
    
    # Fetch data if requested
    if args.fetch:
        print("Fetching fresh VTOP data...")
        from fetch_vtop_data import fetch_vtop_data
        import tempfile
        
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        temp_file.close()
        vtop_data = fetch_vtop_data(temp_file.name)
        data_path = temp_file.name
    elif args.data:
        data_path = args.data
        vtop_data = load_vtop_data(data_path)
    else:
        # Try to find latest data file
        data_files = sorted(Path('.').glob('vtop_data_*.json'), reverse=True)
        if data_files:
            data_path = str(data_files[0])
            print(f"Using latest data file: {data_path}")
            vtop_data = load_vtop_data(data_path)
        else:
            print("❌ Error: No VTOP data found")
            print()
            print("Please provide data using one of these methods:")
            print("  1. Fetch fresh data: python ai/chatbot.py --fetch")
            print("  2. Use existing file: python ai/chatbot.py --data vtop_data.json")
            print("  3. Generate data first: python ai/fetch_vtop_data.py")
            sys.exit(1)
    
    # Initialize chatbot
    chatbot = VTOPChatbot(vtop_data)
    
    # Handle single question or interactive mode
    if args.question:
        chatbot.quick_question(args.question)
    else:
        chatbot.interactive_chat()

if __name__ == '__main__':
    main()
