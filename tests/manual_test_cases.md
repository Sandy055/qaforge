# Manual Test Cases
## ToDoApp — Task Management Web Application

---

## How to Read This Document

Each test case follows this format:
- TC-ID: Unique test case identifier
- Title: What is being tested
- Precondition: What must be true before running the test
- Steps: Exact steps to execute
- Expected Result: What should happen
- Priority: High / Medium / Low
- Type: Functional / Edge Case / Regression / Validation

---

## MODULE 1 — AUTHENTICATION

### Registration

| TC-ID | TC-AUTH-001 |
|---|---|
| Title | Register a new user with valid credentials |
| Precondition | Username does not already exist |
| Steps | 1. POST /register with username "testuser" and password "pass123" |
| Expected Result | 201 Created, message "User registered" |
| Priority | High |
| Type | Functional |

| TC-ID | TC-AUTH-002 |
|---|---|
| Title | Register with duplicate username |
| Precondition | User "testuser" already exists |
| Steps | 1. POST /register with username "testuser" and password "newpass123" |
| Expected Result | 409 Conflict, error "Username already exists" |
| Priority | High |
| Type | Functional |

| TC-ID | TC-AUTH-003 |
|---|---|
| Title | Register with password shorter than 6 characters |
| Precondition | None |
| Steps | 1. POST /register with username "newuser" and password "abc" |
| Expected Result | 400 Bad Request, error about password length |
| Priority | High |
| Type | Edge Case |

| TC-ID | TC-AUTH-004 |
|---|---|
| Title | Register with empty username |
| Precondition | None |
| Steps | 1. POST /register with username "" and password "pass123" |
| Expected Result | 400 Bad Request, error about empty username |
| Priority | High |
| Type | Edge Case |

| TC-ID | TC-AUTH-005 |
|---|---|
| Title | Register with missing username field |
| Precondition | None |
| Steps | 1. POST /register with only password field provided |
| Expected Result | 400 Bad Request, error about missing fields |
| Priority | High |
| Type | Edge Case |

| TC-ID | TC-AUTH-006 |
|---|---|
| Title | Register with missing password field |
| Precondition | None |
| Steps | 1. POST /register with only username field provided |
| Expected Result | 400 Bad Request, error about missing fields |
| Priority | High |
| Type | Edge Case |

| TC-ID | TC-AUTH-007 |
|---|---|
| Title | Register with exactly 6 character password |
| Precondition | None |
| Steps | 1. POST /register with username "user7" and password "abc123" |
| Expected Result | 201 Created — boundary value accepted |
| Priority | High |
| Type | Edge Case |

| TC-ID | TC-AUTH-008 |
|---|---|
| Title | Register with exactly 5 character password |
| Precondition | None |
| Steps | 1. POST /register with username "user8" and password "abc12" |
| Expected Result | 400 Bad Request — boundary value rejected |
| Priority | High |
| Type | Edge Case |

| TC-ID | TC-AUTH-009 |
|---|---|
| Title | Register with no request body |
| Precondition | None |
| Steps | 1. POST /register with empty body |
| Expected Result | 400 Bad Request |
| Priority | Medium |
| Type | Edge Case |

| TC-ID | TC-AUTH-010 |
|---|---|
| Title | Register with whitespace only username |
| Precondition | None |
| Steps | 1. POST /register with username "   " and password "pass123" |
| Expected Result | 400 Bad Request, username cannot be empty |
| Priority | High |
| Type | Edge Case |

---

### Login

| TC-ID | TC-AUTH-011 |
|---|---|
| Title | Login with valid credentials |
| Precondition | User exists with correct password |
| Steps | 1. POST /login with correct username and password |
| Expected Result | 200 OK, message "Login successful" |
| Priority | High |
| Type | Functional |

| TC-ID | TC-AUTH-012 |
|---|---|
| Title | Login with wrong password |
| Precondition | User exists |
| Steps | 1. POST /login with correct username but wrong password |
| Expected Result | 401 Unauthorized, error "Invalid password" |
| Priority | High |
| Type | Functional |

| TC-ID | TC-AUTH-013 |
|---|---|
| Title | Login with non-existent username |
| Precondition | None |
| Steps | 1. POST /login with username that does not exist |
| Expected Result | 404 Not Found, error "User not found" |
| Priority | High |
| Type | Functional |

