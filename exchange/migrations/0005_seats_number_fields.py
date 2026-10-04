from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("exchange", "0004_split_university_country"),
    ]

    operations = [
        migrations.AddField(
            model_name="exchangeprogram",
            name="seats_number",
            field=models.PositiveSmallIntegerField(null=True, verbose_name="Кількість місць"),
        ),
        migrations.AddField(
            model_name="exchangeprogram",
            name="seats_is_upper_bound",
            field=models.BooleanField(
                default=False,
                verbose_name="Місць «до N»",
                help_text="Позначте, якщо вказано максимальну кількість місць (наприклад, «до 4»).",
            ),
        ),
    ]
