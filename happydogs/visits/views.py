"""Visits views."""

# DRF
from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter

# Django
from django.views.generic import ListView

# models
from .models import Visit

# dependencies
from datetime import datetime, timedelta


class ListVisitView(ListView):
    """List all visits day by day on given period."""

    template_name = 'home.html'
    model = Visit
    context_object_name = 'visits'

    def get_queryset(self):
        """Customize queryset to return dict object where 
        keys are ordered days within the period, and values
        the count of dogs."""
        response = {"results": {}}
        period_start_str = self.request.GET.get('period_start', None)
        period_end_str = self.request.GET.get('period_end', None)

        period_start = datetime.strptime(period_start_str, "%Y-%m-%d")
        period_end = datetime.strptime(period_end_str, "%Y-%m-%d")

        for i in range(0, (period_end - period_start).days + 1):
            curr_date = period_start + timedelta(i)
            response['intervals'].setdefault(
                curr_date,
                Visit.objects.filter(
                    start_date__lte=curr_date,
                    end_date__gte=curr_date)
                .count()
            )

        response.setdefault('week_start')

        return response


# class CircleViewSet(mixins.ListModelMixin,
#                     viewsets.GenericViewSet):
#     """Circle view set."""

#     serializer_class = VisitModelSerializer
#     lookup_field = 'slug_name'

#     # Filters
#     filter_backends = (SearchFilter)
#     search_fields = ('period_start', 'period_end')

#     def get_queryset(self):
#         """Restrict list to public-only."""
#         queryset = Visit.objects.all()
#         response = {"results": {}}
#         period_start_str = self.request.GET.get('period_start', None)
#         period_end_str = self.request.GET.get('period_end', None)
#         print(period_start_str)
#         print(type(str(period_start_str)))
#         print(datetime.strptime(str(period_start_str), "%Y/%m/%d"))

#         period_start = datetime.strptime(period_start_str, "%Y-%m-%d")
#         period_end = datetime.strptime(period_end_str, "%Y-%m-%d")
#         if self.action == 'list':
#             for i in range(0, (period_end - period_start).days + 1):
#                 curr_date = period_start + timedelta(i)
#                 response['results'].setdefault(
#                     curr_date,
#                     Visit.objects.filter(
#                         start_date__lte=curr_date,
#                         end_date__gte=curr_date)
#                     .count()
#                 )
#         return queryset
