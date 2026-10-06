import re

from django.db import migrations

NUMBER = re.compile(r"\d+")
UPPER_BOUND = re.compile(r"^\s*до\b", re.IGNORECASE)


def forwards(apps, schema_editor):
    ExchangeProgram = apps.get_model("exchange", "ExchangeProgram")
    for program in ExchangeProgram.objects.all():
        match = NUMBER.search(program.seats or "")
        if match is None:
            raise ValueError(
                f"Не вдалося розпізнати кількість місць {program.seats!r} "
                f"для програми id={program.pk} ({program.university})"
            )
        program.seats_number = int(match.group())
        program.seats_is_upper_bound = bool(UPPER_BOUND.match(program.seats))
        program.save(update_fields=["seats_number", "seats_is_upper_bound"])


def backwards(apps, schema_editor):
    ExchangeProgram = apps.get_model("exchange", "ExchangeProgram")
    for program in ExchangeProgram.objects.all():
        if program.seats_number is None:
            continue
        prefix = "до " if program.seats_is_upper_bound else ""
        program.seats = f"{prefix}{program.seats_number}"
        program.save(update_fields=["seats"])


class Migration(migrations.Migration):
    dependencies = [
        ("exchange", "0005_seats_number_fields"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
