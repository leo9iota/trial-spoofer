#!/usr/bin/env python3
"""
Quick launcher for the comprehensive input demo.
"""

import subprocess
import sys
from pathlib import Path


def main():
    """Run the input demo."""
    demo_path = Path("src/demos/prompt_demo.py")
    
    if not demo_path.exists():
        print("❌ Demo file not found!")
        print(f"Expected: {demo_path.absolute()}")
        sys.exit(1)
    
    print("🚀 Starting comprehensive input demo...")
    print("This demo shows all Rich prompts and Textual input widgets!")
    print()
    
    try:
        subprocess.run([sys.executable, str(demo_path)], check=True)
    except KeyboardInterrupt:
        print("\n👋 Demo interrupted by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Demo failed with exit code {e.returncode}")
        sys.exit(1)


if __name__ == "__main__":
    main()
