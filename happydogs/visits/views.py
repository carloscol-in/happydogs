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


@require_http_methods(['GET'])
def get_dogs_on_day(request, date):
    """Get the dogs full name on given day."""
    response = {"dogs": []}
    status_code = 200

    # if date can be parsed to datetime, then continue
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except:
        response = {
            'error': 'You didn\'t wrote correctly the date.'
        }
        status_code = 404
    else:
        visits = Visit.objects.filter(start_date__lte=date, end_date__gte=date)

        for n in range(0, len(visits)):
            data = {
                'n': n,
                'fullname': visits[n].dog.get_full_name(),
                'startdate': visits[n].start_date.strftime("%Y-%m-%d"),
                'enddate': visits[n].end_date.strftime("%Y-%m-%d"),
            }
            response['dogs'].append(data)

    return JsonResponse(response, status=status_code, safe=False)
