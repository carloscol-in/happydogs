"""Visits views."""

# Django
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView
from django.views.decorators.http import require_http_methods

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
        response = {"calendar": {}}

        period_start_str = self.request.GET.get('period_start', None)
        period_end_str = self.request.GET.get('period_end', None)

        period_start = datetime.strptime(period_start_str, "%Y-%m-%d")
        period_end = datetime.strptime(period_end_str, "%Y-%m-%d")

        period_week_start = (period_start -
                             timedelta(days=period_start.weekday()))
        period_week_end = (period_end +
                           timedelta(days=(7 - (period_end.weekday() + 1))))

        for i in range(0, (period_week_end - period_week_start).days + 1):
            curr_date = period_week_start + timedelta(i)

            if(curr_date >= period_start and curr_date <= period_end):
                response['calendar'].setdefault(
                    curr_date.strftime("%Y-%m-%d"),
                    {
                        'short_date': curr_date.strftime("%b %d"),
                        'dog_count': Visit.objects.filter(
                            start_date__lte=curr_date,
                            end_date__gte=curr_date)
                        .count()
                    }
                )
                continue

            response['calendar'].setdefault(curr_date.strftime("%b %d"), '')

        return response


@require_http_methods(["GET"])
def get_visits_on_period(request):
    """Json response for visits on given period."""
    response = {"calendar": {}}

    period_start_str = request.GET.get('period_start', None)
    period_end_str = request.GET.get('period_end', None)

    period_start = datetime.strptime(period_start_str, "%Y-%m-%d")
    period_end = datetime.strptime(period_end_str, "%Y-%m-%d")

    period_week_start = (period_start -
                         timedelta(days=period_start.weekday()))
    period_week_end = (period_end +
                       timedelta(days=(7 - (period_end.weekday() + 1))))

    for i in range(0, (period_week_end - period_week_start).days + 1):
        curr_date = period_week_start + timedelta(i)

        if(curr_date >= period_start and curr_date <= period_end):
            response['calendar'].setdefault(
                i,
                {
                    'short_date': curr_date.strftime("%b %d"),
                    'long_date': curr_date.strftime("%Y-%m-%d"),
                    'dog_count': Visit.objects.filter(
                        start_date__lte=curr_date,
                        end_date__gte=curr_date)
                    .count()
                }
            )
            continue

        response['calendar'].setdefault(i, {})

    # return render(request, 'home.html', response, content_type='application/xhtml+xml')
    return JsonResponse(response, status=200, safe=False)
