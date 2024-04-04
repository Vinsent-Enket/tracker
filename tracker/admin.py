from django.contrib import admin

# Register your models here.
from tracker.models import Addiction, NiceAddiction, Periodicity

admin.site.register(Addiction)

admin.site.register(NiceAddiction)

admin.site.register(Periodicity)