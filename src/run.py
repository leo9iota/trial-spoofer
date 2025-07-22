#!/usr/bin/env python3
"""
Alternative entry point for direct execution.
This handles import issues when running directly.
"""

import os
import sys

# Add src directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import main

if __name__ == "__main__":
    main()