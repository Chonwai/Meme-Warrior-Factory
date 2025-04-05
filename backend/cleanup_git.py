#!/usr/bin/env python
import os
import subprocess

def run_command(command):
    """Run a shell command and print output"""
    print(f"Running: {command}")
    try:
        result = subprocess.run(command, shell=True, check=True, 
                               capture_output=True, text=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(f"Command output: {e.stdout}")
        print(f"Command error: {e.stderr}")
        return False

# Files that should be removed from git tracking
files_to_untrack = [
    # Sensitive files
    ".env",
    
    # Generated images
    "meme_images/*.png",
    
    # Python cache files
    "__pycache__",
    "__pycache__/*",
    "**/__pycache__",
    "**/__pycache__/*",
    "*.pyc",
    "**/*.pyc"
]

# Remove files from git index without deleting them
for file_pattern in files_to_untrack:
    run_command(f"git rm -r --cached --ignore-unmatch {file_pattern}")

# Make sure .gitignore is properly configured
print("\nVerifying .gitignore has all necessary entries...")
required_ignores = [
    ".env",
    "__pycache__/",
    "*.py[cod]",
    "meme_images/"
]

with open(".gitignore", "r") as f:
    gitignore_content = f.read()

missing_ignores = []
for ignore in required_ignores:
    if ignore not in gitignore_content:
        missing_ignores.append(ignore)

if missing_ignores:
    print("Adding missing entries to .gitignore:")
    with open(".gitignore", "a") as f:
        for ignore in missing_ignores:
            print(f"  Adding: {ignore}")
            f.write(f"\n{ignore}")
else:
    print("All necessary entries already in .gitignore")

# Commit these changes to .gitignore if needed
print("\nYou should now commit these changes with:")
print('git add .gitignore')
print('git commit -m "Remove sensitive files from tracking and update gitignore"')
print('git push\n')

print("IMPORTANT: Your .env file has been untracked. Make sure to:")
print("1. Keep a backup of your .env file")
print("2. Never commit it again to the repository")
print("3. Share sensitive credentials with team members through secure channels") 