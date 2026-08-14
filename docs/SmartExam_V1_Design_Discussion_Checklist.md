# SmartExam V1 — Design Discussion Checklist

We can use this as our checklist for the SmartExam V1 design discussions.

---

## 🟢 Phase 1 — Foundation

- What entities do we need?
- What is the relationship between each entity?
- What belongs to Institute vs Program vs Subject?
- Which entities can be reused?
- Which entities should be soft-deleted?

---

## 🟢 Phase 2 — Users & Permissions

- What can Super Admin do?
- What can Institute Admin do?
- What can Teacher do?
- What can Student do?
- Can one person have multiple roles?
- What happens when a Teacher/Admin leaves?
- Who can see whose data?

---

## 🟢 Phase 3 — Academic Structure

- Institute → Program → Subject → Chapter — is this hierarchy correct?
- Can Subjects be shared between Programs?
- Can Chapters be shared?
- Can Teachers teach multiple Subjects?
- Can multiple Teachers teach the same Subject?
- What happens when Teacher assignment changes?

---

## 🟢 Phase 4 — Questions

- What question types do we support?
- How many options are required?
- How do we validate correct answers?
- Can Teachers reuse Questions?
- Can another Teacher reuse a Question?
- When can a Question be edited?
- When can a Question be deleted?
- What happens when a Question is already used in a Published Assessment?
- Should Teacher get a review/confirmation before saving?

---

## 🟢 Phase 5 — Assessment

- Who can create an Assessment?
- What fields are required?
- What is Draft vs Published vs Closed?
- Can a Published Assessment be edited?
- Can Questions be added/removed after publishing?
- How many marks per Question?
- Negative marking?
- Assessment duration?
- What happens when duration expires?
- Can students attempt multiple times?
- Should Questions be randomized?
- Should Options be randomized?
- Can different students get different Question sets?

---

## 🟢 Phase 6 — Student

- How does Student registration work?
- Who approves a Student?
- Can Student belong to multiple Programs?
- What Assessments can a Student see?
- What happens when enrollment becomes inactive?
- What happens if Student leaves/closes the browser?

---

## 🟢 Phase 7 — Results

- What exactly do we store for an Attempt?
- Do we store individual answers?
- How is the score calculated?
- When is the result visible?
- Can Students see previous attempts?
- Can Teachers see results?
- Can Institute Admin see results?
- What happens to historical results if Questions change?

---

## 🟢 Phase 8 — Data Integrity

- What should be impossible at database level?
- What should be validated in the service layer?
- What should happen if someone tries to bypass the UI?
- What happens when referenced data becomes inactive?
- Which relationships need unique constraints?
- Which operations need transactions?

---

## 🟢 Phase 9 — V1 vs V2

- Is this required for V1?
- If not, can we safely defer it?
- Does adding it now significantly increase complexity?
- Will delaying it make V2 difficult?
- Are we accidentally expanding V1?

---

## Discussion Process

For each question, classify the decision as:

- **V1 — MUST HAVE**
- **V1 — NICE TO HAVE**
- **V2 — DEFER**
- **NOT NEEDED**

Once a decision is agreed, mark it as **🔒 V1 LOCKED**.

This checklist is intended to keep the design discussions focused, avoid unnecessary scope expansion, and ensure that important architectural decisions are made before implementation.
