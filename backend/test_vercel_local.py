#!/usr/bin/env python
"""
Script to simulate Vercel's environment locally.
This helps identify potential issues with the app in Vercel's environment
without having to deploy it.
"""
import os
import sys
import subprocess
import tempfile

# Set Vercel environment variables before importing anything
os.environ["VERCEL"] = "1"
os.environ["SKIP_FILE_OPERATIONS"] = "1"

# Import and apply the filesystem patch
import vercel_middleware
vercel_middleware.apply_patch()

# Ensure Python path includes the current directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Print debug info
print("\n=== Testing in simulated Vercel environment ===")
print(f"Python version: {sys.version}")
print(f"Working directory: {os.getcwd()}")
print(f"Python path: {sys.path}")
print(f"Environment variables:")
for key in sorted(os.environ.keys()):
    if key.startswith('VERCEL') or key.startswith('PYTHON') or key.startswith('OPENAI') or key.startswith('BLOB'):
        print(f"  {key}={os.environ.get(key)}")

# Test filesystem access
print("\n=== Testing file system access ===")
try:
    # Try to create a test directory
    test_dir = './test_directory'
    print(f"Attempting to create directory: {test_dir}")
    os.makedirs(test_dir, exist_ok=True)
    print(f"✅ Directory creation was redirected by middleware")
except Exception as e:
    print(f"❌ Error creating directory: {e}")

try:
    # Try to create a file in the test directory
    test_file = os.path.join(test_dir, 'test.txt')
    print(f"Attempting to write to file: {test_file}")
    with open(test_file, 'w') as f:
        f.write("This is a test")
    print(f"✅ File write was redirected by middleware")
except Exception as e:
    print(f"❌ Error writing to file: {e}")

# Try importing the app directly
print("\n=== Testing app import ===")
try:
    from index import handler
    print("✅ Successfully imported handler from index.py")
except Exception as e:
    print(f"❌ Failed to import handler from index.py: {e}")

# Optional: Try to import app.main directly
try:
    from app.main import app as direct_app
    print("✅ Successfully imported app directly from app.main")
except Exception as e:
    print(f"❌ Failed to import app from app.main: {e}")

# Ask if the user wants to run the server
print("\n=== Server Test ===")
start_server = input("Do you want to start the API server for testing? (y/n): ").strip().lower()

if start_server == 'y':
    print("\n=== Starting the app with uvicorn ===")
    print("The app will start on http://localhost:8000")
    print("Press Ctrl+C to stop")
    print("Check these endpoints:")
    print("- http://localhost:8000/minimal-test")
    print("- http://localhost:8000/env-info")
    print("- http://localhost:8000/meme/test")
    print("=============================================\n")

    try:
        # Run uvicorn
        subprocess.run(["uvicorn", "index:handler", "--reload"])
    except KeyboardInterrupt:
        print("\nStopped by user")
    except Exception as e:
        print(f"\nError running uvicorn: {e}")
else:
    print("\nSkipping server test")

# Clean up the middleware patch
vercel_middleware.remove_patch()
print("\n=== Test completed ===") 