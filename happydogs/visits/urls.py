"""Visits urls."""

# Django
from django.urls import path
from django.views.generic import TemplateView

# Views
from .views import (
    ListVisitView,
)

urlpatterns = [
    # path('', TemplateView.as_view(template_name='home.html')),
    path('', ListVisitView.as_view(), name='visits'),
]
