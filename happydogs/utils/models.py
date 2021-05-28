"""Utilities models."""

# Django
from django.db import models

# dependencies
from django.utils.translation import getText_lazy as _


class HappyDogsModel(models.Model):
    """HappyDogs model abstract class.

    This class should be inherited by all the classes in the project
    so they can have this common properties:
        + created (DateTimeField) DateTime at which the object was created
        + modified (DateTimeField) Last DateTime at which the object was modified.
    """

    created = models.DateTimeField(
        _('Created at'),
        auto_now_add=True,
        help_text='Datetime on which the object was created'
    )
    modified = models.DateTimeField(
        _('Modified at'),
        auto_now=True,
        help_text='Datetime at which the object was modified for the last time'
    )

    class Meta:
        """Meta option."""
        abstract = True

        get_latest_by = ['created']
        ordering = ['-created', '-modified']
