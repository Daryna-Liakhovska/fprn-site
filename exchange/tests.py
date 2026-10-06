import datetime
from unittest import mock

from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.test import TestCase, TransactionTestCase

from .models import ExchangeProgram

EXPECTED = {
    "Uniwersytet Warszawski": ("Польща", 5, False, datetime.date(2026, 11, 15)),
    "KU Leuven": ("Бельгія", 2, False, datetime.date(2026, 12, 1)),
    "Vilnius University": ("Литва", 4, True, datetime.date(2026, 10, 20)),
    "Uniwersytet Jagielloński": ("Польща", 3, False, datetime.date(2026, 11, 15)),
    "University of Tartu": ("Естонія", 2, False, datetime.date(2027, 1, 10)),
    "Masaryk University": ("Чехія", 1, False, datetime.date(2026, 9, 30)),
}


class SeededDataTest(TestCase):
    def test_programs_exist_after_migrate(self):
        self.assertEqual(ExchangeProgram.objects.count(), 6)

    def test_university_and_country_split(self):
        for name, (country, seats, upper, deadline) in EXPECTED.items():
            p = ExchangeProgram.objects.get(university=name)
            self.assertEqual(p.country, country)
            self.assertEqual(p.seats, seats)
            self.assertEqual(p.seats_is_upper_bound, upper)
            self.assertEqual(p.deadline, deadline)

    def test_languages_kept_as_is(self):
        self.assertEqual(ExchangeProgram.objects.get(university="KU Leuven").languages, "English")

    def test_seats_display(self):
        self.assertEqual(ExchangeProgram.objects.get(university="Vilnius University").seats_display, "до 4")


class StatusTest(TestCase):
    def _at(self, date):
        return mock.patch("django.utils.timezone.localdate", return_value=date)

    def test_status_by_deadline(self):
        p = ExchangeProgram.objects.get(university="Vilnius University")
        with self._at(datetime.date(2026, 10, 20)):
            self.assertTrue(p.is_open)
        with self._at(datetime.date(2026, 10, 21)):
            self.assertFalse(p.is_open)

    def test_page(self):
        with self._at(datetime.date(2026, 10, 4)):
            r = self.client.get("/exchange/")
        self.assertContains(r, "Прийом триває", count=5)
        self.assertContains(r, "Прийом завершено", count=1)
        self.assertContains(r, 'href="/exchange/"')

    def test_country_filter(self):
        r = self.client.get("/exchange/", {"country": "Польща"})
        self.assertContains(r, "Uniwersytet Warszawski")
        self.assertContains(r, "Uniwersytet Jagielloński")
        self.assertNotContains(r, "KU Leuven")


class RollbackTest(TransactionTestCase):
    serialized_rollback = True

    def _migrate(self, target):
        executor = MigrationExecutor(connection)
        executor.loader.build_graph()
        executor.migrate([target])

    def test_full_rollback_and_reapply(self):
        self._migrate(("exchange", None))
        self.assertNotIn("exchange_exchangeprogram", connection.introspection.table_names())
        self._migrate(("exchange", "0007_replace_seats_with_number"))
        self.assertEqual(ExchangeProgram.objects.count(), 6)

    def test_partial_rollback_keeps_values(self):
        self._migrate(("exchange", "0003_exchangeprogram_country"))
        with connection.cursor() as c:
            c.execute("SELECT university, seats FROM exchange_exchangeprogram ORDER BY id")
            rows = c.fetchall()
        self.assertIn(("Vilnius University, Литва", "до 4"), rows)
        self.assertIn(("KU Leuven, Бельгія", "2"), rows)
        self._migrate(("exchange", "0007_replace_seats_with_number"))
        self.assertEqual(ExchangeProgram.objects.get(university="KU Leuven").country, "Бельгія")
