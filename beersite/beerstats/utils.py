from datetime import timedelta
from beerstats.models import Brew


def get_intervals(interval_size, start_date, end_date):
    """ Calculate a list of intervals between two dates
        based based on a given interval size in hours
    :interval_size: size of intervals in hours
    :start_date: start date of interval
    :end_date: end date for interval
    :returns: a list of n intervals between the two specified dates
    """
    list2 = []
    while start_date <= end_date:
        list2.append(start_date)
        start_date += timedelta(hours=interval_size)
    return list2


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