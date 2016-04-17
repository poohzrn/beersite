from datetime import timedelta
from django.utils import timezone
from beerstats.models import Brew


def get_intervals(interval_size, start_date, end_date):
    """ Calculate a list of intervals between two dates
        based based on a given interval size in hours
    :interval_size: size of intervals in hours
    :start_date: start date of interval
    :end_date: end date for interval
    :returns: a list of n intervals between the two specified dates
    """
    intervals = []
    while start_date <= end_date:
        intervals.append(timezone.localtime(start_date))
        start_date += timedelta(hours=interval_size)
    return intervals


def get_chart_data(intervals, interval_size, brew_id):
    """TODO: Docstring for get_chart_data.
    :intervals: TODO
    :brew_id: TODO
    :returns: TODO
    """
    brew = Brew.objects.get(id=brew_id)
    data = [['ts', 'bubbles']]
    for interval in intervals:
        data.append([str(interval),
                    brew.bubbles_in_interval(interval,
                    interval + timedelta(hours=interval_size))])
    return data


class ChartData(object):
    def get_data(time_from=timezone.now(), time_to=timezone.now(), size=2):
        brews = Brew.objects.all()
        data = {}
        for brew in brews:
            intervaldata = {}
            for interval in get_intervals(size, time_from, time_to):
                intervaldata[interval] = brew.bubbles_in_interval(interval, interval + timedelta(hours=size))
            data[brew.name] = intervaldata
        return data
