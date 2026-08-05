# Django ORM Relationship Traversal

Think in Python first.

Python:
question.chapter.subject.exam.name

Django ORM:
chapter__subject__exam__name

Rule:
Replace "." with "__".

Examples:

AssessmentAdmin
---------------
exam__name

QuestionAdmin
-------------
chapter__subject__exam__name

AssessmentQuestionAdmin
-----------------------
assessment__name
question__question_text