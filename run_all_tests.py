#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Master Test Runner for AndroRAT
Runs all comprehensive tests and generates detailed report
"""

import sys
import os
import unittest
import time
from datetime import datetime

# Add tests directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tests'))

from test_utils import setup_server_path, get_project_root
setup_server_path()

# Import test modules
try:
    from tests.test_android_15_16_upgrade import (
        Android15UpgradeTests, 
        APKIntegrityTests, 
        ComprehensiveUpgradeValidation
    )
    UPGRADE_TESTS_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import upgrade tests: {e}")
    UPGRADE_TESTS_AVAILABLE = False

try:
    from tests.comprehensive_functionality_test import AndroidCompatibilityTests
    FUNCTIONALITY_TESTS_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import functionality tests: {e}")
    FUNCTIONALITY_TESTS_AVAILABLE = False

try:
    from tests.comprehensive_test import ComprehensiveAndroRATTests
    COMPREHENSIVE_TESTS_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import comprehensive tests: {e}")
    COMPREHENSIVE_TESTS_AVAILABLE = False


class TestResultCollector:
    """Collect and format test results"""
    
    def __init__(self):
        self.results = []
        self.start_time = None
        self.end_time = None
        
    def add_suite_result(self, suite_name, result):
        """Add result from a test suite"""
        self.results.append({
            'name': suite_name,
            'total': result.testsRun,
            'passed': result.testsRun - len(result.failures) - len(result.errors),
            'failed': len(result.failures),
            'errors': len(result.errors),
            'success': result.wasSuccessful()
        })
        
    def generate_report(self):
        """Generate comprehensive test report"""
        report = []
        report.append("\n" + "="*80)
        report.append("ANDRORAT COMPREHENSIVE TEST REPORT")
        report.append("="*80)
        report.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if self.start_time and self.end_time:
            duration = self.end_time - self.start_time
            report.append(f"Duration: {duration:.2f} seconds")
        
        report.append("\n" + "-"*80)
        report.append("TEST SUITE RESULTS")
        report.append("-"*80)
        
        total_tests = 0
        total_passed = 0
        total_failed = 0
        total_errors = 0
        all_success = True
        
        for result in self.results:
            status = "✅ PASS" if result['success'] else "❌ FAIL"
            report.append(f"\n{result['name']}: {status}")
            report.append(f"  Total:  {result['total']}")
            report.append(f"  Passed: {result['passed']}")
            report.append(f"  Failed: {result['failed']}")
            report.append(f"  Errors: {result['errors']}")
            
            total_tests += result['total']
            total_passed += result['passed']
            total_failed += result['failed']
            total_errors += result['errors']
            all_success = all_success and result['success']
        
        report.append("\n" + "-"*80)
        report.append("OVERALL SUMMARY")
        report.append("-"*80)
        report.append(f"Total Tests:     {total_tests}")
        report.append(f"Passed:          {total_passed}")
        report.append(f"Failed:          {total_failed}")
        report.append(f"Errors:          {total_errors}")
        report.append(f"Success Rate:    {(total_passed/total_tests*100) if total_tests > 0 else 0:.1f}%")
        
        report.append("\n" + "="*80)
        if all_success:
            report.append("✅ ALL TEST SUITES PASSED - SYSTEM VALIDATED")
        else:
            report.append("❌ SOME TEST SUITES FAILED - REVIEW REQUIRED")
        report.append("="*80 + "\n")
        
        return "\n".join(report)


def run_test_suite(suite_name, test_class):
    """Run a single test suite"""
    print(f"\n{'='*80}")
    print(f"Running: {suite_name}")
    print(f"{'='*80}\n")
    
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(test_class)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


def main():
    """Main test execution"""
    print("\n" + "="*80)
    print("ANDRORAT MASTER TEST RUNNER")
    print("="*80)
    print(f"Python: {sys.version}")
    print(f"Working Directory: {os.getcwd()}")
    print(f"Project Root: {get_project_root()}")
    print("="*80)
    
    collector = TestResultCollector()
    collector.start_time = time.time()
    
    test_suites = []
    
    # Add available test suites
    if UPGRADE_TESTS_AVAILABLE:
        test_suites.extend([
            ("Android 15/16 Upgrade Tests", Android15UpgradeTests),
            ("APK Integrity Tests", APKIntegrityTests),
            ("Comprehensive Upgrade Validation", ComprehensiveUpgradeValidation),
        ])
    
    if FUNCTIONALITY_TESTS_AVAILABLE:
        test_suites.append(("Android Compatibility Tests", AndroidCompatibilityTests))
    
    if COMPREHENSIVE_TESTS_AVAILABLE:
        # Run specific important tests from comprehensive suite
        print(f"\n{'='*80}")
        print("Running: Comprehensive Android Tests (Selected)")
        print(f"{'='*80}\n")
        
        suite = unittest.TestSuite()
        suite.addTest(ComprehensiveAndroRATTests('test_07_android_configuration_validation'))
        suite.addTest(ComprehensiveAndroRATTests('test_08_android_gradle_configuration'))
        
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        collector.add_suite_result("Comprehensive Android Tests (Selected)", result)
    
    # Run all test suites
    for suite_name, test_class in test_suites:
        result = run_test_suite(suite_name, test_class)
        collector.add_suite_result(suite_name, result)
    
    collector.end_time = time.time()
    
    # Generate and print report
    report = collector.generate_report()
    print(report)
    
    # Save report to file
    report_path = os.path.join(get_project_root(), 'TEST_REPORT.txt')
    with open(report_path, 'w') as f:
        f.write(report)
    print(f"Report saved to: {report_path}")
    
    # Exit with appropriate code
    all_passed = all(r['success'] for r in collector.results)
    sys.exit(0 if all_passed else 1)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest execution interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nFatal error during test execution: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
