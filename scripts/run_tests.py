#!/usr/bin/env python3
"""Test runner script."""

import sys
from pathlib import Path


def run_tests():
    """Run the test suite."""
    project_root = Path(__file__).parent.parent
    
    print("🧪 Running test suite...")
    
    # Run pytest with coverage
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/",
        "-v",
        "--tb=short",
        "--cov=src",
        "--cov-report=term-missing",
        "--cov-report=html:htmlcov"
    ]
    
    try:
        import subprocess
        result = subprocess.run(cmd, cwd=project_root, check=False)
        
        if result.returncode == 0:
            print("✅ All tests passed!")
            print("📊 Coverage report generated in htmlcov/")
        else:
            print("❌ Some tests failed!")
            
        return result.returncode
        
    except FileNotFoundError:
        print("❌ pytest not found. Please install test dependencies:")
        print("   uv sync --dev")
        return 1


if __name__ == "__main__":
    sys.exit(run_tests())