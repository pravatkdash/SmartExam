# SmartExam — V1 Implementation Checklist

**V1 status: FROZEN**

This checklist tracks implementation progress only.  
Business/architecture decisions are maintained separately in:

`SmartExam_V1_Architecture_Design_Notes.md`

## Status legend

- ✅ DONE — implemented and manually verified
- 🟡 PARTIAL — some implementation exists, but V1 work remains
- ⬜ TODO — not implemented yet
- 🚫 V2 — intentionally excluded from V1

---

# 1. Project Foundation

| Item | Status | Notes |
|---|---|---|
| Django project setup | ✅ DONE | Working |
| Apps: accounts | ✅ DONE | Existing |
| Apps: assessment | ✅ DONE | Existing |
| Apps: subjects | ✅ DONE | Existing |
| Apps: questions | ✅ DONE | Existing |
| Apps: common | ✅ DONE | Existing |
| SQLite development database | ✅ DONE | Development/test data available |
| `python manage.py check` | ✅ DONE | Passed |

# 2. User & Authentication

| Item | Status | Notes |
|---|---|---|
| Custom User model | ✅ DONE | Email-based login |
| UUID user ID | ✅ DONE | Existing |
| Unique email | ✅ DONE | Existing |
| Unique mobile number | ✅ DONE | Existing |
| User types | 🟡 PARTIAL | Current `ADMIN`; V1 design calls for Institute Admin |
| Student registration | ✅ DONE | Tested |
| Student login | ✅ DONE | Tested |
| Student logout | ✅ DONE | Tested |
| Student dashboard | ✅ DONE | Tested |
| Teacher registration/approval | ⬜ TODO | V1 organization layer |
| Institute Admin | ⬜ TODO | V1 organization layer |

# 3. Exam / Subject / Chapter / Question

| Item | Status | Notes |
|---|---|---|
| Exam | ✅ DONE | Existing |
| Subject | ✅ DONE | Existing |
| Chapter | ✅ DONE | Existing |
| Question | ✅ DONE | Existing |
| Question options | ✅ DONE | Existing |
| Display order | ✅ DONE | Existing |
| Single-answer questions | ✅ DONE | Working |
| Multiple-answer questions | ✅ DONE | Working |
| Difficulty | ✅ DONE | Existing |
| Marks | ✅ DONE | Existing |
| Negative marks | ✅ DONE | Existing |
| Explanation | ✅ DONE | Existing |
| Question validation | ✅ DONE | Existing/admin-tested |

# 4. Assessment

| Item | Status | Notes |
|---|---|---|
| Assessment model | ✅ DONE | Existing |
| Assessment-question mapping | ✅ DONE | Existing |
| Assessment publishing | ✅ DONE | Tested |
| Published assessment listing | ✅ DONE | Tested |
| Start assessment | ✅ DONE | Tested |
| Attempt creation | ✅ DONE | Tested |
| Attempt question snapshot | ✅ DONE | Tested |
| Question ordering | ✅ DONE | Tested |
| Resume existing in-progress attempt | ✅ DONE | Existing behavior |
| Previous navigation | ✅ DONE | Tested |
| Next navigation | ✅ DONE | Tested |
| Answer selection | ✅ DONE | Tested |
| Submit assessment | ✅ DONE | Tested |
| Result redirect | ✅ DONE | Tested |

# 5. Results / Historical Records

| Item | Status | Notes |
|---|---|---|
| AssessmentAttempt status | ✅ DONE | IN_PROGRESS/SUBMITTED/EXPIRED |
| Score | ✅ DONE | Implemented |
| Submitted timestamp | ✅ DONE | Implemented |
| StudentAnswer | ✅ DONE | Existing |
| Selected options | ✅ DONE | Existing |
| Result page | ✅ DONE | Fixed and working |
| Historical submitted attempt | ✅ DONE | Verified |
| Teacher/admin result visibility | 🟡 PARTIAL | Current basic foundation; institute permissions remain |
| Result preservation after deactivation | ⬜ TODO | Depends on organization/user lifecycle |

# 6. Student Experience

| Item | Status | Notes |
|---|---|---|
| Student dashboard | ✅ DONE | Tested |
| Available assessments | ✅ DONE | Existing |
| Start assessment button | ✅ DONE | Tested |
| Assessment UI | ✅ DONE | Looks good |
| Previous/Next | ✅ DONE | Tested |
| Submit Exam | ✅ DONE | Tested |
| Result display | ✅ DONE | Tested |
| Logout | ✅ DONE | Tested |
| Institute enrollment | ⬜ TODO | V1 organization layer |
| Academic level | ⬜ TODO | V1 eligibility layer |
| Exam/program preference | ⬜ TODO | V1 eligibility layer |

# 7. Institute Layer

