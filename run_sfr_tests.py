#!/usr/bin/env python3
"""
SFR Test Runner - Executes tests following Software Functional Requirements patterns.

This script runs the comprehensive test suite that validates all SFR test cases:
- SFR1: QR Code Detection
- SFR2: Field Mapping  
- SFR4: Scan JSON Building
- SFR5: Keystroke Sequence Generation
- SFR11: Event Persistence
- SFR12: JSON Schema Validation
- SFR15: Multi-Code Detection
- SFR16: Output Deduplication
- SFR17: Simulation Injection
- SFR18: Simulation Keystroke Flow
- PPSR2: Performance Latency
- PPSR5: Accuracy Metrics
- PDSR1: Config Inspection
- PDSR2: API Analysis
- QDSR1: Dependency Audit
- EISR3: Interoperability Schema
- EISR5: MES Integration
- EISR6: Configurable Workflows
"""

import subprocess
import sys
from pathlib import Path


def run_sfr_tests():
    """Run comprehensive SFR compliance tests."""
    print("=" * 60)
    print("AIBI Computer Vision - SFR Test Suite")
    print("=" * 60)
    
    # Change to project root
    project_root = Path(__file__).parent
    
    # Run unit requirement tests
    print("\n🧪 Running Unit Requirement Tests...")
    unit_result = subprocess.run([
        sys.executable, "-m", "pytest", 
        "tests/test_unit_requirements.py",
        "-v",
        "--tb=short",
        "--color=yes"
    ], cwd=project_root)
    
    # Run comprehensive tests
    print("\n🧪 Running SFR Compliance Tests...")
    comp_result = subprocess.run([
        sys.executable, "-m", "pytest", 
        "tests/test_comprehensive.py",
        "-v",
        "--tb=short",
        "--color=yes"
    ], cwd=project_root)
    
    overall_result = max(unit_result.returncode, comp_result.returncode)
    
    if overall_result == 0:
        print("\n✅ All SFR tests passed!")
    else:
        print("\n❌ Some SFR tests failed!")
        
    return overall_result


def run_basic_tests():
    """Run basic functionality tests."""
    print("\n🔧 Running Basic Functionality Tests...")
    result = subprocess.run([
        sys.executable, "-m", "pytest", 
        "tests/",
        "--ignore=tests/test_comprehensive.py",
        "--ignore=tests/test_unit_requirements.py",
        "-v",
        "--tb=short",
        "--color=yes"
    ])
    
    return result.returncode


def run_coverage_report():
    """Run tests with coverage reporting."""
    print("\n📊 Running Tests with Coverage...")
    result = subprocess.run([
        sys.executable, "-m", "pytest", 
        "tests/",
        "--cov=src/aibi_cv",
        "--cov-report=term-missing",
        "--cov-report=html:htmlcov",
        "-v"
    ])
    
    if result.returncode == 0:
        print("\n📈 Coverage report generated in htmlcov/")
    
    return result.returncode


def main():
    """Main test runner."""
    if len(sys.argv) > 1:
        if sys.argv[1] == "--sfr-only":
            return run_sfr_tests()
        elif sys.argv[1] == "--basic-only":
            return run_basic_tests()
        elif sys.argv[1] == "--coverage":
            return run_coverage_report()
        elif sys.argv[1] == "--help":
            print(__doc__)
            print("\nUsage:")
            print("  python run_sfr_tests.py           # Run all tests")
            print("  python run_sfr_tests.py --sfr-only     # Run SFR compliance tests only")
            print("  python run_sfr_tests.py --basic-only   # Run basic tests only")
            print("  python run_sfr_tests.py --coverage     # Run with coverage report")
            print("  python run_sfr_tests.py --help         # Show this help")
            return 0
    
    # Run all tests by default
    print("Running complete test suite...")
    
    sfr_result = run_sfr_tests()
    basic_result = run_basic_tests()
    
    if sfr_result == 0 and basic_result == 0:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print("\n💥 Some tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())