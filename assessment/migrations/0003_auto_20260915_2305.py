from django.db import migrations


def populate_program(apps, schema_editor):
    Assessment = apps.get_model("assessment", "Assessment")

    for assessment in Assessment.objects.select_related(
        "subject__program"
    ).all():
        assessment.program_id = assessment.subject.program_id
        assessment.save(update_fields=["program"])


class Migration(migrations.Migration):

    dependencies = [
        ("assessment", "0002_alter_assessment_options_and_more"),
    ]

    operations = [
        migrations.RunPython(
            populate_program,
            migrations.RunPython.noop,
        ),
    ]