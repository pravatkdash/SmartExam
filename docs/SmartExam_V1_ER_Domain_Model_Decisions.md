# SmartExam V1 — ER / Domain Model Decisions

This document records the agreed V1 entity relationships, ownership rules, authorization boundaries, and assessment lifecycle decisions.

## Core hierarchy


INSTITUTE
   │
   └── 1:N ── PROGRAM
                 │
                 └── 1:N ── SUBJECT
                               │
                               ├── 1:N ── CHAPTER
                               │             │
                               │             └── 1:N ── QUESTION
                               │                            │
                               │                            └── 1:N ── OPTION
                               │
                               └── 1:N ── ASSESSMENT
                                              │
                                              ├── created_by → TEACHER
                                              │
                                              └── N:M QUESTIONS
                                                     │
                                                     └── AssessmentQuestion

TEACHER
   │
   └── 1:N ── TEACHER_ASSIGNMENT ── N:1 ── SUBJECT

STUDENT
   │
   └── 1:N ── STUDENT_ENROLLMENT ── N:1 ── PROGRAM

STUDENT
   │
   └── 1:N ── ATTEMPT ── N:1 ── ASSESSMENT

```text
INSTITUTE
   |
   | 1:N
   v
PROGRAM
   |
   | 1:N
   v
SUBJECT
   |
   | 1:N
   v
CHAPTER
   |
   | 1:N
   v
QUESTION
   |
   | 1:N
   v
OPTION
```

- One Institute → many Programs; Programs are isolated per Institute.
- One Program → many Subjects; a Subject belongs to one Program.
- One Subject → many Chapters; a Chapter belongs to one Subject.
- Class 8 Mathematics and Class 9 Mathematics are separate Subject records.
- Chapters are not shared across Subjects in V1.
- Programs/academic records are deactivated rather than physically deleted when appropriate.

## Users and Institute

Roles:
- SUPER_ADMIN
- INSTITUTE_ADMIN
- TEACHER
- STUDENT

V1:
- A User belongs to at most one Institute.
- `institute_id` may be stored directly on User.
- SUPER_ADMIN may have `institute_id = NULL`.
- One person cannot administer multiple Institutes.
- Only one Institute Admin is ACTIVE at a time; previous admins become INACTIVE and history is retained.

## Teacher Assignment

```text
TEACHER
   1
   |
   | N
   v
TEACHER_ASSIGNMENT
   ^
   |
   | N
   |
SUBJECT
```

V1:
- Only a TEACHER can be assigned to a Subject.
- Institute Admin manages assignments.
- One Subject has at most one ACTIVE Teacher.
- One Teacher can have many Subject assignments.
- A Subject may temporarily have no active Teacher.
- Assignment history is retained.
- Multiple teachers per Subject are V2.

## Teacher scope / authorization

A Teacher may create Questions and Assessments only within an ACTIVE Subject assignment.

Backend must validate:

```text
Teacher
  ↓
ACTIVE TeacherAssignment
  ↓
Subject
  ↓
Chapter
```

The Chapter must belong to that Subject. UI filtering alone is not sufficient.

## Question ownership

```text
TEACHER 1:N QUESTION
CHAPTER 1:N QUESTION
```

A Question:
- is created/owned by its Teacher;
- belongs to exactly one Chapter;
- derives Subject → Program → Institute through Chapter.

No redundant `subject_id`, `program_id`, or `institute_id` is required on Question.

## Question types / options

All question types use the same Option model.

V1:
1. Single Choice — exactly one correct option.
2. Multiple Answer — one or more correct options; all-or-nothing scoring.
3. True/False — exactly two options, exactly one correct.

Relationship:

```text
QUESTION 1:N OPTION
```

## Question reuse

A Question can be reused in multiple Assessments.

Other teachers may reuse/view permitted Questions but cannot edit or delete the original Teacher's Question.

## Question ↔ Assessment

Many-to-many through `AssessmentQuestion`:

```text
QUESTION 1:N ASSESSMENT_QUESTION N:1 ASSESSMENT
```

Initial fields:
- `assessment_id`
- `question_id`
- `display_order`

Constraints:
- `UNIQUE(assessment_id, question_id)` — a Question appears at most once in an Assessment.
- `UNIQUE(assessment_id, display_order)` — stored order is unique.

## Question soft delete

Questions are soft-deleted.

If a deleted Question is already in a Published Assessment:
- it is hidden from the active Question Bank;
- it cannot be selected for new Assessments;
- it cannot be edited;
- existing Published Assessments continue to use it;
- historical Attempts/Results remain valid.

A Draft Assessment containing a deleted Question should not be publishable until the Question is replaced/removed.

## Assessment ownership and scope

```text
TEACHER 1:N ASSESSMENT
SUBJECT 1:N ASSESSMENT
```

Assessment stores:
- `subject_id`
- `created_by` → Teacher

`subject_id` identifies academic scope; `created_by` preserves permanent creator/ownership.

When created, the Teacher must have an ACTIVE assignment to that Subject.

