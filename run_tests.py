#!/usr/bin/env python3
"""Test runner script for AIBI CV project."""

import subprocess
import sys
from pathlib import Path


def run_tests():
    """Run all tests with coverage reporting."""
    project_root = Path(__file__).parent
    
    print("Running tests with uv...")
    
    # Run tests with coverage
    result = subprocess.run([
        "uv", "run", "pytest", 
        "--cov=src/aibi_cv",
        "--cov-report=term-missing",
        "tests/"
    ], cwd=project_root)
    
    if result.returncode == 0:
        print("\n✅ All tests passed!")
        print("📊 Coverage report generated in htmlcov/index.html")
    else:
        print("\n❌ Some tests failed")
    
    return result.returncode


if __name__ == "__main__":
    sys.exit(run_tests())