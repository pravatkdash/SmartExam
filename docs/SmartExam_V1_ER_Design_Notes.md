# SmartExam V1 — ER Design Notes

This document captures the ER/design decisions agreed during the SmartExam V1 design discussions.

## 1. Core Academic Hierarchy

```text
Institute
   |
   v
Program
   |
   v
Subject
   |
   v
Chapter
   |
   v
Question
   |
   v
Option
```

- Program belongs to Institute.
- Subject belongs to Program.
- Chapter belongs to Subject.
- Question belongs to Chapter.
- Option belongs to Question.
- Institute isolation is maintained through this hierarchy.

## 2. Users

User types:

```text
SUPER_ADMIN
ADMIN
TEACHER
STUDENT
```

- Super Admin belongs to SmartExam, not an Institute.
- Institute Admin belongs to exactly one Institute.
- Teacher belongs to exactly one Institute.
- Teacher cannot also be Admin in V1.
- Student's Institute/Program membership is determined through StudentEnrollment.
- A Student can belong to multiple Programs.

## 3. TeacherAssignment

```text
Teacher (User)
    |
    v
TeacherAssignment
    |
    v
Subject
```

Fields:

```text
id
teacher_id
subject_id
status
assigned_at
unassigned_at
created_at
updated_at
```

Rules:
- Only one ACTIVE TeacherAssignment per Subject.
- Teacher can teach multiple Subjects.
- Teachers can be reassigned to the same Subject later.
- Historical assignments are retained.
- Teacher and Subject must belong to the same Institute.
- Do not use UNIQUE(teacher_id, subject_id), because reassignment history is required.

## 4. StudentEnrollment

```text
Student
    |
    v
StudentEnrollment
    |
    v
Program
    |
    v
Institute
```

Status:

```text
PENDING / ACTIVE / REJECTED / INACTIVE
```

Fields:

```text
id
student_id
program_id
status
enrolled_at
approved_at
approved_by
created_at
updated_at
```

Rules:
- Student can belong to multiple Programs.
- Only one ACTIVE enrollment for the same Student + Program.
- Historical enrollment is retained.
- Approval information is retained.

## 5. Question

Fields:

```text
id
chapter_id
created_by
question_text
question_type
explanation
difficulty
status
created_at
updated_at
```

Question types:

```text
SINGLE_CHOICE
MULTIPLE_ANSWER
TRUE_FALSE
```

Rules:
- Questions are created by Teachers.
- Teacher must have an ACTIVE assignment to the relevant Subject.
- Question marks are NOT stored on Question in V1.
- Assessment defines marks_per_question.
- Teacher gets a review/confirmation before saving.
- Draft/unpublished questions can be edited/deactivated.
- Once used in a Published Assessment, a Question is protected.
- A protected Question cannot be edited or deleted.
- To correct a protected Question, create a new Question and use it in a new Assessment/version.

## 6. Option

Fields:

```text
id
question_id
option_text
is_correct
display_order
created_at
updated_at
```

Rules:
- Option belongs to one Question.
- No separate Option status in V1.
- Options are not randomized in V1.
- display_order controls display order.

## 7. Assessment

Fields:

```text
id
subject_id
created_by
name
description
duration_minutes
marks_per_question
status
published_at
created_at
updated_at
```

Status:

```text
DRAFT
SUBMITTED_FOR_REVIEW
PUBLISHED
CLOSED
```

Workflow:

```text
DRAFT
  |
  v
SUBMITTED_FOR_REVIEW
  |
  +-- Reject --> DRAFT
  |
  +-- Approve -> PUBLISHED
                    |
                    v
                  CLOSED
```

Rules:
- Assessment belongs to one Subject.
- Teacher must have an ACTIVE assignment to that Subject.
- Institute Admin reviews before publishing.
- Published Assessment is immutable.
- Published Assessment cannot return to Draft.
- Published Assessment cannot have Questions added, removed, or reordered.
- If changes are needed, create a new Assessment/version.
- Duration is mandatory.
- Timeout automatically submits the Attempt.
- Same marks per question in V1.
- No negative marking in V1.
- Multiple attempts are allowed.
- published_at records publication time.

## 8. AssessmentQuestion

Many-to-many bridge:

```text
Assessment
    |
    v
AssessmentQuestion
    |
    v
Question
```

Fields:

```text
id
assessment_id
question_id
display_order
```

Constraints:

```text
UNIQUE(assessment_id, question_id)
UNIQUE(assessment_id, display_order)
```

Rules:
- Same Question cannot appear twice in one Assessment.
- Same display_order cannot appear twice in one Assessment.
- Questions can be reused across Assessments.
- Published AssessmentQuestion records are immutable.

## 9. Attempt

```text
Student
    |
    v
Attempt
    |
    v
Assessment
```

Fields:

```text
id
student_id
assessment_id
attempt_number
started_at
completed_at
score
total_marks
status
created_at
updated_at
```

Status:

```text
IN_PROGRESS
COMPLETED
```

Rules:
- Multiple attempts allowed.
- UNIQUE(student_id, assessment_id, attempt_number).
- Score is immediately visible after submission.
- Timeout automatically completes the Attempt.
- V1 stores result summary only; individual answers are V2.
- total_marks is stored as a historical snapshot.
- Results are shown newest-first.

