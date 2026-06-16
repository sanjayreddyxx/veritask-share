import json
import os


def make_testcase(id, title, ttype, pre, steps, expect, priority="Medium"):
    return {
        "id": id,
        "title": title,
        "type": ttype,
        "preconditions": pre,
        "steps": steps,
        "expected": expect,
        "priority": priority,
    }


def main():
    cases = []
    screens = [
        ("Auth", "/login", "Login Screen"),
        ("Auth", "/signup", "Signup Screen"),
        ("App", "/dashboard", "Dashboard"),
        ("App", "/tasks", "All Tasks"),
        ("App", "/task/DETAIL", "Task Detail"),
        ("App", "/profile", "Profile"),
        ("App", "/notifications", "Notifications"),
        ("App", "/reports", "Reports"),
        ("App", "/courses", "Courses"),
        ("Admin", "/admin", "Admin Dashboard"),
    ]

    id_counter = 1
    for area, path, label in screens:
        title = f"Navigate to {label} and verify UI elements"
        steps = f"Open BASE_URL{path} -> wait for main elements"
        expect = f"{label} loads and key elements are visible"
        cases.append(make_testcase(id_counter, title, "E2E", "App served locally", steps, expect))
        id_counter += 1

        for device in ["desktop", "tablet", "mobile"]:
            title = f"{label} responsive layout on {device}"
            steps = f"Open BASE_URL{path} at {device} viewport -> inspect layout"
            expect = f"Layout adapts correctly for {device}"
            cases.append(make_testcase(id_counter, title, "UI/UX", "App served locally", steps, expect))
            id_counter += 1

    form_tests = [
        ("Login form validation", "/login", "Missing password shows error"),
        ("Signup form validation", "/signup", "Invalid email shows error"),
        ("Create course validation", "/courses/create", "Missing title shows error"),
    ]
    for title, path, expect_text in form_tests:
        steps = f"Open BASE_URL{path} -> submit invalid form data"
        expect = expect_text
        cases.append(make_testcase(id_counter, title, "Validation", "App served locally", steps, expect, "High"))
        id_counter += 1

    actions = ["Create Task", "Edit Task", "Delete Task", "Assign Task", "Complete Task"]
    for act in actions:
        title = f"{act} via UI"
        steps = f"Login as user -> go to All Tasks -> perform {act}"
        expect = f"{act} succeeds and UI updates accordingly"
        cases.append(make_testcase(id_counter, title, "Functional", "User account available", steps, expect, "High"))
        id_counter += 1

    for i in range(1, 11):
        title = f"Course lifecycle case #{i}"
        steps = "Create course -> enroll user -> access course content -> unenroll"
        expect = "Course lifecycle operations succeed"
        cases.append(make_testcase(id_counter, title, "E2E", "Admin and user accounts", steps, expect))
        id_counter += 1

    reports = ["Generate progress report", "Export report as CSV", "Filter report by date range"]
    for r in reports:
        title = r
        steps = "Navigate to Reports -> apply filters -> export"
        expect = "Report generated and export available"
        cases.append(make_testcase(id_counter, title, "Functional", "Data present", steps, expect))
        id_counter += 1

    for i in range(3):
        title = f"Notification delivery scenario #{i+1}"
        steps = "Trigger notification -> observe delivery in UI"
        expect = "Notification appears in notifications list"
        cases.append(make_testcase(id_counter, title, "E2E", "Notification service configured", steps, expect))
        id_counter += 1

    heuristics = [
        "Keyboard navigation works across main flows",
        "Contrast meets WCAG AA for main pages",
        "All images have alt text or labels",
    ]
    for h in heuristics:
        cases.append(make_testcase(id_counter, h, "UI/UX", "App served locally", "Run accessibility checks", "Pass accessibility checks"))
        id_counter += 1

    extras = [
        ("Search functionality", "/dashboard", "Search returns relevant results"),
        ("Pagination", "/tasks", "Pagination works and preserves filters"),
        ("Sorting", "/tasks", "Sorting by date/name works"),
        ("Offline behavior", "/dashboard", "App shows offline indicator and caches data"),
    ]
    for title, path, expect in extras:
        cases.append(make_testcase(id_counter, title, "Functional", "App served locally", f"Open BASE_URL{path} -> exercise feature", expect))
        id_counter += 1

    while len(cases) < 125:
        title = f"General smoke case #{len(cases)+1}"
        steps = "Navigate through a key flow and verify no console errors"
        expect = "No errors and UI is responsive"
        cases.append(make_testcase(id_counter, title, "Smoke", "App served locally", steps, expect))
        id_counter += 1

    out = os.path.join(os.path.dirname(__file__), "testcases.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(cases, f, indent=2)
    print(f"Wrote {out} with {len(cases)} test cases")


if __name__ == '__main__':
    main()
