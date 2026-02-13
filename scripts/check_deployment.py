#!/usr/bin/env python3
"""Verify deployment readiness"""
import sys
import os

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def check():
    files = ['api/main.py', 'frontend/streamlit_app.py', 'requirements.txt', 
             'render.yaml', '.github/workflows/backend.yml', '.github/workflows/frontend.yml']
    
    print("Checking deployment files...")
    all_ok = all(os.path.exists(f) for f in files)
    
    if all_ok:
        print("[OK] All required files present")
        print("\nNext: Follow DEPLOYMENT.md")
        return 0
    else:
        print("[ERROR] Missing files")
        return 1

if __name__ == "__main__":
    sys.exit(check())
