from django.test import TestCase
from django.urls import reverse

from .models import Department, Program


class PagesTest(TestCase):
    def test_home(self):
        r = self.client.get("/")
        self.assertContains(r, "Факультет природничих наук")
        self.assertContains(r, "Контакти")

    def test_program_list_shows_required_fields(self):
        r = self.client.get(reverse("program_list"))
        p = Program.objects.get(code="Е1")
        self.assertContains(r, p.name)
        self.assertContains(r, p.coordinator_name)
        self.assertContains(r, p.coordinator_contact)
        self.assertContains(r, p.get_absolute_url())

    def test_program_list_truncates_description_to_50_words(self):
        p = Program.objects.get(code="Е1")
        self.assertGreater(len(p.description.split()), 50)
        r = self.client.get(reverse("program_list"))
        last_word = p.description.split()[-1]
        self.assertNotContains(r, last_word)

    def test_program_detail(self):
        p = Program.objects.get(code="Е3")
        r = self.client.get(p.get_absolute_url())
        self.assertContains(r, p.discipline_list[0])
        self.assertContains(r, p.department.name)

    def test_department_list_and_detail(self):
        d = Department.objects.get(name="Кафедра хімії")
        r = self.client.get(reverse("department_list"))
        self.assertContains(r, d.head)
        self.assertContains(r, "Хімія")
        r = self.client.get(d.get_absolute_url())
        self.assertContains(r, "Голуб Олександр Андрійович")
        self.assertContains(r, "доктор технічних наук")

    def test_all_faculty_departments_listed(self):
        self.assertEqual(Department.objects.count(), 6)
        r = self.client.get(reverse("department_list"))
        self.assertContains(r, "Кафедра лабораторної діагностики біологічних систем")
        self.assertContains(r, "Кафедра фізичного виховання")

    def test_404(self):
        self.assertEqual(self.client.get("/departments/999/").status_code, 404)
        self.assertEqual(self.client.get("/programs/999/").status_code, 404)

    def test_header_on_every_page(self):
        for url in ["/", "/programs/", "/departments/"]:
            r = self.client.get(url)
            self.assertContains(r, 'href="/departments/"')
            self.assertContains(r, 'href="/programs/"')
