from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ExchangeProgram",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "university",
                    models.CharField(max_length=255, verbose_name="Університет"),
                ),
                (
                    "languages",
                    models.CharField(max_length=255, verbose_name="Мови навчання"),
                ),
                (
                    "seats",
                    models.CharField(max_length=50, verbose_name="Кількість місць"),
                ),
                ("deadline", models.DateField(verbose_name="Дедлайн подачі")),
                ("description", models.TextField(verbose_name="Опис")),
            ],
            options={
                "verbose_name": "Програма обміну",
                "verbose_name_plural": "Програми обміну",
                "ordering": ["deadline", "university"],
            },
        ),
    ]
