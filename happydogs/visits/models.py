"""Visits models."""

# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Utilities
from utils.models import HappyDogsModel


class Visit(HappyDogsModel):
    """Visit model."""

    start_date = models.DateField(
        _('Start date'),
    )
    end_date = models.DateField(
        _('End date'),
        help_text='Date at which the boarding visit finishes'
    )

    dog = models.ForeignKey(
        'dogs.Dog',
        on_delete=models.CASCADE,
    )

    class Meta:
        """Meta option."""
        constraints = [
            models.UniqueConstraint(
                fields=['start_date', 'end_date', 'dog'],
                name='Start date and end date should be unique for each dog',
            ),
        ]

    def clean(self):
        """Don't allow overlapping start_date and end_date periods."""
