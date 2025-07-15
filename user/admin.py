from django.contrib import admin
from .models import Schedule


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ("id", "date", "status", "description")
    list_filter = ("status", "date")
    search_fields = ("id", "description")
    ordering = ("-date",)
