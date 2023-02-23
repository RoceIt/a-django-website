import json

from django.utils.timezone import timedelta

from agenda.models import Agenda

######
#
# Event keywords
#


EVENT_KW_ASSEMBLY_POINT_PROMOTION = 'APP'

#####
#
# filter test functions
#


def is_assembly_point_promotion(event):
    return event.keyword == EVENT_KW_ASSEMBLY_POINT_PROMOTION

######
#
# Agenda's
#


DELIVERY_AGENDA_NAME = 'dj.app.orders.delivery'
DELIVERY_AGENDA_DESCRIPTION = (
    'Agenda automatically created by the orders module to '
    'create and manage orders as agenda events.'
)
DELIVERY_AGENDA_ARCHIVE_AFTER = timedelta(days=1)


class delivery_agenda():

    def __enter__(self):
        return Agenda.objects.get_or_create(
            name=DELIVERY_AGENDA_NAME,
            defaults={
                'description': DELIVERY_AGENDA_DESCRIPTION,
                'archive_after': DELIVERY_AGENDA_ARCHIVE_AFTER,
            }
        )[0]

    def __exit__(self, exc_type, exc_value, traceback):
        return False


PRICING_AGENDA_NAME = 'dj.app.orders.pricing'
PRICING_AGENDA_DESCRIPTION = (
    'Agenda automatically created by the orders module to '
    'create and manage price setting events.'
)
PRICING_AGENDA_ARCHIVE_AFTER = timedelta(days=1)


class pricing_agenda():

    def __enter__(self):
        return Agenda.objects.get_or_create(
            name=PRICING_AGENDA_NAME,
            defaults={
                'description': PRICING_AGENDA_DESCRIPTION,
                'archive_after': DELIVERY_AGENDA_ARCHIVE_AFTER,
            }
        )[0]

    def __exit__(self, exc_type, exc_value, traceback):
        return False


KEYWORD_AGENDA_NAME = 'dj.app.orders.keywords'
KEYWORD_AGENDA_DESCRIPTION = (
    'Agenda automatically created by the orders module to '
    'create and manage keyword setting events.'
)
KEYWORD_AGENDA_ARCHIVE_AFTER = timedelta(days=0)


class keyword_agenda():

    def __enter__(self):
        return Agenda.objects.get_or_create(
            name=KEYWORD_AGENDA_NAME,
            defaults={
                'description': KEYWORD_AGENDA_DESCRIPTION,
                'archive_after': KEYWORD_AGENDA_ARCHIVE_AFTER,
            }
        )[0]

    def __exit__(self, exc_type, exc_value, traceback):
        return False
