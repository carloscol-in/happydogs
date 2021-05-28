"""Dogs models."""

from django.db import models
from django.utils.translation import gettext_lazy as _

# dependencies
from happydogs.utils.models import HappyDogsModel


class Dogs(HappyDogsModel):
    """Dogs model."""
    first_name = models.CharField(
        _('Dog first name'),
        max_length=50,
    )
    last_name = models.CharField(
        _('Dog last name'),
        max_length=100,
    )

    class Meta:
        """Meta option."""
        constraints = [
            models.UniqueConstraint(
                fields=['first_name', 'last_name'],
                name='Unique full name'
            )
        ]
