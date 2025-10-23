#!/usr/bin/env python3
"""
CLI-TOP AI Configuration
Central configuration for all AI features and Gemini integration
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
env_path = Path(__file__).parent / '.env'
if env_path.exists():
    load_dotenv(env_path)

# Gemini API Configuration
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', '')

if not GOOGLE_API_KEY:
    print("⚠️  Warning: GOOGLE_API_KEY not set")
    print("   To use AI features, please:")
    print("   1. Get a Gemini API key from: https://makersuite.google.com/app/apikey")
    print("   2. Set it in ai/.env file: GOOGLE_API_KEY=your_key_here")
    print("   3. Or set environment variable: export GOOGLE_API_KEY=your_key_here")
    print()

# Model configuration
GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-2.5-flash')
GEMINI_LIVE_MODEL = os.getenv('GEMINI_LIVE_MODEL', 'gemini-2.5-flash-live')
TEMPERATURE = float(os.getenv('TEMPERATURE', '0.7'))
MAX_TOKENS = int(os.getenv('MAX_TOKENS', '2048'))

# Output configuration
OUTPUT_DIR = Path(__file__).parent / 'outputs'
OUTPUT_DIR.mkdir(exist_ok=True)

# Feature flags
ENABLE_CHATBOT = True
ENABLE_CAREER_ADVISOR = True
ENABLE_STUDY_OPTIMIZER = True
ENABLE_PERFORMANCE_INSIGHTS = True

# Display configuration
if GOOGLE_API_KEY:
    print(f"✅ AI Configuration loaded")
    print(f"   Model: {GEMINI_MODEL}")
    print(f"   API Key: ✓ Set")
    print(f"   Output Directory: {OUTPUT_DIR}")
    print()
