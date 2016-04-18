from datetime import timedelta
from django.utils import timezone
from beerstats.models import Brew
from calendar import timegm

def get_chart_series(interval_size=2):
    """Return series for highcharts with a given interval in hours
    :interval_size: interval in hours
    :returns: series of [interval, count]
    """
    series = []
    data = _get_data(interval_size)
    for dataitem in data:
        itemdata = []
        for interval, count in sorted(data[dataitem].items()):
            itemdata.append([get_js_date(interval), count])

        series.append({"name": dataitem,
                       "data": itemdata})
    return series


def _get_data(interval_size):
    """Returns raw data for get_chart_series
    """
    data = {}
    for brew in Brew.objects.all():
        intervaldata = {}
        for interval in _get_intervals(interval_size, brew.start_time, brew.get_max_date()):
            intervaldata[interval] = brew.bubbles_in_interval(interval, interval + timedelta(hours=interval_size))
        data[brew.name] = intervaldata
    return data


def _get_intervals(interval_size, start_date, end_date):
    """ Calculate a list of intervals between two dates
        based based on a given interval size in hours
    :interval_size: size of intervals in hours
    :start_date: start date of interval
    :end_date: end date for interval
    :returns: a list of n intervals between the two specified dates
    """
    if not end_date:
        end_date = start_date
    intervals = []
    while start_date <= end_date:
        intervals.append(timezone.localtime(start_date))
        start_date += timedelta(hours=interval_size)
    return intervals


def get_js_date(date):
    return int(timegm(date.timetuple())) * 1000
