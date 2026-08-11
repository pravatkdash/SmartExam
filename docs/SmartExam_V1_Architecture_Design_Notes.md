# SmartExam — V1 Architecture & Design Notes

## 1. V1 Scope Freeze

**Status: FROZEN**

SmartExam V1 is now the baseline implementation.

- No feature or architecture changes should be introduced into V1.
- New ideas must first be classified as either required for V1 or a V2 enhancement.
- New functionality that is not required for the agreed V1 design should be documented as **V2** and not implemented in V1.
- Finish a stable V1 before expanding the product.

## 2. Platform Hierarchy

```text
SUPER ADMIN
    |
    +---- Institute
             |
             +---- Institute Admin
             |
             +---- Teachers
             |
             +---- Students
```

### Super Admin
Platform-level administrator with platform-wide visibility and institute management/approval.

### Institute
Organization/workspace inside SmartExam.

Institute registration includes:
- Institute name
- Institute communication email
- Institute phone
- Institute address
- Other required institute information

The registered institute email is the official communication email for teacher approval/rejection, student-related institute notifications, and important institute communication.

## 3. Institute Admin

Institute Admin manages the institute workspace and is effectively the management superset of Teacher capabilities at institute scope.

Can:
- Add/edit/deactivate/reactivate/remove teachers
- Approve/reject teacher requests
- Add/edit/deactivate/reactivate/remove students
- Approve/reject student membership requests
- Manage enrollments
- Manage institute-wide content
- Create/manage/publish/unpublish assessments
- View institute-wide assessment results

Soft deactivation is preferred over destructive deletion.

## But importantly, Institute Admin is a User, while Institute is an organization/entity.
## 4. Teacher

Teacher is primarily a **content creator**.

Rules:
- Exactly one institute per teacher in V1
- Email unique
- Mobile number unique
- Teacher cannot belong to multiple institutes in V1

Can:
- Create/manage subjects, chapters and questions
- Create/publish/manage assessments
- View results of own assessments

Cannot:
- Add/manage students
- Approve students
- Manage institute membership
- Access another institute's data
- Access another teacher's private content

## 5. Teacher Registration

```text
Teacher registers
      |
Select Institute
      |
Request = PENDING
      |
Institute communication email
      |
Institute Admin
   /          \
APPROVE      REJECT
   |
Teacher becomes active
```

Selecting an institute does not automatically activate the teacher.

## 6. Student Registration

Students have two V1 onboarding paths.

### A. Direct registration

Student can register without an institute and use SmartExam platform/public assessments according to eligibility.

### B. Registration with institute

Student selects an institute, creating a membership/enrollment request.

```text
Student registers
      |
Select Institute
      |
Enrollment = PENDING
      |
Institute Admin
   /          \
APPROVE      REJECT
   |
Student enrolled
```

Selecting an institute does not automatically grant private institute access.

## 7. Institute Admin Adds Students

Institute Admin can directly create/add students and assign their enrollment.

This supports institutes that already have a student list.

Teacher does **not** add students.

## 8. Enrollment

Enrollment is the relationship between a student and an institute and conceptually contains:
- Student
- Institute
- Academic Level
- Program/Exam
- Enrollment status
- Relevant dates

This supports academic progression and eligibility without putting everything directly on the User record.

## 9. Academic Level

Academic level is separate from Exam/Program.

Examples:
- Class 8
- Class 9
- Class 10
- Class 11
- Class 12

Academic levels should be centrally defined rather than free-text.

## 10. Exam / Program

Examples:
- NEET
- Odisha SSB
- JEE
- Mathematics
- Other programs

Academic Level and Exam/Program are separate eligibility concepts.

## 11. Class 8 / Class 9 Access

If an assessment targets Class 8, Class 9 students must not access it, and vice versa.

An assessment may target multiple academic levels, e.g. Class 8 + Class 9.

## 12. Assessment Visibility

- Teacher: own assessments and their results
- Institute Admin: all assessments/results belonging to the institute
- Super Admin: platform-wide visibility
- Teacher cannot see another institute's data

## 13. Historical Results

Submitted assessment attempts are historical records.

They include concepts such as:
- AssessmentAttempt
- Attempt Questions
- Student Answers
- Score
- Submitted timestamp
- Status

Historical records must survive user deactivation or institute membership changes.

## 14. Soft Delete / Deactivation

V1 prefers soft deletion/deactivation for important user records.

Example:

```text
ACTIVE -> INACTIVE
```

Do not hard-delete users when that would destroy historical assessment/result records.

## 15. Existing Content Structure

Keep the current V1 structure:

```text
Subject
   |
Chapter
   |
Question
   |
Option
```

Existing question functionality remains part of V1.

## 16. Existing Assessment Attempt Structure

```text
Student
   |
AssessmentAttempt
   |
+-- Attempt Questions
+-- Student Answers
+-- Score
+-- Submitted At
+-- Status
```

Current attempt statuses:
- IN_PROGRESS
- SUBMITTED
- EXPIRED

## 17. Role Matrix

| Capability | Super Admin | Institute Admin | Teacher | Student |
|---|---:|---:|---:|---:|
| Manage institutes | YES | NO | NO | NO |
| Approve institutes | YES | NO | NO | NO |
| Manage teachers | YES | YES | NO | NO |
| Approve teachers | YES | YES | NO | NO |
| Add students | YES | YES | NO | NO |
| Approve students | YES | YES | NO | NO |
| Manage enrollments | YES | YES | NO | NO |
| Create questions | YES | YES | YES | NO |
| Manage own questions | YES | YES | YES | NO |
| Manage institute questions | YES | YES | NO | NO |
| Create assessments | YES | YES | YES | NO |
| Manage own assessments | YES | YES | YES | NO |
| Manage institute assessments | YES | YES | NO | NO |
| View own results | YES | YES | YES | YES |
| View institute-wide results | YES | YES | NO | NO |
| Take assessments | Optional | Optional | Optional | YES |

## 18. Demo / Platform Institute

Initially there may be no real institutes or teachers.

Use a default/dummy organization such as:

**SmartExam Platform Institute**

This can support demo/public/platform assessments and platform-managed content.

## 19. V1 Design Principles

1. Institute isolation.
2. Teacher = content creator.
3. Institute Admin = people/organization manager.
4. Students can be direct SmartExam users or institute-enrolled users.
5. Institute membership requests require approval.
6. Academic level controls assessment eligibility.
7. Submitted results are historical records.
8. Soft deletion/deactivation is preferred.
9. V1 remains stable and focused.

## 20. V2 Rule

During V1 development:

1. Discuss every new idea.
2. Check whether it is required by the frozen V1 design.
3. If it is a new capability/enhancement, mark it **V2**.
4. Do not modify V1 for that enhancement.

Potential V2 examples:
- Multiple institute memberships for one student
- Multiple institute memberships for one teacher
- Advanced institute roles
- Multiple complex institute-admin roles
- Advanced audit logs
- Advanced invitations
- Extended academic-year history
- Complex organization hierarchies
- Advanced analytics/reporting

## 21. Current Decision

**SmartExam V1 architecture is frozen.**

Before changing models, services, views, or permissions, compare the request against this document.

If it conflicts with the frozen V1 design and is not required to complete V1:

**Discuss -> classify as V2 -> do not implement in V1.**
