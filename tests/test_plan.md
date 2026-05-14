# QAForge Test Plan
## ToDoApp — Task Management Web Application

---

## 1. Introduction

This test plan defines the testing strategy, scope, objectives, and approach
for the ToDoApp task management web application. It covers all four modules
of the application across functional, regression, validation, and edge-case
testing scenarios.

---

## 2. Objectives

- Verify all features function correctly under normal conditions
- Validate the application meets user requirements and business needs
- Identify defects across all severity levels before release
- Ensure edge cases and invalid inputs are handled gracefully
- Confirm regression coverage so new changes do not break existing features

---

## 3. Scope

### In Scope
- Authentication Module: register, login, logout
- Task Management Module: create, read, update, delete tasks
- Task Filtering Module: filter by status, priority, username
- Dashboard Module: task summary by status and priority

### Out of Scope
- Performance and load testing
- Security penetration testing
- Mobile browser compatibility

---

## 4. Test Types

### Functional Testing
Verify each feature works correctly under normal expected conditions.
Every endpoint is tested with valid inputs and expected outputs.

### Regression Testing
Re-run the full test suite after every code change to ensure existing
functionality has not been broken by new changes.

### Validation Testing
Verify the application meets actual user needs — not just technical
specifications. Includes end-to-end user workflow testing.

### Edge Case Testing
Test boundary conditions, invalid inputs, empty values, and unexpected
scenarios that real users may trigger.

---

## 5. Modules and Feature Areas

### Module 1 — Authentication
| Feature | Priority |
|---|---|
| User registration with valid credentials | High |
| User registration with duplicate username | High |
| User registration with short password | High |
| User registration with empty username | High |
| User login with valid credentials | High |
| User login with wrong password | High |
| User login with non-existent username | High |
| User logout | Medium |

### Module 2 — Task Management
| Feature | Priority |
|---|---|
| Create task with all required fields | High |
| Create task with missing fields | High |
| Create task with invalid priority | High |
| Create task with empty title | High |
| Retrieve existing task by ID | High |
| Retrieve non-existent task | High |
| Update task title | High |
| Update task status | High |
| Update task priority | High |
| Delete existing task | High |
| Delete non-existent task | High |
| Retrieve all tasks | Medium |

### Module 3 — Task Filtering
| Feature | Priority |
|---|---|
| Filter tasks by status | High |
| Filter tasks by priority | High |
| Filter tasks by username | High |
| Filter with invalid status value | Medium |
| Filter with invalid priority value | Medium |
| Filter with no matching results | Medium |
| Combined filters | Medium |

### Module 4 — Dashboard
| Feature | Priority |
|---|---|
| Dashboard summary for valid user | High |
| Dashboard with no tasks | High |
| Dashboard counts match actual tasks | High |
| Dashboard for non-existent user | High |
| Dashboard updates after task changes | High |

---

## 6. Entry and Exit Criteria

### Entry Criteria
- Application is deployed and accessible
- All required test data is prepared
- Test environment matches specification

### Exit Criteria
- All high priority test cases executed
- No open Critical or P1 defects
- All defects documented with reproduction steps
- Test results and defect log updated

---

## 7. Test Environment

- Language: Python 3.9.6
- Framework: Flask 3.1.3
- Test Tool: pytest
- Browser Automation: Selenium
- OS: macOS
- Defect Tracking: Defect log maintained in defects/defect_log.md

---

## 8. Defect Severity Classification

| Severity | Definition | Example |
|---|---|---|
| Critical | System unusable, data loss, security breach | Login always fails |
| High | Major feature broken, no workaround | Cannot create tasks |
| Medium | Feature partially broken, workaround exists | Filter returns wrong count |
| Low | Cosmetic or minor issue | Extra whitespace in response |

---

## 9. Test Deliverables

- Test Plan (this document)
- Manual Test Cases (manual_test_cases.md)
- Automated Test Suite (test_auth.py, test_tasks.py, test_filtering.py, test_regression.py)
- Defect Log (defects/defect_log.md)
- Individual Defect Reports (defects/DEF-00X.md)
- Release Notes (docs/release_notes.md)

---

## 10. Roles and Responsibilities

| Role | Responsibility |
|---|---|
| QA Engineer | Test case design, execution, defect reporting |
| Developer | Bug fixes, code changes |
| Stakeholder | Acceptance criteria, requirement clarification |

---

## Document Control

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | 2025-07-01 | Santhosh Malarvannan | Initial test plan |
| 1.1 | 2025-08-15 | Santhosh Malarvannan | Added filtering module |
| 1.2 | 2025-10-01 | Santhosh Malarvannan | Updated exit criteria |
