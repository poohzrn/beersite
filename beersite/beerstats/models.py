from django.db import models
from django.db.models import Min
from django.utils import timezone

def get_intervals(interval_size, start_date, end_date):
    """ Calculate a list of intervals between two dates
        based based on a given interval size in hours
    :interval_size: size of intervals in hours
    :start_date: start date of interval
    :end_date: end date for interval
    :returns: a list of n intervals between the two specified dates
    """
    number_of_days = (end_date - start_date).days
    return [end_date - timedelta(hours=interval, days=day)
            for day in range(0, number_of_days)
            for interval in range(0, interval_size)]

class Brew(models.Model):
    """A brew class"""
    name = models.CharField(max_length=50)
    bubble_sensor_gpio = models.SmallIntegerField(blank=True, null=True)
    start_time = models.DateTimeField(default=timezone.now)

    def bubbles_in_interval(self, time_from, time_to):
        """TODO: Docstring for bubbles_in_interval.

        :time_from: TODO
        :time_to: TODO
        :returns: TODO

        """
        if time_from > time_to:
            return self.bubble_set.filter(time_stamp__gte=time_to,
                                          time_stamp__lt=time_from).count()
        else:
            return self.bubble_set.filter(time_stamp__gte=time_from,
                                          time_stamp__lt=time_to).count()

    def bubbles_from_to_now(self, time_from):
        """TODO: Docstring for bubbles_from_to_now.

        :time_from: time from
        :returns: number of bubbles from 'time_from' untill now

        """
        return self.bubbles_in_interval(time_from, timezone.now())

    def get_min_date(self):
        """TODO: Docstring for get_min_date.
        :returns: First date a bubble is registered

        """
        return self.bubble_set.all(). \
            aggregate(Min('time_stamp'))['time_stamp__min']

    def __str__(self):
        """TODO: Docstring for __str__.
        :returns: TODO

        """
        return self.name


class Bubble(models.Model):

    """This is a bubble"""
    time_stamp = models.DateTimeField(default=timezone.now, blank=True)
    brew = models.ForeignKey(Brew)

    def __str__(self):
        """TODO: Docstring for __str__.
        :returns: TODO

        """
        return self.brew.name + ": " + str(self.time_stamp.isoformat())
