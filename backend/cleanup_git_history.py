#!/usr/bin/env python
import os
import subprocess
import sys

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

def main():
    print("⚠️ This script will rewrite git history to remove sensitive data ⚠️")
    print("This is a destructive operation and should be used with caution.")
    confirmation = input("Are you sure you want to continue? (yes/no): ")
    
    if confirmation.lower() != "yes":
        print("Operation cancelled.")
        sys.exit(0)
    
    # Step 1: Create a backup (optional but recommended)
    print("\n1. Creating a backup of the repository...")
    if not os.path.exists("../backup"):
        os.makedirs("../backup")
    
    run_command("git bundle create ../backup/repo.bundle --all")
    
    # Step 2: Use git filter-branch to remove .env files from history
    print("\n2. Removing .env files from git history...")
    run_command("""
    git filter-branch --force --index-filter "git rm --cached --ignore-unmatch */.env .env" \
    --prune-empty --tag-name-filter cat -- --all
    """)
    
    # Step 3: Remove cached objects and refs
    print("\n3. Cleaning up...")
    run_command("git for-each-ref --format='delete %(refname)' refs/original | git update-ref --stdin")
    run_command("git reflog expire --expire=now --all")
    run_command("git gc --prune=now")
    
    # Step 4: Instructions for force push
    print("\n✅ History rewriting complete!")
    print("\nTo push these changes to the remote repository, you need to force push:")
    print("\ngit push origin --force --all")
    print("\nWARNING: This will overwrite the remote repository. Make sure all team members are aware of this change.")
    print("They will need to re-clone the repository or use 'git pull --rebase' after this operation.")
    
if __name__ == "__main__":
    main() 