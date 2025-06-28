
#!/usr/bin/env python3
"""
YouTube Channel Discovery Tool Setup Script
"""

import os
import sys

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version}")

def check_environment_variables():
    """Check if required environment variables are set"""
    required_vars = ['GOOGLE_API_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.environ.get(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n💡 Set these in your .env file or Replit Secrets")
        return False
    
    print("✅ All required environment variables are set")
    return True

def main():
    """Main setup function"""
    print("🚀 YouTube Channel Discovery Tool Setup")
    print("=" * 50)
    
    check_python_version()
    
    if check_environment_variables():
        print("\n✅ Setup complete!")
        print("\n📖 Next steps:")
        print("1. Ensure all dependencies are installed: pip install -r requirements_for_vscode.txt")
        print("2. Run: python main.py")
        print("3. Open http://0.0.0.0:5000 in your browser")
        print("\n🔑 Get YouTube API key from: https://console.cloud.google.com/")
    else:
        print("\n❌ Setup incomplete - fix environment variables and try again")

if __name__ == "__main__":
    main()