| TC-ID | TC-AUTH-014 |
|---|---|
| Title | Login with missing password field |
| Precondition | None |
| Steps | 1. POST /login with only username provided |
| Expected Result | 400 Bad Request |
| Priority | High |
| Type | Edge Case |

| TC-ID | TC-AUTH-015 |
|---|---|
| Title | Login with empty request body |
| Precondition | None |
| Steps | 1. POST /login with empty body |
| Expected Result | 400 Bad Request |
| Priority | Medium |
| Type | Edge Case |

---

### Logout

| TC-ID | TC-AUTH-016 |
|---|---|
| Title | Logout existing user |
| Precondition | User exists |
| Steps | 1. POST /logout with valid username |
| Expected Result | 200 OK, message "Logout successful" |
| Priority | Medium |
| Type | Functional |

| TC-ID | TC-AUTH-017 |
|---|---|
| Title | Logout non-existent user |
| Precondition | None |
| Steps | 1. POST /logout with username that does not exist |
| Expected Result | 404 Not Found |
| Priority | Medium |
| Type | Functional |

| TC-ID | TC-AUTH-018 |
|---|---|
| Title | Logout with missing username field |
| Precondition | None |
| Steps | 1. POST /logout with empty body |
| Expected Result | 400 Bad Request |
| Priority | Medium |
| Type | Edge Case |

---

## MODULE 2 — TASK MANAGEMENT

### Create Task

| TC-ID | TC-TASK-001 |
|---|---|
| Title | Create task with all required fields |
| Precondition | User exists |
| Steps | 1. POST /tasks with title, username, priority "high" |
| Expected Result | 201 Created, task_id returned |
| Priority | High |
| Type | Functional |

| TC-ID | TC-TASK-002 |
|---|---|
| Title | Create task with missing title |
| Precondition | User exists |
| Steps | 1. POST /tasks without title field |
| Expected Result | 400 Bad Request, missing field error |
| Priority | High |
| Type | Edge Case |

| TC-ID | TC-TASK-003 |
|---|---|
| Title | Create task with missing username |
| Precondition | None |
| Steps | 1. POST /tasks without username field |
| Expected Result | 400 Bad Request, missing field error |
| Priority | High |
| Type | Edge Case |

| TC-ID | TC-TASK-004 |
|---|---|
| Title | Create task with missing priority |
| Precondition | User exists |
| Steps | 1. POST /tasks without priority field |
| Expected Result | 400 Bad Request, missing field error |
| Priority | High |
| Type | Edge Case |

| TC-ID | TC-TASK-005 |
|---|---|
| Title | Create task with invalid priority value |
| Precondition | User exists |
| Steps | 1. POST /tasks with priority "urgent" |
| Expected Result | 400 Bad Request, invalid priority error |
| Priority | High |
| Type | Edge Case |

| TC-ID | TC-TASK-006 |
|---|---|
| Title | Create task with empty title |
| Precondition | User exists |
| Steps | 1. POST /tasks with title "" |
| Expected Result | 400 Bad Request, title cannot be empty |
| Priority | High |
| Type | Edge Case |

| TC-ID | TC-TASK-007 |
|---|---|
| Title | Create task with whitespace only title |
| Precondition | User exists |
| Steps | 1. POST /tasks with title "   " |
| Expected Result | 400 Bad Request, title cannot be empty |
| Priority | High |
| Type | Edge Case |

| TC-ID | TC-TASK-008 |
|---|---|
| Title | Create task for non-existent user |
| Precondition | None |
| Steps | 1. POST /tasks with username that does not exist |
| Expected Result | 404 Not Found |
| Priority | High |
| Type | Functional |

| TC-ID | TC-TASK-009 |
|---|---|
| Title | Create task with priority "low" |
| Precondition | User exists |
| Steps | 1. POST /tasks with priority "low" |
| Expected Result | 201 Created |
| Priority | High |
| Type | Functional |

| TC-ID | TC-TASK-010 |
|---|---|
| Title | Create task with priority "medium" |
| Precondition | User exists |
| Steps | 1. POST /tasks with priority "medium" |
| Expected Result | 201 Created |
| Priority | High |
| Type | Functional |

| TC-ID | TC-TASK-011 |
|---|---|
| Title | Create task with optional due date |
| Precondition | User exists |
| Steps | 1. POST /tasks with due_date "2025-12-31" |
| Expected Result | 201 Created, due_date stored correctly |
| Priority | Medium |
| Type | Functional |

