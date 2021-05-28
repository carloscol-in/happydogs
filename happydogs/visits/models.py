"""Visits models."""

# Django
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
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

    def __str__(self):
        """Dog name -> (start_date, end_date)"""
        return "{0} -> ({1}, {2})".format(self.dog, self.start_date, self.end_date)

    def clean(self):
        """Clean validated data.

        1. start_date should be lower or equal to end_date.
        2. The period between start_date and end_date shouldn't overlap for an existing visit appointment."""
        if self.start_date > self.end_date:
            raise ValidationError(
                _("Start date should be lower or equal to end date.")
            )

        overlap_exists = Visit.objects.filter(
            Q(dog=self.dog),
            Q(
                start_date__lte=self.start_date,
                end_date__gte=self.start_date
            ) | Q(
                start_date__lte=self.end_date,
                end_date__gte=self.end_date
            )
        ).exists()

        if overlap_exists:
            raise ValidationError(
                _("There's already a boarding visit that overlaps with the selected period.")
            )