## 10. Institute Isolation

```text
Institute A
├── Programs
├── Subjects
├── Chapters
├── Teachers
├── Students
└── Assessments

Institute B
├── Programs
├── Subjects
├── Chapters
├── Teachers
├── Students
└── Assessments
```

Data from one Institute must not be visible or usable by another Institute.

Programs/Subjects/Questions/Assessments are not globally shared in V1.

## 11. Inactive Data Principle

> INACTIVE means no new activity, not deletion of historical data.

If a Subject becomes INACTIVE:

- No new Questions.
- No new Assessments.
- No new student activity under it.
- Existing Published Assessments remain.
- Existing Attempts remain.
- Historical Results remain.

## 12. Data Integrity

Recommended database constraints:

```text
UNIQUE(institute_id, program_code)
UNIQUE(program_id, subject_code)
UNIQUE(subject_id, chapter_code)

UNIQUE(assessment_id, question_id)
UNIQUE(assessment_id, display_order)

UNIQUE(student_id, assessment_id, attempt_number)
```

Special active-record rules:
- Only one ACTIVE TeacherAssignment per Subject.
- Only one ACTIVE StudentEnrollment per Student + Program.
- Only one ACTIVE Institute Admin per Institute.

## 13. Service-Layer Validation

The frontend is not the security boundary.

Examples:

```text
Teacher creates Assessment
    |
    +-- Teacher ACTIVE?
    +-- Teacher assigned to Subject?
    +-- Same Institute?
    +-- Assessment still DRAFT?
```

Student starts Assessment:

```text
Student ACTIVE?
    |
ACTIVE enrollment?
    |
Assessment belongs to student's Program?
    |
Assessment PUBLISHED?
    |
Allow Attempt
```

Published Assessment:

```text
PUBLISHED
    |
    +-- No editing
    +-- No question changes
    +-- No duration changes
    +-- No marks changes
```

## 14. Authentication & Authorization

Architecture principle:

```text
Request
   |
Authentication
   | Who is this user?
   v
Authorization
   | Is this user allowed?
   v
Service Layer
   | Business validation
   v
Database
```

Protected APIs require authentication.

The backend must reject unauthorized requests even if the UI is bypassed.

JWT/token authentication can be used for API authentication; the exact Django authentication approach will be finalized during implementation design.

## 15. Transactions

Use database transactions for multi-step operations that must succeed or fail together.

Important V1 examples:

### Assessment submission

```text
Submit
  -> Calculate score
  -> Complete Attempt
  -> Save score
  -> Save completed_at
```

### Assessment publishing

```text
Validate Assessment
  -> Validate Questions
  -> Freeze Assessment
  -> Set PUBLISHED
  -> Set published_at
```

### Teacher reassignment

```text
Teacher A -> INACTIVE
Teacher B -> ACTIVE
```

### Student enrollment approval

```text
PENDING -> ACTIVE
approved_by
approved_at
```

### Assessment creation

Assessment and its AssessmentQuestion records should not leave a partially created Assessment.

## 16. V1 Scope

- Institute management
- Programs
- Subjects
- Chapters
- Super Admin
- Institute Admin
- Teacher
- Student
- Teacher assignments
- Student enrollment
- Single Choice
- Multiple Answer
- True/False
- Question review/confirmation
- Assessment creation
- Admin review
- Assessment publishing
- Published Assessment immutability
- Duration
- Automatic submission on timeout
- Same marks per question
- No negative marking
- Multiple attempts
- Random question order
- Immediate score visibility
- Previous result history
- Institute isolation
- Backend authorization
- Database integrity
- Transactions

## 17. Deferred to V2

- Individual question marks
- Partial marking
- Negative marking
- Option randomization
- Different question sets per student
- Question pools
- Assessment sections
- Assessment availability windows
- Resume after browser close
- Detailed AttemptAnswer/history
- Multiple active teachers per Subject
- Teacher + Admin dual role
- Advanced analytics
- Advanced reporting
- Notifications
- Payment/subscription system

### V1/V2 Principle

> Defer complexity, not architecture.

A feature can be postponed, but V1 should not unnecessarily prevent adding it later.

## 18. Final ER Relationship Summary

```text
Institute
   |
   +-- 1:N --> Program
                  |
                  +-- 1:N --> Subject
                                |
                                +-- 1:N --> Chapter
                                              |
                                              +-- 1:N --> Question
                                                            |
                                                            +-- 1:N --> Option


User
   |
   +-- ADMIN ---------> Institute
   |
   +-- TEACHER -------> Institute
   |       |
   |       +-- 1:N --> TeacherAssignment -- N:1 --> Subject
   |
   +-- STUDENT
           |
           +-- 1:N --> StudentEnrollment -- N:1 --> Program


Teacher
   |
   +-- 1:N --> Assessment
                 |
                 +-- 1:N --> AssessmentQuestion -- N:1 --> Question


Student
   |
   +-- 1:N --> Attempt -- N:1 --> Assessment
```

## 19. Next Step

Before implementation:

1. Review this ER model.
2. Check for missing or contradictory relationships.
3. Define exact Django fields.
4. Define ForeignKey `on_delete` behavior.
5. Define indexes and constraints.
6. Define model/service validation.
7. Then implement Django models and migrations.

**Do not start implementation until the ER/model design review is complete.**