| TC-ID | TC-TASK-012 |
|---|---|
| Title | Create task without due date |
| Precondition | User exists |
| Steps | 1. POST /tasks without due_date field |
| Expected Result | 201 Created, due_date is null |
| Priority | Medium |
| Type | Functional |

---

### Retrieve Task

| TC-ID | TC-TASK-013 |
|---|---|
| Title | Retrieve existing task by ID |
| Precondition | Task exists |
| Steps | 1. GET /tasks/T001 |
| Expected Result | 200 OK, full task data returned |
| Priority | High |
| Type | Functional |

| TC-ID | TC-TASK-014 |
|---|---|
| Title | Retrieve non-existent task |
| Precondition | None |
| Steps | 1. GET /tasks/T999 |
| Expected Result | 404 Not Found |
| Priority | High |
| Type | Functional |

| TC-ID | TC-TASK-015 |
|---|---|
| Title | Retrieve task returns all expected fields |
| Precondition | Task exists |
| Steps | 1. GET /tasks/T001, check all fields present |
| Expected Result | task_id, title, username, priority, status, due_date all present |
| Priority | High |
| Type | Validation |

| TC-ID | TC-TASK-016 |
|---|---|
| Title | Retrieve all tasks returns correct count |
| Precondition | Multiple tasks exist |
| Steps | 1. GET /tasks |
| Expected Result | 200 OK, count matches number of tasks |
| Priority | Medium |
| Type | Functional |

---

### Update Task

| TC-ID | TC-TASK-017 |
|---|---|
| Title | Update task title |
| Precondition | Task exists |
| Steps | 1. PUT /tasks/T001 with new title |
| Expected Result | 200 OK, title updated |
| Priority | High |
| Type | Functional |

| TC-ID | TC-TASK-018 |
|---|---|
| Title | Update task status to in_progress |
| Precondition | Task exists with status pending |
| Steps | 1. PUT /tasks/T001 with status "in_progress" |
| Expected Result | 200 OK, status updated |
| Priority | High |
| Type | Functional |

| TC-ID | TC-TASK-019 |
|---|---|
| Title | Update task status to completed |
| Precondition | Task exists |
| Steps | 1. PUT /tasks/T001 with status "completed" |
| Expected Result | 200 OK, status updated |
| Priority | High |
| Type | Functional |

| TC-ID | TC-TASK-020 |
|---|---|
| Title | Update task with invalid status |
| Precondition | Task exists |
| Steps | 1. PUT /tasks/T001 with status "done" |
| Expected Result | 400 Bad Request, invalid status error |
| Priority | High |
| Type | Edge Case |

| TC-ID | TC-TASK-021 |
|---|---|
| Title | Update task with invalid priority |
| Precondition | Task exists |
| Steps | 1. PUT /tasks/T001 with priority "critical" |
| Expected Result | 400 Bad Request, invalid priority error |
| Priority | High |
| Type | Edge Case |

| TC-ID | TC-TASK-022 |
|---|---|
| Title | Update task with empty title |
| Precondition | Task exists |
| Steps | 1. PUT /tasks/T001 with title "" |
| Expected Result | 400 Bad Request, title cannot be empty |
| Priority | High |
| Type | Edge Case |

| TC-ID | TC-TASK-023 |
|---|---|
| Title | Update non-existent task |
| Precondition | None |
| Steps | 1. PUT /tasks/T999 with valid data |
| Expected Result | 404 Not Found |
| Priority | High |
| Type | Functional |

| TC-ID | TC-TASK-024 |
|---|---|
| Title | Update task due date |
| Precondition | Task exists |
| Steps | 1. PUT /tasks/T001 with due_date "2026-01-01" |
| Expected Result | 200 OK, due_date updated |
| Priority | Medium |
| Type | Functional |

---

### Delete Task

| TC-ID | TC-TASK-025 |
|---|---|
| Title | Delete existing task |
| Precondition | Task exists |
| Steps | 1. DELETE /tasks/T001 |
| Expected Result | 200 OK, message "Task deleted" |
| Priority | High |
| Type | Functional |

| TC-ID | TC-TASK-026 |
|---|---|
| Title | Delete non-existent task |
| Precondition | None |
| Steps | 1. DELETE /tasks/T999 |
| Expected Result | 404 Not Found |
| Priority | High |
| Type | Functional |

