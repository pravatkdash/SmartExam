# SmartExam V1 — Student Portal Phase

## Objective

Complete the **Student Portal from UI to full functional testing**.

This phase covers the complete student journey:

> Student Login → Dashboard → Available Assessment → Instructions → Start Exam → Answer Questions → Navigate → Submit → Result → Attempt History → Profile/Logout

### V1 Rule

Keep the existing SmartExam V1 backend/design stable.

- Fix bugs when required.
- Add only functionality required for the agreed V1 student journey.
- New ideas/features should be marked **V2** instead of changing V1 scope.

---

# 1. Current Starting Point

The following are already working or substantially implemented:

- [x] Student registration by Institute Admin
- [x] Student login
- [x] Student dashboard exists
- [x] Assessment/question infrastructure exists
- [x] Admin can create questions
- [x] Admin can create assessments
- [x] Published assessment flow exists or is being finalized

Before modifying anything, verify the current implementation.

---

# 2. Student Portal UI

## 2.1 Student Dashboard

### Goal

Create a clean, simple student-focused dashboard.

### Expected content

- Welcome message
- Student name
- Available assessments
- Assessment title
- Subject
- Chapter / scope
- Number of questions
- Total marks
- Duration
- Assessment status
- View/Start button
- Result/history access
- Profile access
- Logout

### Checklist

- [ ] Review current dashboard
- [ ] Improve layout
- [ ] Make assessment cards clear
- [ ] Show useful assessment information
- [ ] Hide admin/teacher functionality
- [ ] Add responsive layout
- [ ] Test desktop view
- [ ] Test mobile-sized view

---

# 3. Assessment Details / Instructions

When a student selects an assessment:

Display:

- Assessment name
- Subject
- Chapter / scope
- Number of questions
- Total marks
- Duration
- Negative marking information
- Attempt information
- Instructions
- Start Exam button

### Checklist

- [ ] Assessment details page
- [ ] Only published assessments visible
- [ ] Student can view valid assessment
- [ ] Invalid assessment handled safely
- [ ] Start button works
- [ ] Clear instructions before starting

---

# 4. Exam Screen

## Required V1 functionality

- [ ] Display one question at a time or agreed question layout
- [ ] Display question number
- [ ] Display question text
- [ ] Display options
- [ ] Support single-answer MCQ
- [ ] Support multiple-answer MCQ
- [ ] Display marks
- [ ] Display negative marks where applicable
- [ ] Question navigation
- [ ] Previous button
- [ ] Next button
- [ ] Question status
- [ ] Answer selection
- [ ] Save answer
- [ ] Submit exam
- [ ] Timer

### Question states

Use clear visual/status indicators for:

- Not visited
- Visited but unanswered
- Answered
- Current question

---

# 5. Timer

## V1 Requirements

- [ ] Timer starts when exam starts
- [ ] Timer displays remaining time
- [ ] Timer decreases correctly
- [ ] Refresh does not incorrectly reset timer
- [ ] Exam automatically submits when time expires
- [ ] Student cannot continue after expiry
- [ ] Server-side time validation where required

### Important

Do not rely only on JavaScript for exam timing/security.

---

# 6. Submit Exam

Before final submission:

Display confirmation such as:

> You have answered X out of Y questions. Are you sure you want to submit?

### Checklist

- [ ] Submit confirmation
- [ ] Cancel submission
- [ ] Final submission works
- [ ] Double submission prevented
- [ ] Answers are finalized
- [ ] Attempt status updated
- [ ] Student redirected to result

---

# 7. Result Screen

Display:

- Assessment name
- Student name
- Score
- Total marks
- Correct answers
- Incorrect answers
- Unanswered questions
- Percentage
- Result status if applicable
- Attempt date/time

### Checklist

- [ ] Result calculated correctly
- [ ] Positive marks correct
- [ ] Negative marks correct
- [ ] Multiple-answer scoring follows V1 rules
- [ ] Unanswered questions handled correctly
- [ ] Result belongs only to logged-in student
- [ ] Result cannot be modified by student

---

# 8. Attempt / Result History

Student should be able to see previous attempts.

Example:

| Assessment | Date | Score | Status | Action |
|---|---|---:|---|---|
| Physics Test | 14 Sep | 72/100 | Completed | View Result |

### Checklist

- [ ] Attempt history page
- [ ] Only current student's attempts shown
- [ ] Latest attempts visible
- [ ] View result works
- [ ] Empty history handled
- [ ] Unauthorized access blocked

---

# 9. Student Profile

V1 profile can remain simple.

Display:

- Name
- Mobile number
- Email if applicable
- Institute/program information if applicable
- Account information

### Checklist

- [ ] Profile page
- [ ] Correct student information
- [ ] Sensitive/internal fields not exposed
- [ ] Edit functionality only if required by V1

---

# 10. Logout

### Checklist

- [ ] Logout works
- [ ] Session is invalidated
- [ ] Back button cannot reopen protected student pages
- [ ] Dashboard requires login
- [ ] Exam pages require valid student session

---

# 11. Access Control / Security Testing

These tests are mandatory.

## Student isolation

- [ ] Student A cannot view Student B's result
- [ ] Student A cannot view Student B's attempt
- [ ] Student A cannot modify another student's attempt
- [ ] Student cannot access teacher pages
- [ ] Student cannot access institute-admin pages
- [ ] Student cannot access Django admin

## Assessment protection

- [ ] Draft assessment cannot be started
- [ ] Inactive assessment cannot be started
- [ ] Invalid assessment ID handled safely
- [ ] Unauthorized assessment access blocked

## Attempt protection

- [ ] Attempt belongs to correct student
- [ ] Attempt cannot be reassigned through URL manipulation
- [ ] Completed attempt cannot be submitted again
- [ ] Expired attempt cannot continue

---

# 12. Complete Student Journey Test

This is the primary happy-path test.

## Scenario ST-001 — Complete Student Exam Journey

1. [ ] Register student through Institute Admin
2. [ ] Confirm student account exists
3. [ ] Login using mobile + PIN
4. [ ] Open Student Dashboard
5. [ ] Verify available published assessment
6. [ ] Open assessment details
7. [ ] Read instructions
8. [ ] Start exam
9. [ ] Verify timer
10. [ ] Answer question 1
11. [ ] Move to next question
12. [ ] Answer several questions
13. [ ] Leave one question unanswered
14. [ ] Navigate backward
15. [ ] Verify previously selected answers
16. [ ] Submit exam
17. [ ] Confirm submission
18. [ ] Verify result
19. [ ] Verify score calculation
20. [ ] Open attempt history
21. [ ] Verify completed attempt
22. [ ] Open result again
23. [ ] Logout
24. [ ] Verify protected pages require login

---

# 13. Functional Edge-Case Testing

## Login

- [ ] Correct mobile + PIN
- [ ] Wrong PIN
- [ ] Unknown mobile
- [ ] Empty mobile
- [ ] Empty PIN
- [ ] Invalid PIN length
- [ ] Logout then access dashboard

## Assessment

- [ ] Published assessment
- [ ] Draft assessment
- [ ] Inactive assessment
- [ ] Assessment with zero questions
- [ ] Assessment with one question
- [ ] Assessment with many questions

## Questions

- [ ] Single-answer question
- [ ] Multiple-answer question
- [ ] Unanswered question
- [ ] Last question
- [ ] First question
- [ ] Navigation backward/forward

## Submission

- [ ] Normal submission
- [ ] Submission with unanswered questions
- [ ] Double-click submit
- [ ] Refresh during exam
- [ ] Browser back during exam
- [ ] Timer reaches zero

---

# 14. Calculation Testing

Create a small controlled assessment specifically for calculation testing.

Example:

- 10 questions
- +1 mark for correct answer
- -0.25 for incorrect answer
- 0 for unanswered

Test:

### Case A

10 correct

Expected:

`10`

### Case B

5 correct, 5 unanswered

Expected:

`5`

### Case C

5 correct, 5 incorrect

Expected:

`5 - 1.25 = 3.75`

### Case D

10 incorrect

Expected:

`-2.5`

Verify the actual V1 business rule if SmartExam intentionally prevents negative final scores.

---

# 15. UI Quality Checklist

Before declaring the Student Portal complete:

