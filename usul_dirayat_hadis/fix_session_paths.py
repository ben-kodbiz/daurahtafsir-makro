#!/usr/bin/env python3
"""
Script to fix CSS and JS paths in all session HTML files
"""

import os
import re

def fix_session_file(file_path):
    """Fix paths in a single session HTML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix CSS path
        content = content.replace('href="../styles.css"', 'href="style.css"')
        
        # Fix theme.js reference
        theme_script = '''    <script>
        function toggleTheme() {
            const html = document.documentElement;
            const currentTheme = html.className;
            if (currentTheme === 'light-theme') {
                html.className = 'dark-theme';
            } else if (currentTheme === 'dark-theme') {
                html.className = 'sepia-theme';
            } else {
                html.className = 'light-theme';
            }
        }
    </script>'''
        
        content = content.replace('    <script src="../theme.js"></script>', theme_script)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        return False

def main():
    """Fix all session HTML files"""
    current_dir = os.getcwd()
    fixed_count = 0
    error_count = 0
    
    print("🔧 Fixing session HTML file paths...")
    
    # Process all session files
    for i in range(1, 121):
        file_path = f"sesi_{i}.html"
        if os.path.exists(file_path):
            if fix_session_file(file_path):
                fixed_count += 1
                if fixed_count % 20 == 0:
                    print(f"   ✅ Fixed {fixed_count} files...")
            else:
                error_count += 1
        else:
            print(f"   ⚠️  File not found: {file_path}")
    
    print(f"\n🎉 Path fixing completed!")
    print(f"   ✅ Fixed: {fixed_count} files")
    if error_count > 0:
        print(f"   ❌ Errors: {error_count} files")
    print(f"   📁 All session files now use local style.css and inline theme toggle")

if __name__ == "__main__":
    main()