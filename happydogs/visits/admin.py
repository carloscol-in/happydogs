"""Visits admin."""

# Django
from django.contrib import admin

# Models
from .models import Visit


class VisitAdmin(admin.ModelAdmin):
    """Visit admin."""
    list_display = ('dog', 'start_date', 'end_date',)
    list_display_links = ('start_date', 'end_date',)
    search_fields = ('dog',)

    fieldsets = (
        ('Dog', {
            'fields': (
                ('dog'),
            )
        }),
        ('Boarding Visit', {
            'fields': (
                ('start_date', 'end_date'),
            )
        })
    )


admin.site.register(Visit, VisitAdmin)
