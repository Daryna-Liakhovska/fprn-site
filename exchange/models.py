from django.db import models
from django.utils import timezone


class ExchangeProgram(models.Model):
    university = models.CharField("Університет", max_length=255)
    country = models.CharField("Країна", max_length=100, blank=True, default="")
    languages = models.CharField("Мови навчання", max_length=255)
    seats = models.PositiveSmallIntegerField("Кількість місць")
    seats_is_upper_bound = models.BooleanField(
        "Місць «до N»",
        default=False,
        help_text="Позначте, якщо вказано максимальну кількість місць (наприклад, «до 4»).",
    )
    deadline = models.DateField("Дедлайн подачі")
    description = models.TextField("Опис")

    class Meta:
        verbose_name = "Програма обміну"
        verbose_name_plural = "Програми обміну"
        ordering = ["deadline", "university"]

    def __str__(self):
        return f"{self.university}, {self.country}" if self.country else self.university

    @property
    def seats_display(self):
        return f"до {self.seats}" if self.seats_is_upper_bound else str(self.seats)

    @property
    def is_open(self):
        return timezone.localdate() <= self.deadline