- [ ] Consistent navbar
- [ ] Consistent typography
- [ ] Consistent buttons
- [ ] Clear primary actions
- [ ] Good spacing
- [ ] No unnecessary admin terminology
- [ ] Helpful empty states
- [ ] Helpful error messages
- [ ] Mobile-friendly layout
- [ ] No broken links
- [ ] No template errors
- [ ] No visible Django debug information in production-like testing

---

# 16. Backend / Code Review

For every student feature verify:

- [ ] URL is correct
- [ ] View is correct
- [ ] Login protection exists
- [ ] Student role protection exists
- [ ] Query filters by logged-in student where required
- [ ] Template is correct
- [ ] POST actions use CSRF protection
- [ ] Invalid IDs are handled
- [ ] Database relationships are correct
- [ ] No unnecessary duplicate logic
- [ ] No debug print statements
- [ ] No hard-coded student IDs
- [ ] No hard-coded assessment IDs

---

# 17. Database Testing

Verify:

- [ ] Student record
- [ ] Assessment
- [ ] Questions
- [ ] Options
- [ ] Attempt
- [ ] Student answers
- [ ] Result

Check that relationships are correct.

Important:

> A student must only see and modify data belonging to their own account/attempt.

---

# 18. Testing Order

Do NOT test everything at once.

Use this order:

### Stage 1 — Login

Student registration → Login → Logout

### Stage 2 — Dashboard

Login → Dashboard → Assessment list

### Stage 3 — Assessment

Dashboard → Assessment details → Instructions

### Stage 4 — Exam

Start → Question → Answer → Navigation

### Stage 5 — Submission

Submit → Confirmation → Finalize attempt

### Stage 6 — Result

Result calculation → Result display

### Stage 7 — History

Attempt history → Previous result

### Stage 8 — Security

Unauthorized URLs → Student isolation → Role protection

### Stage 9 — Edge Cases

Timer → Refresh → Back button → Double submit → Invalid data

### Stage 10 — Final Regression

Run the complete student journey again from a clean test state.

---

# 19. V1 Completion Criteria

Student Portal is considered complete only when:

- [ ] Student can register
- [ ] Student can login
- [ ] Student sees appropriate assessments
- [ ] Student can read assessment instructions
- [ ] Student can start an exam
- [ ] Student can answer questions
- [ ] Student can navigate questions
- [ ] Timer works
- [ ] Student can submit
- [ ] Attempt is finalized correctly
- [ ] Result is calculated correctly
- [ ] Result is displayed correctly
- [ ] Attempt history works
- [ ] Student can logout
- [ ] Access control works
- [ ] Edge cases are tested
- [ ] No critical UI bugs remain
- [ ] No critical backend bugs remain
- [ ] Complete regression test passes

---

# 20. V2 Parking Lot

Do not implement these during V1 unless already required by the frozen design.

Possible V2 features:

- Leaderboard
- Paid assessments
- Coupons
- Certificates
- Advanced analytics
- Student performance charts
- Bookmarks
- Question comments/discussion
- Social/community features
- Advanced notifications
- Gamification
- Subscription system
- Advanced student personalization

Keep these separate from V1.

---

# 21. Working Method

We will work **one step at a time**.

For each feature:

1. Inspect existing code
2. Decide what needs changing
3. Make the smallest required change
4. Run the server
5. Test manually
6. Fix issues
7. Mark the scenario complete
8. Move to the next feature

Do not make large batches of unrelated changes.

---

# Student Portal Status

| Area | Status |
|---|---|
| Student Registration | ✅ Working |
| Student Login | ✅ Working |
| Dashboard | 🔄 UI improvement/testing |
| Assessment List | 🔄 Testing |
| Assessment Details | ⬜ |
| Exam Screen | ⬜ |
| Question Navigation | ⬜ |
| Timer | ⬜ |
| Submission | ⬜ |
| Result | ⬜ |
| Attempt History | ⬜ |
| Profile | ⬜ |
| Logout | ⬜ |
| Security Testing | ⬜ |
| Edge-Case Testing | ⬜ |
| Final Regression | ⬜ |

**Current starting point: Student Dashboard UI.**
