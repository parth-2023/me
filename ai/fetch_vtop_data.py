#!/usr/bin/env python3
"""
VTOP Data Fetcher
Automatically fetches all VTOP data using cli-top binary before running AI features
"""

import subprocess
import json
import sys
import os
from pathlib import Path
from datetime import datetime

def get_cli_top_path():
    """Get the path to cli-top binary"""
    # Try current directory first
    cli_path = Path(__file__).parent.parent / 'cli-top'
    if cli_path.exists():
        return str(cli_path)
    
    # Try looking in PATH
    result = subprocess.run(['which', 'cli-top'], capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout.strip()
    
    print("❌ Error: cli-top binary not found")
    print("   Please build it first: go build -o cli-top main.go")
    sys.exit(1)

def fetch_vtop_data(output_file=None):
    """
    Fetch all VTOP data using cli-top export command
    
    Args:
        output_file: Path to save the data (optional)
    
    Returns:
        dict: VTOP data dictionary
    """
    cli_top = get_cli_top_path()
    
    print("🔄 Fetching fresh VTOP data...")
    print()
    
    # Use cli-top's ai export command
    if output_file:
        cmd = [cli_top, 'ai', 'export', '-o', output_file]
    else:
        # Export to stdout
        cmd = [cli_top, 'ai', 'export', '-o', '-']
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60,
            cwd=str(Path(cli_top).parent)
        )
        
        if result.returncode != 0:
            print(f"❌ Failed to fetch VTOP data")
            print(f"   Error: {result.stderr}")
            sys.exit(1)
        
        # Parse the JSON output
        if output_file:
            with open(output_file, 'r') as f:
                data = json.load(f)
            print(f"✅ VTOP data saved to: {output_file}")
        else:
            data = json.loads(result.stdout)
            print("✅ VTOP data fetched successfully")
        
        # Display summary
        print()
        print(f"📊 Data Summary:")
        print(f"   Student: {data.get('reg_no', 'N/A')}")
        print(f"   Semester: {data.get('semester', 'N/A')}")
        print(f"   CGPA: {data.get('cgpa', 'N/A')}")
        print(f"   Courses: {len(data.get('marks', []))}")
        print(f"   Attendance Records: {len(data.get('attendance', []))}")
        print(f"   Upcoming Exams: {len(data.get('exams', []))}")
        print(f"   Assignments: {len(data.get('assignments', []))}")
        print()
        
        return data
    
    except subprocess.TimeoutExpired:
        print("❌ Timeout: VTOP took too long to respond")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse VTOP data: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        output_file = sys.argv[1]
    else:
        # Generate default output filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f"vtop_data_{timestamp}.json"
    
    print("=" * 60)
    print("📡 VTOP Data Fetcher")
    print("=" * 60)
    print()
    
    data = fetch_vtop_data(output_file)
    
    print("=" * 60)
    print("✅ Data fetch complete!")
    print("=" * 60)
    print()
    print(f"You can now run AI features with this data:")
    print(f"  python ai/run_all_features.py {output_file}")
    print(f"  python ai/chatbot.py --data {output_file}")
    print()

if __name__ == '__main__':
    main()
