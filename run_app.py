#!/usr/bin/env python3
"""
BD Travel Bot - Streamlit Chat App Runner
=========================================

This script helps you run the BD Travel Bot Streamlit app with proper setup.

Usage:
    python run_app.py

Requirements:
    - All dependencies from requirements.txt must be installed
    - .env file with proper API keys must be configured
"""

import subprocess
import sys
import os
from pathlib import Path


def check_requirements():
    """Check if required packages are installed."""
    try:
        import streamlit
        import langchain
        import langgraph

        print("✅ All required packages are installed!")
        return True
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("Please run: pip install -r requirements.txt")
        return False


def check_env_file():
    """Check if .env file exists."""
    env_file = Path(".env")
    if env_file.exists():
        print("✅ .env file found!")
        return True
    else:
        print("❌ .env file not found!")
        print("Please create a .env file with your API keys:")
        print("GOOGLE_API_KEY=your_google_api_key")
        print("NVIDIA_API_KEY=your_nvidia_api_key")
        print("DB_URI=your_database_uri")
        return False


def run_streamlit():
    """Run the Streamlit app."""
    print("🚀 Starting BD Travel Bot...")
    print("📱 The app will open in your browser at: http://localhost:8501")
    print("🛑 Press Ctrl+C to stop the app")
    print("-" * 50)

    try:
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", "streamlit_app.py"], check=True
        )
    except KeyboardInterrupt:
        print("\n👋 BD Travel Bot stopped!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running Streamlit: {e}")


def main():
    """Main function to run the app."""
    print("🇧🇩 BD Travel Bot - Streamlit Chat App")
    print("=" * 40)

    # Check requirements
    if not check_requirements():
        return

    # Check environment file
    if not check_env_file():
        return

    # Run the app
    run_streamlit()


if __name__ == "__main__":
    main()
