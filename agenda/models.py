from datetime import time
import json
import logging

from django.db import models
from django.utils.translation import ugettext_lazy as _
import django.utils.timezone as tz
from address.models import Address

# ARCHIVE_DELTAS = ((tz.timedelta(days=1), _('1 day')),
#                   (tz.timedelta(days=7), _('7 days')),
#                   (tz.timedelta(days=31), _('1 month')))


# class AgendaManager(models.Manager):

#     _available_agendas = []

#     def CreateIfNotAvailable(self, agenda_name, description, archive_after):

#         if agenda_name not in self._available_agendas:
#             if not self.filter(name=agenda_name).exists():
#                 print(f"adding {agenda_name}")
#                 # self.create(name=agenda_name, description=description,
#                 #         archive_after=archive_after
#             self._available_agendas.append(agenda_name)
#         return True

MIN_TIME = time.min
MAX_TIME = time.max

logger = logging.getLogger(__name__)


class Agenda(models.Model):

    ARCHIVE_DELTAS = ((tz.timedelta(days=0), _('no archive policy')),
                      (tz.timedelta(days=1), _('1 day')),
                      (tz.timedelta(days=7), _('7 days')),
                      (tz.timedelta(days=31), _('1 month')))

    name = models.CharField(
        _('name'),
        max_length=30,
    )

    description = models.TextField(
        _('description'),
    )

    archive_after = models.DurationField(
        _('archive after'),
        choices=ARCHIVE_DELTAS,
    )

    # objects = AgendaManager()

    def __str__(self):
        return self.name


class BaseEvent(models.Model):

    agenda = models.ForeignKey(
        Agenda,
        related_name="%(app_label)s_%(class)ss",
        related_query_name="%(app_label)s_%(class)s",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    title = models.CharField(
        _('short description'),
        max_length=80,
        blank=False,
    )

    description = models.TextField(
        _('description'),
    )

    start_date = models.DateField(
        _('start date'),
        blank=True,
        null=True,
    )

    start_time = models.TimeField(
        _('start time'),
        blank=True,
        null=True,
    )

    end_date = models.DateField(
        _('end date'),
        blank=True,
        null=True,
    )

    end_time = models.TimeField(
        _('end time'),
        blank=True,
        null=True,
    )

    location = models.CharField(
        _("location"),
        max_length=80,
        blank=True,
    )

    address = models.ForeignKey(
        Address,
        related_name="%(app_label)s_%(class)ss",
        related_query_name="%(app_label)s_%(class)s",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    created_by = models.CharField(
        _('created by'),
        max_length=80,
        blank=True,
    )

    finished = models.BooleanField(
        _('finished'),
        default=False,
    )

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     try:
    #         print(self.description)
    #         self._json = json.loads(self.description)
    #     except json.decoder.JSONDecodeError:
    #         self._json = None

    class Meta:
        abstract = True

    def __str__(self):
        # show = (self.start_date, self.title)
        return(f'{self.safe_start_date}: {self.title}')

    @property
    def safe_start_date(self):
        return self.start_date or tz.now().date()

    @property
    def safe_end_date(self):
        return self.end_date or self.start_date

    @property
    def safe_start_time(self):
        return self.start_time or MIN_TIME

    @property
    def safe_end_time(self):
        if self.end_date:
            return self.end_time or MAX_TIME
        return self.end_time or self.start_time or MAX_TIME

    @property
    def safe_start_datetime(self):
        return tz.make_aware(
            tz.datetime.combine(self.safe_start_date, self.safe_start_time))

    @property
    def safe_end_datetime(self):
        return tz.make_aware(
            tz.datetime.combine(self.safe_end_date, self.safe_end_time))

    def __contains__(self, datetime):
        return self.safe_start_datetime <= datetime <= self.safe_end_datetime

    # def __getattr__(self, name):
    #     if self._json is not None and name in self._json:
    #             return self._json[name]
    #     raise AttributeError(f'{name} not in instance nor in json description')


class CurrentEvent(BaseEvent):

    def expired(self):
        return tz.now() > self.safe_end_datetime

    def archive(self):
        return tz.now() > self.safe_end_datetime + self.agenda.archive_after

    def move_to_archived_events(self):
        arch_event = ArchivedEvent(
            agenda=self.agenda,
            title=self.title,
            description=self.description,
            start_date=self.start_date,
            start_time=self.start_time,
            end_date=self.end_date,
            end_time=self.end_time,
            location=self.location,
            address=self.address,
            created_by=self.created_by)
        arch_event.save()
        self.delete()
        logger.info(f'moved {self} to archive events')


class ArchivedEvent(BaseEvent):

    pass
