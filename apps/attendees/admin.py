from django.contrib import admin
from .models import Attendee


@admin.register(Attendee)
class AttendeeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'date_of_birth')
    search_fields = ('first_name', 'last_name', 'email')
