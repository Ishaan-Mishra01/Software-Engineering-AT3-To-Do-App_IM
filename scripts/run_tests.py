#!/usr/bin/env python3
"""
Master test runner for To-Do App
Runs all test suites and provides a comprehensive report
"""
import os
import sys
import unittest
import time
import subprocess
from datetime import datetime

# Add parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ANSI colour codes for terminal output
class Colours:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    """Print a formatted header"""
    print(f"\n{Colours.BLUE}{Colours.BOLD}{'=' * 60}{Colours.END}")
    print(f"{Colours.BLUE}{Colours.BOLD}{text.center(60)}{Colours.END}")
    print(f"{Colours.BLUE}{Colours.BOLD}{'=' * 60}{Colours.END}\n")

def print_section(text):
    """Print a section header"""
    print(f"\n{Colours.CYAN}{Colours.BOLD}{text}{Colours.END}")
    print(f"{Colours.CYAN}{'-' * len(text)}{Colours.END}")

def run_test_suite(suite_name, test_module):
    """Run a specific test suite and return results"""
    print_section(f"Running {suite_name}")
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(test_module)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    start_time = time.time()
    result = runner.run(suite)
    end_time = time.time()
    
    # Calculate statistics
    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    success = total_tests - failures - errors
    duration = end_time - start_time
    
    # Print summary
    print(f"\n{Colours.BOLD}Summary for {suite_name}:{Colours.END}")
    print(f"  Total tests: {total_tests}")
    print(f"  {Colours.GREEN}✓ Passed: {success}{Colours.END}")
    if failures > 0:
        print(f"  {Colours.RED}✗ Failed: {failures}{Colours.END}")
    if errors > 0:
        print(f"  {Colours.RED}✗ Errors: {errors}{Colours.END}")
    print(f"  Duration: {duration:.2f}s")
    
    return {
        'name': suite_name,
        'total': total_tests,
        'passed': success,
        'failed': failures,
        'errors': errors,
        'duration': duration,
        'success': failures == 0 and errors == 0
    }

def check_server_running():
    """Check if Flask server is running"""
    try:
        import requests
        response = requests.get('http://localhost:5001', timeout=2)
        return True
    except:
        return False

def start_flask_server():
    """Start Flask server for testing"""
    print_section("Starting Flask Server")
    
    if check_server_running():
        print(f"{Colours.YELLOW}Flask server already running on port 5001{Colours.END}")
        return None
    
    # Start server in background
    server_process = subprocess.Popen(
        [sys.executable, 'run.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    
    # Wait for server to start
    print("Waiting for server to start...", end='', flush=True)
    for i in range(10):
        time.sleep(1)
        print(".", end='', flush=True)
        if check_server_running():
            print(f" {Colours.GREEN}Ready!{Colours.END}")
            return server_process
    
    print(f" {Colours.RED}Failed to start!{Colours.END}")
    server_process.terminate()
    return None

def main():
    """Main test runner"""
    print_header("To-Do App Test Suite")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check Python version
    print(f"Python version: {sys.version.split()[0]}")
    
    # Start Flask server if needed
    server_process = None
    if not check_server_running():
        server_process = start_flask_server()
        if not server_process and not check_server_running():
            print(f"{Colours.RED}ERROR: Could not start Flask server{Colours.END}")
            print("Please start the server manually with: python3 server.py")
            return 1
    
    # Import test modules
    test_modules = []
    try:
        from tests import test_unit
        test_modules.append(('Unit Tests', test_unit))
    except ImportError as e:
        print(f"{Colours.RED}Could not import unit tests: {e}{Colours.END}")
    
    try:
        from tests import test_integration
        test_modules.append(('Integration Tests', test_integration))
    except ImportError as e:
        print(f"{Colours.RED}Could not import integration tests: {e}{Colours.END}")
    
    try:
        from tests import test_frontend
        test_modules.append(('Frontend Tests', test_frontend))
    except ImportError as e:
        print(f"{Colours.RED}Could not import frontend tests: {e}{Colours.END}")
    
    try:
        from tests import test_security
        test_modules.append(('Security Tests', test_security))
    except ImportError as e:
        print(f"{Colours.RED}Could not import security tests: {e}{Colours.END}")
    
    try:
        from tests import test_performance
        test_modules.append(('Performance Tests', test_performance))
    except ImportError as e:
        print(f"{Colours.RED}Could not import performance tests: {e}{Colours.END}")
    
    # Run all test suites
    results = []
    for suite_name, test_module in test_modules:
        try:
            result = run_test_suite(suite_name, test_module)
            results.append(result)
        except Exception as e:
            print(f"{Colours.RED}Error running {suite_name}: {e}{Colours.END}")
            results.append({
                'name': suite_name,
                'total': 0,
                'passed': 0,
                'failed': 0,
                'errors': 1,
                'duration': 0,
                'success': False
            })
    
    # Run the existing test_app.py for API tests
    print_section("Running API Tests (test_app.py)")
    try:
        result = subprocess.run(
            [sys.executable, 'tests/test_app.py'],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            print(f"{Colours.GREEN}✓ API tests passed{Colours.END}")
            api_success = True
        else:
            print(f"{Colours.RED}✗ API tests failed{Colours.END}")
            print(result.stdout)
            print(result.stderr)
            api_success = False
    except Exception as e:
        print(f"{Colours.RED}Error running API tests: {e}{Colours.END}")
        api_success = False
    
    # Print final summary
    print_header("Test Summary")
    
    total_suites = len(results)
    total_tests = sum(r['total'] for r in results)
    total_passed = sum(r['passed'] for r in results)
    total_failed = sum(r['failed'] for r in results)
    total_errors = sum(r['errors'] for r in results)
    total_duration = sum(r['duration'] for r in results)
    
    print(f"{Colours.BOLD}Overall Results:{Colours.END}")
    print(f"  Test Suites: {total_suites}")
    print(f"  Total Tests: {total_tests}")
    print(f"  {Colours.GREEN}✓ Passed: {total_passed}{Colours.END}")
    
    if total_failed > 0:
        print(f"  {Colours.RED}✗ Failed: {total_failed}{Colours.END}")
    if total_errors > 0:
        print(f"  {Colours.RED}✗ Errors: {total_errors}{Colours.END}")
    
    print(f"  Total Duration: {total_duration:.2f}s")
    
    # Suite breakdown
    print(f"\n{Colours.BOLD}Suite Breakdown:{Colours.END}")
    for result in results:
        status = f"{Colours.GREEN}✓ PASS{Colours.END}" if result['success'] else f"{Colours.RED}✗ FAIL{Colours.END}"
        print(f"  {result['name']:<20} {status} ({result['passed']}/{result['total']} tests, {result['duration']:.2f}s)")
    
    if api_success:
        print(f"  {'API Tests':<20} {Colours.GREEN}✓ PASS{Colours.END}")
    else:
        print(f"  {'API Tests':<20} {Colours.RED}✗ FAIL{Colours.END}")
    
    # Overall status
    all_passed = all(r['success'] for r in results) and api_success
    
    if all_passed:
        print(f"\n{Colours.GREEN}{Colours.BOLD}🎉 All tests passed! 🎉{Colours.END}")
        exit_code = 0
    else:
        print(f"\n{Colours.RED}{Colours.BOLD}❌ Some tests failed ❌{Colours.END}")
        exit_code = 1
    
    # Cleanup
    if server_process:
        print(f"\n{Colours.YELLOW}Stopping test server...{Colours.END}")
        server_process.terminate()
        server_process.wait(timeout=5)
    
    print(f"\nCompleted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return exit_code

if __name__ == '__main__':
    sys.exit(main())