#!/usr/bin/env python3
"""
Setup script for YouTube Channel Discovery Tool
Run this script to set up the project in VS Code
"""

import os
import sys
import subprocess

def setup_project():
    """Set up the YouTube Channel Discovery project"""
    print("🚀 Setting up YouTube Channel Discovery Tool...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version.split()[0]} detected")
    
    # Install dependencies
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements_for_vscode.txt"])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        print("Please run: pip install -r requirements_for_vscode.txt")
        return False
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("\n⚙️  Creating .env file from template...")
        try:
            with open('.env.template', 'r') as template:
                content = template.read()
            with open('.env', 'w') as env_file:
                env_file.write(content)
            print("✅ .env file created")
            print("📝 Please edit .env file and add your GOOGLE_API_KEY")
        except Exception as e:
            print(f"❌ Error creating .env file: {e}")
            return False
    else:
        print("✅ .env file already exists")
    
    print("\n🎉 Setup complete!")
    print("\n📋 Next steps:")
    print("1. Edit .env file and add your YouTube API key")
    print("2. Run: python main.py")
    print("3. Open http://localhost:5000 in your browser")
    print("\n🔑 Get YouTube API key from: https://console.cloud.google.com")
    
    return True

if __name__ == "__main__":
    setup_project()