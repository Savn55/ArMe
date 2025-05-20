from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'state', 'latitude', 'longitude')
    search_fields = ('name', 'description', 'city', 'state')
    list_filter = ('category', 'state', 'city')