# Architectural Decisions

## 2026-08-05

### English Standard

SmartExam will use American English consistently
throughout the project.

Examples:

- favorite
- color
- center
- organization
- analyze
- behavior

## Student Registration and Authentication

### Decision

Students will be allowed to self-register for SmartExam.

The mobile number will be the student's unique login identifier.

### Registration Details

A student will provide:

- Name — required
- Mobile number — required and unique
- Email — optional
- PIN — required

The mobile number will be verified using OTP during registration.

### Authentication

Students will log in using:

- Mobile number
- PIN

The PIN will be stored securely using Django's password hashing mechanism. The plain-text PIN will never be stored.

OTP will be used for mobile-number verification and will not replace the student's PIN.

### Database Identity

The student's mobile number will **not** be used as the database primary key.

The existing UUID-based `User.id` will remain the primary key.

The mobile number will have a unique constraint and will act as the student's business/login identifier.

### Future Considerations

The following are intentionally not part of V1:

- Teacher-controlled student registration
- Bulk student import
- Email-based login
- Email verification
- PIN recovery through email
- Advanced authentication/security mechanisms

## Assessment Attempts

### Decision

A student can attempt the same assessment multiple times.

Every attempt will be stored as a separate record and will not overwrite previous attempts.

### Attempt History

The system will retain the complete attempt history for each student and assessment.

The latest completed attempt will be used as the student's latest result.

### Attempt Completion

An assessment attempt can end in one of the following states:

- In Progress
- Submitted
- Time Expired
- Cancelled

When the timer reaches zero, the attempt will be automatically ended as `TIME_EXPIRED` and the result will be displayed.

### Navigation

Students can navigate backward to previous questions in V1.

Teacher-controlled navigation rules may be introduced in a future version.

### Answer Persistence

Answers will be submitted and stored only when the student submits the assessment.

Automatic answer saving/recovery is a future consideration.

### Browser/Session Behaviour

If the student refreshes the browser or attempts to continue the assessment from another browser/device, the active attempt will be cancelled.

The cancelled attempt will remain in the attempt history.

### Results

The result will be displayed immediately after submission or timeout.

Teacher-controlled result visibility will be considered in a future version.

### Teacher Access

Teachers will be able to view student assessment attempts and their results.