from django.contrib import admin
from .models import Event, Country


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'start_datetime', 'capacity', 'is_active')
    list_filter = ('location', 'is_active', 'start_datetime')
    search_fields = ('title', 'description')
