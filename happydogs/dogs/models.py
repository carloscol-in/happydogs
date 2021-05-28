"""Dogs models."""

from django.db import models
from django.utils.translation import gettext_lazy as _

# dependencies
from utils.models import HappyDogsModel


class Dog(HappyDogsModel):
    """Dogs model."""
    first_name = models.CharField(
        _('Dog first name'),
        max_length=50,
    )
    last_name = models.CharField(
        _('Dog last name'),
        max_length=100,
        blank=True,
        null=True,
    )

    class Meta:
        """Meta option."""
        constraints = [
            models.UniqueConstraint(
                fields=['first_name', 'last_name'],
                name='Unique full name'
            )
        ]

    def __str__(self):
        """Get dog's full name."""
        return self.get_full_name()

    def get_full_name(self):
        """Get dog's full name."""
        return "{} {}".format(self.first_name, self.last_name)
