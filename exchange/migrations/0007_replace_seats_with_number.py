from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("exchange", "0006_fill_seats_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="exchangeprogram",
            name="seats",
            field=models.CharField(default="", max_length=50, verbose_name="Кількість місць"),
        ),
        migrations.RemoveField(
            model_name="exchangeprogram",
            name="seats",
        ),
        migrations.RenameField(
            model_name="exchangeprogram",
            old_name="seats_number",
            new_name="seats",
        ),
        migrations.AlterField(
            model_name="exchangeprogram",
            name="seats",
            field=models.PositiveSmallIntegerField(verbose_name="Кількість місць"),
        ),
    ]
