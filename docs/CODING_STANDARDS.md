# SmartExam Coding Standards

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