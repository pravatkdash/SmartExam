# SmartExam: V1 End-to-End Workflow Test Plan

This document outlines the clean V1 end-to-end testing procedure for SmartExam, following a real user journey across all roles and system capabilities.

---

## 1. Super Admin Phase

* **System Authentication:** Login to SmartExam Admin portal.
* **Institute Setup:** Create new Institute entity.
* **User Management:** Create Institute Admin credentials for the newly created institute.

---

## 2. Institute Admin Phase

* **System Authentication:** Login through `/institute/login`.
* **Staff Onboarding:** Create Teacher account.
* **Academic Hierarchy Setup:**
  * Create Program.
  * Create Subject.
  * Create Chapters under the defined Subject.

---

## 3. Teacher Phase

* **System Authentication:** Login to the Teacher portal.
* **Verification:** Verify assigned Subject and Chapter access.
* **Question Bank Operations:**
  * Add new questions.
  * Edit existing questions.
  * Verify full question list and individual item details.

---

## 4. Assessment Phase

* **Creation:** Create a new assessment.
* **Configuration:** Add and select questions from the question bank.
* **Deployment:** Publish assessment for students.

---

## 5. Student Phase

* **System Access:** Register or login to the Student portal.
* **Assessment Discovery:** See available published assessments.
* **Execution:**
  * Start exam.
  * Answer questions.
  * Submit exam.

---

## 6. Result & Analytics Phase

* **Score Verification:** Confirm overall exam score.
* **Marks Calculation:** Verify correct addition of positive marks.
* **Penalty Logic:** Validate negative marking calculations.
* **Data Integrity:** Verify overall attempt history and result analytics.