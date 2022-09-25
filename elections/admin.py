from django.contrib import admin

from .models import AnnouncedPuResults, Lga, Party, PollingUnit

# Register your models here.

admin.site.register(AnnouncedPuResults)
admin.site.register(PollingUnit)
admin.site.register(Party)
admin.site.register(Lga)