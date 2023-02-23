import datetime

from django.test import TestCase

from .models import Agenda, CurrentEvent
from . import data_for_agenda_tests


class TestAgendaTestData(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.agenda1 = Agenda.objects.create(
            **data_for_agenda_tests.full_agenda_n(1)
        )
        cls.current_event2 = CurrentEvent.objects.create(
            **data_for_agenda_tests.full_current_event_n(2)
        )

    def test_full_agenda_n_ok(self):
        self.assertEqual(self.agenda1.name, 'name_1')
        self.assertEqual(self.agenda1.description, 'description_1')
        self.assertEqual(
            self.agenda1.archive_after, Agenda.ARCHIVE_DELTAS[0][0])

    def test_full_event_n_ok(self):
        self.assertEqual(
            self.current_event2.agenda.name,
            Agenda(**data_for_agenda_tests.full_agenda_n(2)).name)
        self.assertEqual(
            self.current_event2.start_date,
            datetime.date.today() + datetime.timedelta(days=2),
        )
        self.assertEqual(self.current_event2.start_time,
                         datetime.time(1, 0, 0))
        self.assertEqual(
            self.current_event2.end_date,
            datetime.date.today() + datetime.timedelta(days=4))
        self.assertEqual(self.current_event2.end_time,
                         datetime.time(2,0,0))
        self.assertEqual(self.current_event2.location, 'location_2')
        self.assertEqual(self.current_event2.address.address_name,
                         'address_name_2')
        self.assertEqual(self.current_event2.created_by,
                         'created_by_2')