| TC-ID | TC-TASK-027 |
|---|---|
| Title | Deleted task not retrievable |
| Precondition | Task exists |
| Steps | 1. DELETE /tasks/T001, 2. GET /tasks/T001 |
| Expected Result | GET returns 404 Not Found |
| Priority | High |
| Type | Regression |

| TC-ID | TC-TASK-028 |
|---|---|
| Title | Deleting one task does not affect others |
| Precondition | Multiple tasks exist |
| Steps | 1. DELETE /tasks/T001, 2. GET /tasks/T002 |
| Expected Result | T002 still returns 200 OK |
| Priority | High |
| Type | Regression |

---

## MODULE 3 — TASK FILTERING

| TC-ID | TC-FILTER-001 |
|---|---|
| Title | Filter tasks by status pending |
| Precondition | Tasks with different statuses exist |
| Steps | 1. GET /tasks/filter?status=pending |
| Expected Result | Only pending tasks returned |
| Priority | High |
| Type | Functional |

| TC-ID | TC-FILTER-002 |
|---|---|
| Title | Filter tasks by status completed |
| Precondition | Tasks with different statuses exist |
| Steps | 1. GET /tasks/filter?status=completed |
| Expected Result | Only completed tasks returned |
| Priority | High |
| Type | Functional |

| TC-ID | TC-FILTER-003 |
|---|---|
| Title | Filter tasks by priority high |
| Precondition | Tasks with different priorities exist |
| Steps | 1. GET /tasks/filter?priority=high |
| Expected Result | Only high priority tasks returned |
| Priority | High |
| Type | Functional |

| TC-ID | TC-FILTER-004 |
|---|---|
| Title | Filter tasks by priority low |
| Precondition | Tasks with different priorities exist |
| Steps | 1. GET /tasks/filter?priority=low |
| Expected Result | Only low priority tasks returned |
| Priority | High |
| Type | Functional |

| TC-ID | TC-FILTER-005 |
|---|---|
| Title | Filter tasks by username |
| Precondition | Tasks for multiple users exist |
| Steps | 1. GET /tasks/filter?username=testuser |
| Expected Result | Only tasks for testuser returned |
| Priority | High |
| Type | Functional |

| TC-ID | TC-FILTER-006 |
|---|---|
| Title | Filter with invalid status value |
| Precondition | None |
| Steps | 1. GET /tasks/filter?status=unknown |
| Expected Result | 400 Bad Request |
| Priority | Medium |
| Type | Edge Case |

| TC-ID | TC-FILTER-007 |
|---|---|
| Title | Filter with invalid priority value |
| Precondition | None |
| Steps | 1. GET /tasks/filter?priority=urgent |
| Expected Result | 400 Bad Request |
| Priority | Medium |
| Type | Edge Case |

| TC-ID | TC-FILTER-008 |
|---|---|
| Title | Filter with no matching results |
| Precondition | No completed tasks exist |
| Steps | 1. GET /tasks/filter?status=completed |
| Expected Result | 200 OK, empty tasks list, count 0 |
| Priority | Medium |
| Type | Edge Case |

| TC-ID | TC-FILTER-009 |
|---|---|
| Title | Filter by both status and priority |
| Precondition | Tasks with various status and priority exist |
| Steps | 1. GET /tasks/filter?status=pending&priority=high |
| Expected Result | Only pending high priority tasks returned |
| Priority | Medium |
| Type | Functional |

| TC-ID | TC-FILTER-010 |
|---|---|
| Title | Filter by all three parameters |
| Precondition | Tasks exist for multiple users |
| Steps | 1. GET /tasks/filter?status=pending&priority=high&username=testuser |
| Expected Result | Only matching tasks returned |
| Priority | Medium |
| Type | Functional |

---

## MODULE 4 — DASHBOARD

| TC-ID | TC-DASH-001 |
|---|---|
| Title | Dashboard returns correct summary for valid user |
| Precondition | User exists with tasks |
| Steps | 1. GET /dashboard?username=testuser |
| Expected Result | 200 OK, correct counts for all statuses |
| Priority | High |
| Type | Functional |

| TC-ID | TC-DASH-002 |
|---|---|
| Title | Dashboard for user with no tasks |
| Precondition | User exists with no tasks |
| Steps | 1. GET /dashboard?username=emptyuser |
| Expected Result | 200 OK, all counts are 0 |
| Priority | High |
| Type | Edge Case |

