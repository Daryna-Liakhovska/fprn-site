import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Department",
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
                ("name", models.CharField(max_length=200, verbose_name="Назва")),
                (
                    "head",
                    models.CharField(max_length=200, verbose_name="Завідувач кафедри"),
                ),
            ],
            options={
                "verbose_name": "Кафедра",
                "verbose_name_plural": "Кафедри",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="HomePage",
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
                    "title",
                    models.CharField(max_length=200, verbose_name="Назва факультету"),
                ),
                (
                    "tagline",
                    models.CharField(
                        blank=True, max_length=300, verbose_name="Короткий підзаголовок"
                    ),
                ),
                ("about", models.TextField(verbose_name="Опис факультету")),
                (
                    "dean",
                    models.CharField(blank=True, max_length=200, verbose_name="Декан"),
                ),
                (
                    "address",
                    models.CharField(blank=True, max_length=300, verbose_name="Адреса"),
                ),
                (
                    "phone",
                    models.CharField(
                        blank=True, max_length=100, verbose_name="Телефон"
                    ),
                ),
                (
                    "email",
                    models.EmailField(blank=True, max_length=254, verbose_name="Email"),
                ),
            ],
            options={
                "verbose_name": "Головна сторінка",
                "verbose_name_plural": "Головна сторінка",
            },
        ),
        migrations.CreateModel(
            name="Program",
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
                ("name", models.CharField(max_length=200, verbose_name="Назва")),
                ("code", models.CharField(max_length=20, verbose_name="Код")),
                ("description", models.TextField(verbose_name="Опис")),
                (
                    "coordinator_name",
                    models.CharField(
                        max_length=200, verbose_name="Ім'я координатора набору"
                    ),
                ),
                (
                    "coordinator_contact",
                    models.CharField(
                        max_length=200, verbose_name="Контакт координатора набору"
                    ),
                ),
                (
                    "disciplines",
                    models.TextField(
                        blank=True,
                        help_text="Одна дисципліна на рядок",
                        verbose_name="Список дисциплін",
                    ),
                ),
                (
                    "department",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="programs",
                        to="faculty.department",
                        verbose_name="Випускова кафедра",
                    ),
                ),
            ],
            options={
                "verbose_name": "Спеціальність",
                "verbose_name_plural": "Спеціальності",
                "ordering": ["code", "name"],
            },
        ),
        migrations.CreateModel(
            name="Teacher",
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
                ("name", models.CharField(max_length=200, verbose_name="Ім'я")),
                ("position", models.CharField(max_length=200, verbose_name="Посада")),
                (
                    "degree",
                    models.CharField(
                        blank=True, max_length=200, verbose_name="Науковий ступінь"
                    ),
                ),
                (
                    "department",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="teachers",
                        to="faculty.department",
                        verbose_name="Кафедра",
                    ),
                ),
            ],
            options={
                "verbose_name": "Викладач",
                "verbose_name_plural": "Викладачі",
                "ordering": ["id"],
            },
        ),
    ]
