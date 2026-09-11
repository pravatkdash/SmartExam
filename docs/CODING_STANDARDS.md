# SmartExam Coding Standards

SmartExam
│
├── accounts/
│   └── User, login, authentication
│
├── subjects/
│   └── Program, Subject, Chapter
│
├── institute_admin/
│   └── Institute Admin functionality
│
├── questions/
│   └── Questions
│
└── assessments/
    └── Assessments

## Naming
- Use American English
- Use singular model names
- Use meaningful variable names

## Django
- Use related_name for all ForeignKeys
- Prefer CharField over TextField for titles/names
- Avoid null=True for CharField/TextField
- Add __str__() to every model
- Add Meta ordering where appropriate

## Git
- One feature per branch
- One logical commit

Database/model behavior → models.py
Teacher form/formset validation → teacher_forms.py
Question business logic → question_service.py
HTTP request/page handling → views.py
Admin-specific behavior → admin.py / admin_forms.py


questions/
├── models.py
├── question_service.py    ← question business rules / locking
├── teacher_forms.py       ← teacher forms
├── views.py               ← teacher request handling
└── ...