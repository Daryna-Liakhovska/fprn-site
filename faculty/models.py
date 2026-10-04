from django.db import models
from django.urls import reverse


class HomePage(models.Model):
    title = models.CharField("Назва факультету", max_length=200)
    tagline = models.CharField("Короткий підзаголовок", max_length=300, blank=True)
    about = models.TextField("Опис факультету")
    dean = models.CharField("Декан", max_length=200, blank=True)
    address = models.CharField("Адреса", max_length=300, blank=True)
    phone = models.CharField("Телефон", max_length=100, blank=True)
    email = models.EmailField("Email", blank=True)

    class Meta:
        verbose_name = "Головна сторінка"
        verbose_name_plural = "Головна сторінка"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        return cls.objects.filter(pk=1).first()


class Department(models.Model):
    name = models.CharField("Назва", max_length=200)
    head = models.CharField("Завідувач кафедри", max_length=200)

    class Meta:
        verbose_name = "Кафедра"
        verbose_name_plural = "Кафедри"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("department_detail", args=[self.pk])


class Program(models.Model):
    name = models.CharField("Назва", max_length=200)
    code = models.CharField("Код", max_length=20)
    description = models.TextField("Опис")
    coordinator_name = models.CharField("Ім'я координатора набору", max_length=200)
    coordinator_contact = models.CharField("Контакт координатора набору", max_length=200)
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="programs",
        verbose_name="Випускова кафедра",
    )
    disciplines = models.TextField(
        "Список дисциплін", blank=True, help_text="Одна дисципліна на рядок"
    )

    class Meta:
        verbose_name = "Спеціальність"
        verbose_name_plural = "Спеціальності"
        ordering = ["code", "name"]

    def __str__(self):
        return f"{self.code} {self.name}"

    def get_absolute_url(self):
        return reverse("program_detail", args=[self.pk])

    @property
    def discipline_list(self):
        return [d.strip() for d in self.disciplines.splitlines() if d.strip()]


class Teacher(models.Model):
    name = models.CharField("Ім'я", max_length=200)
    position = models.CharField("Посада", max_length=200)
    degree = models.CharField("Науковий ступінь", max_length=200, blank=True)
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="teachers",
        verbose_name="Кафедра",
    )

    class Meta:
        verbose_name = "Викладач"
        verbose_name_plural = "Викладачі"
        ordering = ["id"]

    def __str__(self):
        return self.name
