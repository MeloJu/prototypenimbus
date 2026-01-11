#!/usr/bin/env python3
# Quick start script for Music Generator Company

import sys
import subprocess
import os

def check_python_version():
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("ERROR: Python 3.8+ required")
        return False
    
    if version.major == 3 and version.minor >= 12:
        print("WARNING: Python 3.12+ may have compatibility issues with ML packages")
        print("Recommended: Python 3.11 for full features")
        print("Current setup will use fallback modes\n")
    
    return True

def check_ollama():
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        if response.status_code == 200:
            models = response.json().get('models', [])
            if any('llama2' in m.get('name', '') for m in models):
                print("✅ Ollama with llama2 detected")
                return True
            else:
                print("⚠️  Ollama running but llama2 not found")
                print("   Run: ollama pull llama2")
                return False
    except:
        pass
    
    print("❌ Ollama not detected")
    print("   Install from: https://ollama.com/download")
    print("   Then run: ollama pull llama2")
    return False

def install_dependencies():
    print("\nInstalling dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed")
        return True
    except:
        print("❌ Failed to install dependencies")
        return False

def start_server():
    print("\n" + "="*60)
    print("Starting Music Generator Company...")
    print("="*60)
    print("\nWeb interface: http://127.0.0.1:5000")
    print("Press CTRL+C to stop\n")
    
    try:
        subprocess.call([sys.executable, "web_app.py"])
    except KeyboardInterrupt:
        print("\n\nServer stopped")

if __name__ == "__main__":
    print("="*60)
    print("Music Generator Company - Setup")
    print("="*60)
    print()
    
    if not check_python_version():
        sys.exit(1)
    
    ollama_ok = check_ollama()
    
    if not os.path.exists("venv") and not os.path.exists("env"):
        print("\nNo virtual environment detected")
        print("Recommended: python -m venv venv")
    
    deps_ok = install_dependencies()
    
    if not deps_ok:
        print("\n❌ Setup failed")
        sys.exit(1)
    
    if not ollama_ok:
        print("\n⚠️  Ollama not ready - system will use fallback mode")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(0)
    
    start_server()