If the Teacher is later unassigned:
- Draft/Published/Closed Assessments remain;
- Attempts/Results remain;
- creator history remains;
- the Teacher cannot continue editing if they no longer have the required active scope;
- a new Teacher does not automatically inherit ownership.

Assessment does **not** store `program_id`; Program is derived through Subject.

## Assessment lifecycle

```text
DRAFT → PUBLISHED → CLOSED
```

- Published Assessments are immutable.
- If changes are needed after publication, create another Assessment/version.
- Closed Assessments remain historical/read-only.
- Institute Admin can view but cannot edit/publish Teacher Assessments.

## Assessment configuration — V1

Assessment includes:
- Name
- Subject
- Created By Teacher
- Duration
- Marks per Question
- Attempt Policy
- Status

Duration is mandatory.

Published Assessments are available anytime until CLOSED.

Availability windows are V2.

When duration expires:

```text
IN_PROGRESS → AUTO-SUBMIT → COMPLETED
```

## Marks / scoring — V1

All questions in one Assessment have the same marks value.

```text
Correct → full marks
Wrong → 0
Unanswered → 0
```

- No negative marking.
- Multiple Answer = all-or-nothing.
- Individual question marks are V2.
- Partial marking is V2.
- Score is immediately visible after submission.

## Assessment randomization — V1

- Random question order: YES.
- Same selected question set for all students.
- Option order: fixed.
- Different question sets per student: V2.
- Option randomization: V2.
- Stored `AssessmentQuestion.display_order` is not changed for an individual attempt.

## Assessment sections

V1 has one question sequence:

```text
Q1 → Q2 → Q3 → ... → Q100
```

Separate sections are V2.

## Student enrollment

Students enroll at Program level.

```text
STUDENT 1:N STUDENT_ENROLLMENT N:1 PROGRAM
```

A Student can enroll in multiple Programs within the same Institute.

Enrollment status:
- PENDING
- ACTIVE
- REJECTED
- INACTIVE

At most one ACTIVE enrollment should exist for a given Student + Program.

An ACTIVE Program enrollment gives access to all active Subjects in that Program.

## Student assessment access

Students with ACTIVE enrollment can access Published Assessments under their Program/Subject.

No explicit Student → Assessment assignment is required in V1.

Draft/deleted/out-of-scope Assessments are not visible.

## Attempt / Result — V1

V1 stores the attempt/result summary, not individual selected answers.

```text
STUDENT 1:N ATTEMPT N:1 ASSESSMENT
```

Attempt fields:
- student
- assessment
- attempt number
- started_at
- completed_at
- score
- total_marks
- status

Status can remain simple:
- IN_PROGRESS
- COMPLETED

Student result history is displayed using:

`completed_at DESC`

Latest result first.

Detailed per-question answer history is V2.

## Browser close / resume — V1

V1 uses a simple one-session model.

No resume functionality is required. The student is expected to complete the Assessment in one session.

Proper resume/recovery is V2.

## Teacher dashboard

Teacher can view:
- My Questions
- My Assessments
- Results for Assessments created by that Teacher

Teacher cannot view another Teacher's results unless a future permission explicitly allows it.

## Institute Admin dashboard

Institute Admin can view:
- Programs
- Subjects
- Chapters
- Teachers
- Students
- Questions
- Assessments
- Results

Institute Admin manages academic structure and student/user governance but cannot:
- edit Teacher Questions;
- delete Teacher Questions;
- edit Teacher Assessments;
- publish Teacher Assessments;
- change Results.

Principle:

> Institute Admin governs the Institute; Teacher owns academic content.

## Teacher deactivation / unassignment

When a Teacher is unassigned/deactivated:
- Questions remain.
- Draft/Published/Closed Assessments remain.
- Attempts remain.
- Results remain.
- Historical ownership remains.

A new Teacher may be assigned later but does not automatically inherit edit/ownership rights over old content.

## Conceptual V1 model

```text
INSTITUTE
   |
   +-- PROGRAM
         |
         +-- SUBJECT
               |
               +-- CHAPTER
                     |
                     +-- QUESTION
                           |
                           +-- OPTION

TEACHER
   |
   +-- TEACHER_ASSIGNMENT -- SUBJECT
   |
   +-- QUESTION
   |
   +-- ASSESSMENT -- SUBJECT
          |
          +-- ASSESSMENT_QUESTION -- QUESTION

STUDENT
   |
   +-- STUDENT_ENROLLMENT -- PROGRAM
   |
   +-- ATTEMPT -- ASSESSMENT
```

## Next implementation design phase

Before creating Django models, finalize:
1. Exact fields for each entity.
2. UUID/primary-key strategy.
3. Status choices.
4. Soft-delete fields.
5. Unique constraints.
6. Foreign-key `on_delete` behavior.
7. Indexes.
8. Database constraints vs service-layer validation.
9. AssessmentQuestion ordering/randomization implementation.
10. Attempt lifecycle/scoring implementation.

Only after approval should Django models and migrations be created.