| Item | Status | Notes |
|---|---|---|
| Institute model | ⬜ TODO | V1 |
| Institute registration | ⬜ TODO | V1 |
| Institute communication email | ⬜ TODO | V1 |
| Super Admin institute approval | ⬜ TODO | V1 |
| Institute Admin role | ⬜ TODO | V1 |
| Institute Admin dashboard | ⬜ TODO | V1 |
| Institute-wide data isolation | ⬜ TODO | V1 |

# 8. Teacher Management

| Item | Status | Notes |
|---|---|---|
| Teacher belongs to one institute | ⬜ TODO | V1 |
| Teacher registration request | ⬜ TODO | V1 |
| Institute Admin teacher approval | ⬜ TODO | V1 |
| Teacher management by Institute Admin | ⬜ TODO | V1 |
| Teacher creates content | 🟡 PARTIAL | Existing content foundation |
| Teacher creates assessments | 🟡 PARTIAL | Existing assessment foundation |
| Teacher sees own assessment results | 🟡 PARTIAL | Authorization boundary remains |

# 9. Student Enrollment

| Item | Status | Notes |
|---|---|---|
| Direct SmartExam student | 🟡 PARTIAL | Existing student registration |
| Student selects institute | ⬜ TODO | V1 |
| Enrollment request | ⬜ TODO | V1 |
| Institute Admin approves enrollment | ⬜ TODO | V1 |
| Institute Admin directly adds student | ⬜ TODO | V1 |
| Enrollment status | ⬜ TODO | V1 |
| Academic level | ⬜ TODO | V1 |
| Program/exam association | ⬜ TODO | V1 |

# 10. Assessment Eligibility

| Item | Status | Notes |
|---|---|---|
| Institute ownership/context | ⬜ TODO | V1 |
| Assessment creator | ⬜ TODO | V1 authorization |
| Target academic level | ⬜ TODO | V1 |
| Multiple target academic levels | ⬜ TODO | V1 |
| Program/exam targeting | ⬜ TODO | V1 |
| Class 8 vs Class 9 isolation | ⬜ TODO | V1 |
| Institute A vs Institute B isolation | ⬜ TODO | V1 |

# 11. Soft Deactivation

| Item | Status | Notes |
|---|---|---|
| User deactivation strategy | 🟡 PARTIAL | Django User already has `is_active`; full V1 workflow remains |
| Teacher deactivation | ⬜ TODO | V1 |
| Student deactivation | ⬜ TODO | V1 |
| Preserve historical attempts/results | 🟡 PARTIAL | Data model supports history; lifecycle rules remain |
| Avoid destructive deletion | ⬜ TODO | V1 policy/workflow |

# 12. Testing

| Item | Status | Notes |
|---|---|---|
| Django system check | ✅ DONE | Passed |
| Manual student registration test | ✅ DONE | Tested |
| Manual login test | ✅ DONE | Tested |
| Manual assessment start | ✅ DONE | Tested |
| Manual answer selection | ✅ DONE | Tested |
| Manual previous/next | ✅ DONE | Tested |
| Manual submit | ✅ DONE | Tested |
| Manual result verification | ✅ DONE | Tested |
| Automated model tests | ⬜ TODO | Very limited currently |
| Automated service tests | ⬜ TODO | Very limited currently |
| Automated view tests | ⬜ TODO | Very limited currently |
| Permission tests | ⬜ TODO | Important when institute layer is implemented |

# 13. Documentation

| Item | Status | Notes |
|---|---|---|
| V1 architecture/design notes | ✅ DONE | Frozen source of truth |
| V1 implementation checklist | ✅ DONE | This file |
| Old roadmap updated | ⬜ TODO | Existing roadmap is outdated |
| V2 ideas document | 🚫 V2 | Do not expand V1 unnecessarily |

---

# 14. Current Position

The core **Student → Assessment → Attempt → Submit → Result** flow is working.

The major remaining V1 development area is the organization and eligibility layer:

```text
Super Admin
     |
  Institute
     |
Institute Admin
   /       Teacher   Student
   |         |
Content   Enrollment
   |         |
Assessment  Academic Level
   |
Eligibility
   |
Attempt
   |
Result
```

## Important rule

Do not start implementing a new feature just because it sounds useful.

For every new request:

1. Compare it with `SmartExam_V1_Architecture_Design_Notes.md`.
2. If required by V1 → implement.
3. If not required by V1 → discuss and mark it V2.
4. Do not change the frozen V1 architecture for a V2 enhancement.

---

# 15. Next Development Target

Before coding the next feature:

**Review and confirm the Institute / Institute Admin / Teacher / Student data model and permission boundaries against the frozen V1 design.**

Then implement in small, testable steps.

No large uncontrolled rewrite.
