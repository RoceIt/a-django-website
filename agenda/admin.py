from django.contrib import admin
from .models import Agenda, CurrentEvent, ArchivedEvent

admin.site.register(Agenda)
admin.site.register(CurrentEvent)
admin.site.register(ArchivedEvent)
