# Scripts Directory

This directory contains utility scripts for the To-Do application.

## Scripts

### run_tests.py
Master test runner that executes all test suites with coloured output.

Usage:
```bash
python scripts/run_tests.py
```

Features:
- Automatically starts Flask server if needed
- Runs all test suites (unit, integration, frontend, security, performance)
- Provides coloured output for easy reading
- Returns proper exit codes for CI/CD integration

## Running Scripts

All scripts should be run from the project root directory:
```bash
cd /path/to/Software-Engineering-AT3-To-Do-App_IM
python scripts/script_name.py
```