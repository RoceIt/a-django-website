"""Functions to create test agenda models."""
import datetime

from .models import Agenda

import address


NAME = 'name'
DESCRIPTION = 'description'
ARCHIVE_AFTER = 'archive_after'


def full_agenda_n(n):
    return {
        NAME: f'name_{n}',
        DESCRIPTION: f'description_{n}',
        ARCHIVE_AFTER: Agenda.ARCHIVE_DELTAS[0][0],
    }


AGENDA = 'agenda'
TITLE = 'title'
START_DATE = 'start_date'
START_TIME = 'start_time'
END_DATE = 'end_date'
END_TIME = 'end_time'
LOCATION = 'location'
ADDRESS = 'address'
CREATED_BY = 'created_by'


def full_current_event_n(n):
    return {
        AGENDA: Agenda.objects.create(**full_agenda_n(n)),
        TITLE: f'title_{n}',
        START_DATE: datetime.date.today() + datetime.timedelta(days=n),
        START_TIME: datetime.time(1, 0, 0),
        END_DATE: datetime.date.today() + datetime.timedelta(days=2*n),
        END_TIME: datetime.time(2, 0, 0),
        LOCATION: f'location_{n}',
        ADDRESS: address.models.Address.objects.create(
            **address.data_for_address_tests.full_address_n(n)),
        CREATED_BY: f'created_by_{n}',
    }
