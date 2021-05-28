"""Register dogs models to admin."""

# Django
from django.contrib import admin

# Models
from .models import Dog


class DogAdmin(admin.ModelAdmin):
    """Dog admin."""
    list_display = ('first_name', 'last_name', 'created', 'modified')
    search_fields = ('first_name', 'last_name',)
    list_display_links = ('first_name', 'last_name',)


admin.site.register(Dog, DogAdmin)
