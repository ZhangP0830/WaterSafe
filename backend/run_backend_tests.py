#!/usr/bin/env python3
"""
WaterSafe Backend Test Runner

This script provides comprehensive test execution for the WaterSafe backend
with detailed reporting and quality metrics.
"""

import subprocess
import sys
import json
import time
import os
from datetime import datetime
from pathlib import Path

class BackendTestRunner:
    def __init__(self):
        self.test_results = {
            "total": 0,
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "coverage": 0,
            "start_time": None,
            "end_time": None,
            "duration": 0,
            "test_files": [],
            "errors": []
        }
        
        self.test_files = [
            "test_main.py",
            "test_water_quality_prediction.py", 
            "test_guidance_api.py",
            "test_database.py",
            "test_integration.py"
        ]

    def run_tests(self):
        """Run all backend tests with comprehensive reporting"""
        print("WaterSafe Backend Test Suite Execution")
        print("=" * 50)
        
        self.test_results["start_time"] = datetime.now()
        
        try:
            # Check if pytest is available
            self.check_dependencies()
            
            # Run the test suite
            print("Running comprehensive backend test suite...\n")
            
            # Run tests with coverage
            cmd = [
                "python", "-m", "pytest", 
                "tests/",
                "-v",
                "--tb=short",
                "--cov=.",
                "--cov-report=html:htmlcov",
                "--cov-report=term-missing",
                "--cov-report=json:coverage.json",
                "--junitxml=test-results.xml"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=".")
            
            self.parse_test_results(result.stdout, result.stderr)
            self.generate_report()
            
        except Exception as error:
            print(f"❌ Test execution failed: {error}")
            self.test_results["failed"] += 1
            self.test_results["errors"].append(str(error))
            self.generate_error_report(error)
        
        self.test_results["end_time"] = datetime.now()
        self.test_results["duration"] = (self.test_results["end_time"] - self.test_results["start_time"]).total_seconds()
        
        return self.test_results

    def check_dependencies(self):
        """Check if required testing dependencies are available"""
        print("Checking test dependencies...")
        
        try:
            import pytest
            import pytest_asyncio
            import httpx
            import pandas
            import numpy
            print("All dependencies are available\n")
        except ImportError as e:
            raise Exception(f"Missing dependency: {e}")

    def parse_test_results(self, stdout, stderr):
        """Parse test results from pytest output"""
        print("Parsing test results...\n")
        
        lines = stdout.split('\n')
        
        for line in lines:
            if 'passed' in line and 'failed' in line:
                # Extract test counts
                parts = line.split()
                for part in parts:
                    if part.endswith('passed'):
                        self.test_results["passed"] = int(part.split()[0])
                    elif part.endswith('failed'):
                        self.test_results["failed"] = int(part.split()[0])
                    elif part.endswith('skipped'):
                        self.test_results["skipped"] = int(part.split()[0])
        
        self.test_results["total"] = (
            self.test_results["passed"] + 
            self.test_results["failed"] + 
            self.test_results["skipped"]
        )
        
        # Try to read coverage from JSON file
        try:
            if os.path.exists("coverage.json"):
                with open("coverage.json", "r") as f:
                    coverage_data = json.load(f)
                    self.test_results["coverage"] = coverage_data.get("totals", {}).get("percent_covered", 0)
        except Exception:
            self.test_results["coverage"] = 0

    def generate_report(self):
        """Generate comprehensive test report"""
        print("Backend Test Execution Report")
        print("=" * 40)
        
        print(f"Duration: {self.test_results['duration']:.2f} seconds")
        print(f"Total Tests: {self.test_results['total']}")
        print(f"Passed: {self.test_results['passed']}")
        print(f"Failed: {self.test_results['failed']}")
        print(f"Skipped: {self.test_results['skipped']}")
        print(f"Coverage: {self.test_results['coverage']:.1f}%\n")
        
        # Quality Assessment
        self.assess_quality()
        
        # Recommendations
        self.generate_recommendations()
        
        # Save detailed report
        self.save_detailed_report()

    def assess_quality(self):
        """Assess test quality and provide feedback"""
        print("Quality Assessment")
        print("=" * 20)
        
        pass_rate = (self.test_results["passed"] / self.test_results["total"]) * 100 if self.test_results["total"] > 0 else 0
        
        if pass_rate == 100:
            print("EXCELLENT: All tests passed!")
        elif pass_rate >= 90:
            print("GOOD: Most tests passed, minor issues to address")
        elif pass_rate >= 80:
            print("FAIR: Some tests failed, review and fix issues")
        else:
            print("POOR: Many tests failed, significant issues to address")
        
        if self.test_results["coverage"] >= 80:
            print("Coverage: Excellent test coverage")
        elif self.test_results["coverage"] >= 60:
            print("Coverage: Good test coverage, room for improvement")
        else:
            print("Coverage: Low test coverage, needs improvement")
        
        print("")

    def generate_recommendations(self):
        """Generate recommendations based on test results"""
        print("Recommendations")
        print("=" * 15)
        
        if self.test_results["failed"] > 0:
            print("Fix failing tests before deployment")
            print("Review test cases for accuracy and completeness")
        
        if self.test_results["coverage"] < 80:
            print("Increase test coverage to meet quality standards")
            print("Focus on critical business logic and edge cases")
        
        if self.test_results["skipped"] > 0:
            print("Review skipped tests and implement if needed")
        
        print("Run tests regularly during development")
        print("Monitor test metrics and quality trends")
        print("Add integration tests for critical user workflows\n")

    def save_detailed_report(self):
        """Save detailed test report to file"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": self.test_results,
            "test_files": self.test_files,
            "quality": {
                "pass_rate": (self.test_results["passed"] / self.test_results["total"]) * 100 if self.test_results["total"] > 0 else 0,
                "coverage": self.test_results["coverage"],
                "status": "PASS" if self.test_results["failed"] == 0 else "FAIL"
            }
        }
        
        report_path = "backend-test-report.json"
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)
        
        print(f"Detailed report saved to: {report_path}")

    def generate_error_report(self, error):
        """Generate error report for failed test execution"""
        print("Error Report")
        print("=" * 15)
        print(f"Error: {error}")
        print("\nTroubleshooting:")
        print("1. Ensure all dependencies are installed: pip install -r requirements.txt")
        print("2. Install test dependencies: pip install pytest pytest-asyncio httpx pytest-cov")
        print("3. Check Python version compatibility")
        print("4. Verify test file syntax and imports")
        print("5. Run individual test files to isolate issues\n")

    def run_specific_tests(self, test_pattern):
        """Run specific tests matching a pattern"""
        print(f"Running tests matching pattern: {test_pattern}")
        
        cmd = [
            "python", "-m", "pytest", 
            f"tests/{test_pattern}",
            "-v",
            "--tb=short"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=".")
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        return result.returncode == 0

    def run_coverage_only(self):
        """Run tests with coverage report only"""
        print("Running tests with coverage analysis...")
        
        cmd = [
            "python", "-m", "pytest", 
            "tests/",
            "--cov=.",
            "--cov-report=html:htmlcov",
            "--cov-report=term-missing",
            "--quiet"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=".")
        print(result.stdout)
        
        return result.returncode == 0

def main():
    """Main entry point for test runner"""
    runner = BackendTestRunner()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "coverage":
            success = runner.run_coverage_only()
        elif command == "specific":
            if len(sys.argv) > 2:
                pattern = sys.argv[2]
                success = runner.run_specific_tests(pattern)
            else:
                print("Usage: python run_backend_tests.py specific <test_pattern>")
                sys.exit(1)
        else:
            print("Unknown command. Available commands: coverage, specific")
            sys.exit(1)
    else:
        # Run full test suite
        results = runner.run_tests()
        success = results["failed"] == 0
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
