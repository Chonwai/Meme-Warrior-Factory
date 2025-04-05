"""
A middleware to simulate Vercel's read-only filesystem.

To use, import and apply the patch before importing your app:

```python
import vercel_middleware
vercel_middleware.apply_patch()

# Now import your app
from app.main import app
```
"""
import os
import tempfile
import builtins
import shutil

# Store original functions
original_open = builtins.open
original_makedirs = os.makedirs

# Global flag to enable/disable the patch
patch_enabled = False

# Temp directory for redirected writes
vercel_temp_dir = tempfile.mkdtemp(prefix="vercel_sim_")
print(f"Created Vercel simulation temp directory: {vercel_temp_dir}")

def patched_open(file, mode='r', *args, **kwargs):
    """Redirect write operations to temp directory"""
    global patch_enabled
    
    if not patch_enabled:
        return original_open(file, mode, *args, **kwargs)
    
    # Only patch write operations
    if 'w' in mode or 'a' in mode or '+' in mode:
        # Get absolute path
        if not os.path.isabs(file):
            file = os.path.abspath(file)
        
        # If this is in the current working directory or below, redirect to temp
        cwd = os.getcwd()
        if file.startswith(cwd):
            # Calculate path inside temp dir
            rel_path = os.path.relpath(file, cwd)
            temp_path = os.path.join(vercel_temp_dir, rel_path)
            
            # Create parent directories
            os.makedirs(os.path.dirname(temp_path), exist_ok=True)
            
            print(f"Redirecting write to {file} → {temp_path}")
            return original_open(temp_path, mode, *args, **kwargs)
    
    # For read operations or files outside cwd, use the original
    return original_open(file, mode, *args, **kwargs)

def patched_makedirs(name, mode=0o777, exist_ok=False):
    """Redirect directory creation to temp directory"""
    global patch_enabled
    
    if not patch_enabled:
        return original_makedirs(name, mode, exist_ok)
    
    # Get absolute path
    if not os.path.isabs(name):
        name = os.path.abspath(name)
    
    # If this is in the current working directory or below, redirect to temp
    cwd = os.getcwd()
    if name.startswith(cwd):
        # Calculate path inside temp dir
        rel_path = os.path.relpath(name, cwd)
        temp_path = os.path.join(vercel_temp_dir, rel_path)
        
        print(f"Redirecting makedirs {name} → {temp_path}")
        return original_makedirs(temp_path, mode, exist_ok)
    
    # For directories outside cwd, use the original
    return original_makedirs(name, mode, exist_ok)

def apply_patch():
    """Apply the patch to simulate Vercel's filesystem"""
    global patch_enabled
    
    # Replace builtins.open with our patched version
    builtins.open = patched_open
    
    # Replace os.makedirs with our patched version
    os.makedirs = patched_makedirs
    
    # Enable the patch
    patch_enabled = True
    
    print("Applied Vercel filesystem simulation patches")

def remove_patch():
    """Remove the patch"""
    global patch_enabled
    
    # Restore original functions
    builtins.open = original_open
    os.makedirs = original_makedirs
    
    # Disable the patch
    patch_enabled = False
    
    # Clean up temp directory
    shutil.rmtree(vercel_temp_dir, ignore_errors=True)
    
    print("Removed Vercel filesystem simulation patches")

# Auto-clean on exit
import atexit
atexit.register(remove_patch) 