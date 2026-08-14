# SmartExam V1 — Domain Model & ER Design

## Purpose

This document captures the V1 domain-model and ER-design decisions for SmartExam before implementation.

## 1. User and Institute

SmartExam uses one User model with roles:
- SUPER_ADMIN
- INSTITUTE_ADMIN
- TEACHER
- STUDENT

For V1, a user belongs to at most one Institute.

Relationship:

```text
INSTITUTE 1 ───── N USER
```

`institute_id` can be stored directly on User.

- SUPER_ADMIN → `institute_id = NULL`
- INSTITUTE_ADMIN / TEACHER / STUDENT → one Institute

Future multi-institute membership is V2/V3.

## 2. Institute Admin

An Institute may have multiple admin records historically, but only one active admin at a time.

```text
ABC Institute
├── Admin A → INACTIVE
├── Admin B → INACTIVE
└── Admin C → ACTIVE
```

Rules:
- One person cannot administer multiple Institutes.
- Admin and Teacher are separate responsibilities in V1.
- Leaving an Institute means becoming INACTIVE.
- Another admin can become ACTIVE.
- Historical records are retained.

## 3. Program

Program is the main student-access boundary.

Examples:
- Class 8
- Class 9
- NEET
- Institute-specific programs

Students enroll at Program level and automatically get access to all active Subjects in that Program.

### Future Platform Programs

SmartExam may later provide platform-owned Programs such as Odisha SSB. Institutes can subscribe instead of recreating them.

This is V2/V3-ready and should not complicate V1.

## 4. Program Customization

Future model:

```text
SmartExam Platform
└── Odisha SSB
     ├── Mathematics
     ├── General Science
     └── General Studies
             |
             | subscription
             v
ABC Institute
└── Odisha SSB
     ├── Platform Subjects
     └── Institute-specific additions
```

Platform-owned content is view/reuse only. Institutes cannot modify it, but can add institute-specific Subjects/Chapters where appropriate.

## 5. Academic Structure

Institute Admin owns and manages:

```text
Program
   ↓
Subject
   ↓
Chapter
```

Institute Admin:
- Creates/manages Programs
- Creates/manages Subjects
- Creates/manages Chapters
- Assigns Subjects to Teachers

Teacher does not manage this structure in V1.

## 6. Teacher Responsibility

Teacher V1 responsibilities:

```text
Teacher
   ↓
Questions
   ↓
Assessments
```

Teachers can create/reuse Questions and create/publish Assessments.

Teachers cannot modify Program/Subject/Chapter structure or another teacher's content.

## 7. Student Enrollment

Enrollment is at Program level.

```text
Student
   ↓
ABC Institute
   ↓
Class 8
   ├── Mathematics
   ├── Physics
   └── Chemistry
```

An ACTIVE enrollment gives access to all active Subjects and their published Assessments.

No separate Subject enrollment is required in V1.

## 8. Assessment Access

Students with ACTIVE enrollment can access all PUBLISHED assessments for their Program/Subject.

Draft, deleted, or out-of-scope assessments are not visible.

No explicit student-to-assessment assignment is required in V1.

## 9. Assessment Lifecycle

```text
DRAFT
  ↓
PUBLISHED
  ↓
CLOSED
```

Published assessments are immutable. If a new version is needed, create another assessment.

Closed assessments remain historical/read-only.

## 10. Assessment Configuration — V1

Each assessment has:
- Name
- Program
- Subject
- Creator/Teacher
- Duration
- Marks per question
- Attempt policy
- Status

Duration is mandatory (for example 30, 45, 60, 90 minutes).

Published assessments are available anytime until CLOSED.

Availability windows (`Available From` / `Available Until`) are V2.

When duration expires, the system automatically submits the attempt.

## 11. Attempts and Results — V1

Store the attempt/result summary, not individual answers.

Suggested data:
- Student
- Assessment
- Attempt number
- Started At
- Completed At
- Score
- Total Marks

Results are displayed in `completed_at DESC` order.

Detailed per-question answer storage is V2.

## 12. Scoring — V1

No negative marking.

```text
Correct      → full marks
Wrong        → 0
Unanswered   → 0
```

All questions in an assessment have the same marks value.

Different marks per individual question are V2.

Result is immediately visible after submission.

## 13. Question Types — V1

Supported:
1. Single Choice
2. Multiple Answer
3. True / False

Multiple Answer uses all-or-nothing scoring:

```text
Exact correct set → full marks
Anything else     → 0
```

## 14. Assessment Randomization — V1

Question order may be randomized per attempt.

All students use the same selected question set.

Option order is fixed in V1.

Option randomization and different question sets per student are V2.

## 15. Assessment Sections

V1 uses one question sequence:

```text
Q1 → Q2 → ... → Q100
```

Separate assessment sections are V2.

## 16. Question Reuse

Questions can be reused in multiple assessments.

Published assessments remain immutable even as the question bank evolves. Exact snapshot/version behavior will be finalized during implementation design.

## 17. Teacher Dashboard

Teacher can view:
- My Questions
- My Assessments (Draft / Published / Closed)
- Results for assessments created by that teacher

Teacher cannot view another teacher's results unless a future permission explicitly allows it.

## 18. Institute Admin Dashboard

Institute Admin has institute-wide visibility over:
- Programs
- Subjects
- Chapters
- Teachers
- Students
- Questions
- Assessments
- Results

Institute Admin can manage academic structure and enrollment/user governance, but cannot edit/publish teacher-created Questions or Assessments and cannot change results.

## 19. Teacher Deactivation / Unassignment

When a teacher is removed from a Subject assignment:
- Teacher becomes inactive/unassigned for that scope.
- Questions remain.
- Draft/Published/Closed assessments remain.
- Student attempts/results remain.

Historical data is retained.

A new teacher can be assigned later, but does not automatically inherit ownership/edit rights over old teacher content.

## 20. Conceptual V1 Model

```text
                         INSTITUTE
                             |
                             | 1:N
                             v
                           USER
                             |
                 +-----------+-----------+
                 |           |           |
              ADMIN       TEACHER     STUDENT
                             |           |
                             v           v
                         QUESTIONS    ENROLLMENT
                             |           |
                             v           v
                        ASSESSMENTS    PROGRAM
                             |           |
                             |           v
                             |        SUBJECT
                             |           |
                             |           v
                             |        CHAPTER
                             |
                             v
                          ATTEMPT
                             |
                             v
                           RESULT
```

This is conceptual only. Exact cardinalities, foreign keys, constraints, and Django models come next.

## 21. Future V2/V3 Scope

Not part of V1:
- Platform Program catalog/subscriptions
- State-wise exam ecosystem
- Platform-owned canonical exams/questions
- Bulk question upload/update
- Option randomization
- Different question sets per student
- Individual question marks
- Negative marking
- Partial marking
- Assessment sections
- Assessment availability windows
- Detailed per-question answer storage
- Detailed answer review/analytics
- Multi-institute user membership
- Admin + Teacher dual role
- Platform content synchronization/versioning

## 22. Next Design Phase

Finalize:
1. Program ↔ Subject ↔ Chapter cardinalities
2. Teacher Assignment
3. Student Enrollment
4. Question ↔ Option
5. Assessment ↔ Question
6. Attempt/Result
7. Soft-delete rules
8. Database constraints vs business-logic constraints

Then convert the approved domain model into Django models and migrations.
