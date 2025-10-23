#!/usr/bin/env python3
"""
Better VTOP Backend Server
Flask API to execute CLI-TOP commands and return outputs
Uses stored credentials from cli-top-config.env
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import subprocess
import json
import os
import sys
from pathlib import Path
import tempfile
import re

app = Flask(__name__, static_folder='.')
CORS(app)

# Path to CLI-TOP binary and config
CLI_TOP_PATH = Path(__file__).parent.parent / 'cli-top'
CLI_TOP_CONFIG = Path(__file__).parent.parent / 'cli-top-config.env'

if not CLI_TOP_PATH.exists():
    print(f"⚠️  Warning: CLI-TOP binary not found at {CLI_TOP_PATH}")
    print("   Build it first: go build -o cli-top main.go")

if not CLI_TOP_CONFIG.exists():
    print(f"⚠️  Warning: Config file not found at {CLI_TOP_CONFIG}")
    print("   Run CLI-TOP first to generate credentials")

# Auto-login flag - set to True to use stored credentials
AUTO_LOGIN = True

# Store session credentials temporarily
sessions = {}

@app.route('/')
def index():
    """Serve the main HTML file"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    """Serve static files (CSS, JS)"""
    return send_from_directory('.', path)


@app.route('/api/login', methods=['POST'])
def login():
    """
    Login to VTOP and store credentials
    Request: {"username": "...", "password": "..."}
    """
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400
        
        # Create credentials file
        creds_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        creds_data = {
            'username': username,
            'password': password
        }
        json.dump(creds_data, creds_file)
        creds_file.close()
        
        # Test login with a simple command
        try:
            result = subprocess.run(
                [str(CLI_TOP_PATH), '--creds', creds_file.name, 'profile'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                # Success - store session
                session_id = os.urandom(16).hex()
                sessions[session_id] = creds_file.name
                
                return jsonify({
                    'success': True,
                    'session_id': session_id,
                    'message': 'Login successful!'
                })
            else:
                os.unlink(creds_file.name)
                return jsonify({
                    'error': 'Login failed. Check your credentials.',
                    'details': result.stderr
                }), 401
                
        except subprocess.TimeoutExpired:
            os.unlink(creds_file.name)
            return jsonify({'error': 'Login timeout. VTOP might be slow.'}), 408
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@app.route('/api/logout', methods=['POST'])
def logout():
    """Logout and clear session"""
    data = request.json
    session_id = data.get('session_id')
    
    if session_id in sessions:
        creds_file = sessions[session_id]
        if os.path.exists(creds_file):
            os.unlink(creds_file)
        del sessions[session_id]
    
    return jsonify({'success': True})


@app.route('/api/execute', methods=['POST'])
def execute_command():
    """
    Execute a CLI-TOP command
    Request: {"session_id": "...", "command": "grades view", "args": [...]}
    If AUTO_LOGIN is True, session_id is optional and stored credentials are used
    """
    try:
        data = request.json
        session_id = data.get('session_id')
        command = data.get('command')
        args = data.get('args', [])
        
        # Build command - use stored config if AUTO_LOGIN is enabled
        if AUTO_LOGIN and CLI_TOP_CONFIG.exists():
            # Use the stored credentials from cli-top-config.env
            cmd = [str(CLI_TOP_PATH)]
        else:
            # Use session-based credentials
            if not session_id or session_id not in sessions:
                return jsonify({'error': 'Invalid or expired session'}), 401
            
            creds_file = sessions[session_id]
            cmd = [str(CLI_TOP_PATH), '--creds', creds_file]
        
        # Parse command
        if isinstance(command, str):
            cmd.extend(command.split())
        else:
            cmd.extend(command)
        
        if args:
            cmd.extend(args)
        
        print(f"📡 Executing command: {' '.join(cmd)}")
        
        # Commands that require semester selection
        interactive_commands = ['marks', 'grades', 'attendance', 'da', 'syllabus', 'exams', 'timetable']
        needs_semester = any(ic in cmd for ic in interactive_commands)
        
        # Execute
        if needs_semester:
            # Use echo to automatically select latest semester (option 5)
            result = subprocess.run(
                cmd,
                input="5\n",  # Select latest semester
                capture_output=True,
                text=True,
                timeout=60,
                cwd=str(CLI_TOP_PATH.parent)
            )
        else:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,
                cwd=str(CLI_TOP_PATH.parent)
            )
        
        # Parse output
        output = result.stdout
        error = result.stderr
        
        print(f"Exit code: {result.returncode}")
        print(f"Output length: {len(output)} chars")
        if error:
            print(f"⚠️ Stderr: {error[:200]}")
        
        # Try to detect if output is a table and format it
        formatted_output = format_cli_output(output)
        
        return jsonify({
            'success': result.returncode == 0,
            'output': formatted_output,
            'raw_output': output,
            'error': error if error else None,
            'exit_code': result.returncode
        })
        
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Command timeout (60s)'}), 408
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({'error': f'Execution error: {str(e)}'}), 500


@app.route('/api/ai-export', methods=['POST'])
def ai_export():
    """Export AI data"""
    try:
        data = request.json
        session_id = data.get('session_id')
        
        # Use stored credentials if AUTO_LOGIN is enabled
        if AUTO_LOGIN and CLI_TOP_CONFIG.exists():
            cmd = [str(CLI_TOP_PATH)]
        else:
            if not session_id or session_id not in sessions:
                return jsonify({'error': 'Invalid session'}), 401
            
            creds_file = sessions[session_id]
            cmd = [str(CLI_TOP_PATH), '--creds', creds_file]
        
        # Create temp file for export
        export_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        export_file.close()
        
        # Execute export
        cmd.extend(['ai', 'export', '-o', export_file.name])
        
        print(f"📤 Exporting AI data: {' '.join(cmd)}")
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(CLI_TOP_PATH.parent)
        )
        
        if result.returncode == 0:
            # Read exported data
            with open(export_file.name, 'r') as f:
                ai_data = json.load(f)
            
            os.unlink(export_file.name)
            
            print(f"✅ AI data exported successfully")
            
            return jsonify({
                'success': True,
                'data': ai_data
            })
        else:
            os.unlink(export_file.name)
            print(f"❌ Export failed: {result.stderr}")
            return jsonify({
                'error': 'Export failed',
                'details': result.stderr
            }), 500
            
    except Exception as e:
        print(f"❌ Export error: {str(e)}")
        return jsonify({'error': f'Export error: {str(e)}'}), 500


@app.route('/api/ai-features', methods=['POST'])
def run_ai_features():
    """Run AI features on exported data"""
    try:
        data = request.json
        ai_data = data.get('ai_data')
        feature = data.get('feature', 'all')
        
        if not ai_data:
            return jsonify({'error': 'No AI data provided'}), 400
        
        # Save data to temp file
        data_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        json.dump(ai_data, data_file)
        data_file.close()
        
        # Determine which feature to run
        ai_path = Path(__file__).parent.parent / 'ai'
        
        if feature == 'all':
            script = ai_path / 'run_all_features.py'
            cmd = ['python3', str(script), data_file.name]
        else:
            # Map feature names to script names
            feature_map = {
                'attendance_calculator': 'attendance_calculator.py',
                'grade_predictor': 'grade_predictor.py',
                'cgpa_analyzer': 'cgpa_analyzer.py',
                'attendance_recovery': 'attendance_recovery.py',
                'exam_readiness': 'exam_readiness.py',
                'study_allocator': 'study_allocator.py',
                'performance_analyzer': 'performance_analyzer.py',
                'target_planner': 'target_planner.py',
                'weakness_identifier': 'weakness_identifier.py'
            }
            
            script_name = feature_map.get(feature)
            if not script_name:
                os.unlink(data_file.name)
                return jsonify({'error': f'Unknown feature: {feature}'}), 404
            
            script = ai_path / 'features' / script_name
            cmd = ['python3', str(script), data_file.name]
        
        if not script.exists():
            os.unlink(data_file.name)
            return jsonify({'error': f'Feature not found: {script}'}), 404
        
        # Run feature
        print(f"🤖 Running AI feature: {feature}")
        print(f"Script path: {script}")
        print(f"Data file: {data_file.name}")
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=str(ai_path)
        )
        
        print(f"Exit code: {result.returncode}")
        print(f"Output length: {len(result.stdout)} chars")
        if result.stderr:
            print(f"⚠️ Stderr: {result.stderr[:200]}")
        
        os.unlink(data_file.name)
        
        # Format AI output
        ai_output = result.stdout if result.stdout else result.stderr
        formatted_ai_output = format_cli_output(ai_output) if ai_output else {'type': 'text', 'content': 'No output'}
        
        return jsonify({
            'success': result.returncode == 0,
            'output': formatted_ai_output,
            'raw_output': result.stdout,
            'error': result.stderr if result.stderr else None
        })
        
    except Exception as e:
        return jsonify({'error': f'AI feature error: {str(e)}'}), 500


@app.route('/api/gemini-features', methods=['POST'])
def run_gemini_features():
    """Run Gemini AI features on exported data"""
    try:
        data = request.json
        ai_data = data.get('ai_data')
        feature = data.get('feature', 'chatbot')
        mode = data.get('mode')
        
        if not ai_data:
            return jsonify({'error': 'No AI data provided'}), 400
        
        # Save data to temp file
        data_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        json.dump(ai_data, data_file)
        data_file.close()
        
        # Determine which Gemini feature to run
        gemini_path = Path(__file__).parent.parent / 'ai' / 'gemini_features'
        ai_path = Path(__file__).parent.parent / 'ai'
        
        # Map features to scripts
        feature_map = {
            'chatbot': (ai_path / 'chatbot.py', ['--fetch']),
            'insights': (gemini_path / 'performance_insights.py', []),
            'career': (gemini_path / 'career_advisor.py', []),
            'study-plan': (gemini_path / 'study_plan_generator.py', []),
            'study-guide': (gemini_path / 'study_guide.py', []),
            'voice': (gemini_path / 'voice_assistant.py', [])
        }
        
        if feature not in feature_map:
            os.unlink(data_file.name)
            return jsonify({'error': f'Unknown Gemini feature: {feature}'}), 404
        
        script, extra_args = feature_map[feature]
        
        if not script.exists():
            os.unlink(data_file.name)
            return jsonify({'error': f'Gemini feature not found: {script}'}), 404
        
        # Build command
        cmd = ['python3', str(script), data_file.name] + extra_args
        
        # Run Gemini feature
        print(f"✨ Running Gemini feature: {feature}")
        print(f"Script path: {script}")
        print(f"Data file: {data_file.name}")
        print(f"Command: {' '.join(cmd)}")
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60,  # Gemini might take longer
            cwd=str(gemini_path)
        )
        
        print(f"Exit code: {result.returncode}")
        print(f"Output length: {len(result.stdout)} chars")
        if result.stderr:
            print(f"⚠️ Stderr: {result.stderr[:200]}")
        
        os.unlink(data_file.name)
        
        # Format Gemini output
        gemini_output = result.stdout if result.stdout else result.stderr
        formatted_output = format_cli_output(gemini_output) if gemini_output else {'type': 'text', 'content': 'No output'}
        
        return jsonify({
            'success': result.returncode == 0,
            'output': formatted_output,
            'raw_output': result.stdout,
            'error': result.stderr if result.stderr else None
        })
        
    except subprocess.TimeoutExpired:
        os.unlink(data_file.name)
        return jsonify({'error': 'Gemini feature timeout (60s) - API might be slow'}), 408
    except Exception as e:
        return jsonify({'error': f'Gemini feature error: {str(e)}'}), 500


@app.route('/api/smart-command', methods=['POST'])
def smart_command():
    """Execute smart context-aware multi-tool commands"""
    try:
        data = request.json
        ai_data = data.get('ai_data')
        smart_type = data.get('smart_type')
        
        if not ai_data or not smart_type:
            return jsonify({'error': 'AI data and smart_type required'}), 400
        
        # Save data to temp file
        data_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        json.dump(ai_data, data_file)
        data_file.close()
        
        ai_path = Path(__file__).parent.parent / 'ai'
        output_parts = []
        
        try:
            if smart_type == 'attendance_advice':
                # Run attendance + attendance calculator
                output_parts.append("🔄 Checking Attendance...\n")
                
                # Get attendance from CLI
                cmd = [str(CLI_TOP_PATH), 'attendance', 'calculator']
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    output_parts.append(result.stdout + "\n")
                
                # Run AI attendance calculator
                script = ai_path / 'features' / 'attendance_calculator.py'
                result = subprocess.run(
                    ['python3', str(script), data_file.name],
                    capture_output=True, text=True, timeout=30, cwd=str(ai_path)
                )
                if result.returncode == 0:
                    output_parts.append("\n📊 AI Analysis:\n" + result.stdout)
                
            elif smart_type == 'performance_overview':
                # Run CGPA + performance analyzer + insights
                output_parts.append("🔄 Analyzing Performance...\n")
                
                # Get CGPA
                cmd = [str(CLI_TOP_PATH), 'cgpa', 'view']
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    output_parts.append(result.stdout + "\n")
                
                # Run performance analyzer
                script = ai_path / 'features' / 'performance_analyzer.py'
                result = subprocess.run(
                    ['python3', str(script), data_file.name],
                    capture_output=True, text=True, timeout=30, cwd=str(ai_path)
                )
                if result.returncode == 0:
                    output_parts.append("\n📊 Performance Trends:\n" + result.stdout)
                
            elif smart_type == 'focus_advisor':
                # Run weakness identifier
                output_parts.append("🔄 Identifying Focus Areas...\n")
                
                script = ai_path / 'features' / 'weakness_identifier.py'
                result = subprocess.run(
                    ['python3', str(script), data_file.name],
                    capture_output=True, text=True, timeout=30, cwd=str(ai_path)
                )
                if result.returncode == 0:
                    output_parts.append(result.stdout)
                
            elif smart_type == 'exam_prediction':
                # Run exam readiness + grade predictor
                output_parts.append("🔄 Predicting Exam Performance...\n")
                
                # Exam readiness
                script = ai_path / 'features' / 'exam_readiness.py'
                result = subprocess.run(
                    ['python3', str(script), data_file.name],
                    capture_output=True, text=True, timeout=30, cwd=str(ai_path)
                )
                if result.returncode == 0:
                    output_parts.append(result.stdout + "\n")
                
                # Grade predictor
                script = ai_path / 'features' / 'grade_predictor.py'
                result = subprocess.run(
                    ['python3', str(script), data_file.name],
                    capture_output=True, text=True, timeout=30, cwd=str(ai_path)
                )
                if result.returncode == 0:
                    output_parts.append("\n🎯 Grade Predictions:\n" + result.stdout)
            
            os.unlink(data_file.name)
            
            combined_output = '\n'.join(output_parts)
            
            return jsonify({
                'success': True,
                'output': {'type': 'text', 'content': combined_output},
                'raw_output': combined_output
            })
            
        except Exception as e:
            os.unlink(data_file.name)
            raise e
            
    except Exception as e:
        return jsonify({'error': f'Smart command error: {str(e)}'}), 500


@app.route('/api/chat', methods=['POST'])
def chat():
    """Interactive chat with AI chatbot"""
    try:
        data = request.json
        ai_data = data.get('ai_data')
        message = data.get('message')
        
        if not ai_data or not message:
            return jsonify({'error': 'AI data and message required'}), 400
        
        # Save data to temp file
        data_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        json.dump(ai_data, data_file)
        data_file.close()
        
        # Create temp file for user message
        msg_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
        msg_file.write(message)
        msg_file.close()
        
        # Run chatbot with single question
        ai_path = Path(__file__).parent.parent / 'ai'
        script = ai_path / 'chatbot.py'
        
        if not script.exists():
            os.unlink(data_file.name)
            os.unlink(msg_file.name)
            return jsonify({'error': 'Chatbot not found'}), 404
        
        # Use --question flag for single Q&A
        cmd = ['python3', str(script), '--data', data_file.name, '--question', message]
        
        print(f"💬 Chat query: {message}")
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=str(ai_path)
        )
        
        os.unlink(data_file.name)
        os.unlink(msg_file.name)
        
        # Extract response
        response = result.stdout.strip() if result.stdout else result.stderr.strip()
        
        # Clean up the response (remove prompts, etc.)
        lines = response.split('\n')
        cleaned_lines = []
        skip_next = False
        
        for line in lines:
            # Skip configuration messages
            if '✅ AI Configuration' in line or 'Model:' in line or 'API Key' in line:
                continue
            if 'Output Directory' in line or skip_next:
                skip_next = False
                continue
            # Skip empty lines at start
            if not cleaned_lines and not line.strip():
                continue
            cleaned_lines.append(line)
        
        clean_response = '\n'.join(cleaned_lines).strip()
        
        return jsonify({
            'success': True,
            'response': clean_response,
            'raw': response
        })
        
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Chat timeout - AI is taking too long'}), 408
    except Exception as e:
        return jsonify({'error': f'Chat error: {str(e)}'}), 500


def format_cli_output(output):
    """Format CLI output for better display"""
    # Check if it's a table (contains borders like ├──, │, etc.)
    if '│' in output or '├' in output or '┌' in output:
        return {
            'type': 'table',
            'content': output
        }
    
    # Check if it's JSON
    try:
        json_data = json.loads(output)
        return {
            'type': 'json',
            'content': json_data
        }
    except:
        pass
    
    # Regular text
    return {
        'type': 'text',
        'content': output
    }


if __name__ == '__main__':
    print("="*60)
    print("🚀 Better VTOP Backend Server")
    print("="*60)
    print(f"CLI-TOP Path: {CLI_TOP_PATH}")
    print(f"Exists: {CLI_TOP_PATH.exists()}")
    print()
    print("Server starting on http://localhost:5555")
    print("Open http://localhost:5555 in your browser")
    print("="*60)
    print()
    
    app.run(debug=True, port=5555, host='0.0.0.0')
