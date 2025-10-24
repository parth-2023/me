#!/usr/bin/env python3
"""Fix Unicode characters in AI features for Windows compatibility."""

import os
import re

# Unicode replacements
replacements = {
    '🚨': 'URGENT:',
    '⚠️': 'WARNING:',
    '📚': 'INFO:',
    '✅': 'OK',
    '❌': 'FAIL',
    'ℹ️': 'INFO:',
    '📊': 'STATS:',
    '🎯': 'TARGET:',
    '📈': 'UP',
    '📉': 'DOWN',
    '➡️': 'SAME',
    '🌟': 'EXCELLENT',
    '📖': 'INFO',
    '🟢': 'GREEN',
    '🟡': 'YELLOW',
    '🔴': 'RED',
    '💻': 'LAB',
    '📐': 'MATH',
    '🎉': 'SUCCESS',
    '💡': 'TIP',
    '📂': 'FOLDER',
    '📘': 'COURSE',
    '≥': '>=',
    '≤': '<=',
    '≠': '!=',
    '±': '+/-',
    '°': 'deg',
    '²': '^2',
    '³': '^3',
    '½': '1/2',
    '¼': '1/4',
    '¾': '3/4',
}

def fix_unicode_in_file(filepath):
    """Fix Unicode characters in a single file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Apply replacements
        original_content = content
        for unicode_char, replacement in replacements.items():
            content = content.replace(unicode_char, replacement)
        
        # Only write if changes were made
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'Fixed {filepath}')
            return True
        else:
            print(f'No changes needed in {filepath}')
            return False
    except Exception as e:
        print(f'Error processing {filepath}: {e}')
        return False

def main():
    """Fix Unicode characters in all AI feature files."""
    features_dir = 'features'
    fixed_count = 0
    
    if not os.path.exists(features_dir):
        print(f'Directory {features_dir} not found')
        return
    
    for filename in os.listdir(features_dir):
        if filename.endswith('.py'):
            filepath = os.path.join(features_dir, filename)
            if fix_unicode_in_file(filepath):
                fixed_count += 1
    
    print(f'\nFixed {fixed_count} files')

if __name__ == '__main__':
    main()