| TC-ID | TC-DASH-003 |
|---|---|
| Title | Dashboard for non-existent user |
| Precondition | None |
| Steps | 1. GET /dashboard?username=ghost |
| Expected Result | 404 Not Found |
| Priority | High |
| Type | Functional |

| TC-ID | TC-DASH-004 |
|---|---|
| Title | Dashboard without username parameter |
| Precondition | None |
| Steps | 1. GET /dashboard with no parameters |
| Expected Result | 400 Bad Request |
| Priority | High |
| Type | Edge Case |

| TC-ID | TC-DASH-005 |
|---|---|
| Title | Dashboard pending count matches actual |
| Precondition | User has 3 pending tasks |
| Steps | 1. Create 3 pending tasks, 2. GET /dashboard |
| Expected Result | pending count equals 3 |
| Priority | High |
| Type | Validation |

| TC-ID | TC-DASH-006 |
|---|---|
| Title | Dashboard updates after task completed |
| Precondition | User has pending task |
| Steps | 1. GET dashboard, 2. Update task to completed, 3. GET dashboard again |
| Expected Result | completed count increases by 1, pending decreases by 1 |
| Priority | High |
| Type | Validation |

| TC-ID | TC-DASH-007 |
|---|---|
| Title | Dashboard updates after task deleted |
| Precondition | User has tasks |
| Steps | 1. GET dashboard, note total, 2. Delete a task, 3. GET dashboard again |
| Expected Result | total count decreases by 1 |
| Priority | High |
| Type | Regression |

| TC-ID | TC-DASH-008 |
|---|---|
| Title | Dashboard high priority count correct |
| Precondition | User has mix of priority tasks |
| Steps | 1. Create high, medium, low priority tasks, 2. GET dashboard |
| Expected Result | high_priority count matches number of high priority tasks |
| Priority | High |
| Type | Validation |

| TC-ID | TC-DASH-009 |
|---|---|
| Title | Dashboard only shows tasks for requested user |
| Precondition | Multiple users with tasks exist |
| Steps | 1. GET /dashboard?username=user1 |
| Expected Result | Only user1 tasks counted, not user2 tasks |
| Priority | High |
| Type | Functional |

---

## END TO END WORKFLOW TESTS

| TC-ID | TC-E2E-001 |
|---|---|
| Title | Full user workflow — register, create task, complete task |
| Precondition | None |
| Steps | 1. Register new user, 2. Create task, 3. Update task to completed, 4. Check dashboard shows completed count of 1 |
| Expected Result | All steps succeed, dashboard reflects correct state |
| Priority | High |
| Type | Validation |

| TC-ID | TC-E2E-002 |
|---|---|
| Title | Multiple users do not see each other's tasks |
| Precondition | None |
| Steps | 1. Register user1 and user2, 2. Create tasks for each, 3. Filter by each username |
| Expected Result | Each user only sees their own tasks |
| Priority | High |
| Type | Validation |

| TC-ID | TC-E2E-003 |
|---|---|
| Title | Task count consistency across dashboard and filter |
| Precondition | User with tasks exists |
| Steps | 1. GET dashboard pending count, 2. GET filter by status pending, compare counts |
| Expected Result | Both counts match |
| Priority | High |
| Type | Validation |

| TC-ID | TC-E2E-004 |
|---|---|
| Title | Create and immediately retrieve task |
| Precondition | User exists |
| Steps | 1. POST /tasks, get task_id, 2. GET /tasks/task_id |
| Expected Result | Retrieved task matches created task exactly |
| Priority | High |
| Type | Functional |

| TC-ID | TC-E2E-005 |
|---|---|
| Title | Update task and verify change persisted |
| Precondition | Task exists |
| Steps | 1. PUT /tasks/T001 with new title, 2. GET /tasks/T001 |
| Expected Result | Retrieved task shows updated title |
| Priority | High |
| Type | Functional |

---

## Test Case Summary

| Module | Total Cases | High | Medium | Low |
|---|---|---|---|---|
| Authentication | 18 | 14 | 4 | 0 |
| Task Management | 28 | 24 | 4 | 0 |
| Task Filtering | 10 | 5 | 5 | 0 |
| Dashboard | 9 | 8 | 1 | 0 |
| End to End | 5 | 5 | 0 | 0 |
| Total | 70 | 56 | 14 | 0 |

Note: Additional edge case and regression test cases are implemented
in the automated test suite, bringing total coverage to 80+ scenarios.
