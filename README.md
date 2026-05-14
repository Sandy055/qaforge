# QAForge

A comprehensive manual and automated test suite for a multi-module
task management web application — built to demonstrate end-to-end
Software Quality Assurance skills.

## What This Project Is

QAForge demonstrates a complete QA process applied to a real web
application — from test planning and manual test case design through
automated regression testing, defect reporting, and living documentation.

## Project Structure

| Path | Description |
|---|---|
| app/todo_app.py | Flask web application being tested |
| tests/test_plan.md | Comprehensive test plan document |
| tests/manual_test_cases.md | 80+ manual test cases by module |
| tests/test_auth.py | Automated tests for authentication module |
| tests/test_tasks.py | Automated tests for task management module |
| tests/test_filtering.py | Automated tests for filtering and dashboard |
| tests/test_regression.py | Full regression test suite |
| defects/defect_log.md | Master defect log |
| defects/DEF-001.md | Defect report — filter validation |
| defects/DEF-002.md | Defect report — dashboard 404 handling |
| defects/DEF-003.md | Defect report — title whitespace |
| docs/release_notes.md | Release notes across test cycles |

## Test Results

test_auth.py        21 tests   all passing
test_tasks.py       32 tests   all passing
test_filtering.py   23 tests   all passing
test_regression.py  18 tests   all passing
Total               94 tests   all passing

## Skills Demonstrated

- Test plan design covering functional, regression, validation, edge cases
- 80+ manual test cases organized by module and priority
- Automated regression suite using pytest
- Boundary value analysis and edge case coverage
- Defect lifecycle — identification, documentation, verification
- Root cause analysis
- Living test documentation and release notes
- Python, Flask, pytest

## How to Run

python3 -m venv venv
source venv/bin/activate
pip install flask pytest selenium webdriver-manager
python3 -m pytest tests/ -v --ignore=tests/test_plan.md --ignore=tests/manual_test_cases.md
