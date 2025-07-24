#!/usr/bin/env python3
"""
Setup script for Summer School Chatbot
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

def print_step(step, message):
    """Print a formatted step message."""
    print(f"\n{'='*50}")
    print(f"STEP {step}: {message}")
    print('='*50)

def check_python_version():
    """Check if Python version is 3.8 or higher."""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required.")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version}")

def create_virtual_environment():
    """Create a virtual environment."""
    venv_path = Path("venv")
    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return
    
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ Virtual environment created successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to create virtual environment")
        sys.exit(1)

def install_dependencies():
    """Install project dependencies."""
    venv_python = "venv/bin/python" if os.name != 'nt' else "venv\\Scripts\\python.exe"
    venv_pip = "venv/bin/pip" if os.name != 'nt' else "venv\\Scripts\\pip.exe"
    
    try:
        # Upgrade pip
        subprocess.run([venv_python, "-m", "pip", "install", "--upgrade", "pip"], check=True)
        
        # Install requirements
        subprocess.run([venv_pip, "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        sys.exit(1)

def setup_configuration():
    """Set up configuration files."""
    config_dir = Path("config")
    config_dir.mkdir(exist_ok=True)
    
    # Copy config template if it doesn't exist
    config_file = config_dir / "config.env"
    config_example = config_dir / "config.env.example"
    
    if not config_file.exists() and config_example.exists():
        shutil.copy(config_example, config_file)
        print("✅ Configuration file created from template")
        print(f"📝 Please edit {config_file} to add your API keys")
    else:
        print("ℹ️ Configuration file already exists or template not found")
    
    # Check for credentials file
    creds_file = config_dir / "google_drive_credentials.json"
    creds_example = config_dir / "google_drive_credentials.json.example"
    
    if not creds_file.exists():
        print("📝 Please add your Google Drive credentials to:")
        print(f"   {creds_file}")
        if creds_example.exists():
            print(f"   Use {creds_example} as a template")

def create_directories():
    """Create necessary directories."""
    directories = ["data", "logs", "docs", "tests"]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Directory '{directory}' ready")

def main():
    """Main setup function."""
    print("🚀 Summer School Chatbot Setup")
    print("This script will help you set up the chatbot environment")
    
    print_step(1, "Checking Python version")
    check_python_version()
    
    print_step(2, "Creating virtual environment")
    create_virtual_environment()
    
    print_step(3, "Installing dependencies")
    install_dependencies()
    
    print_step(4, "Setting up configuration")
    setup_configuration()
    
    print_step(5, "Creating directories")
    create_directories()
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Edit config/config.env with your API keys")
    print("2. Add your Google Drive credentials to config/google_drive_credentials.json")
    print("3. Activate the virtual environment:")
    if os.name != 'nt':
        print("   source venv/bin/activate")
    else:
        print("   venv\\Scripts\\activate")
    print("4. Run the chatbot:")
    print("   cd src && python cli_interface.py")
    
    print("\n📚 For more information, see README.md")

if __name__ == "__main__":
    main() 