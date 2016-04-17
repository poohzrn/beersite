from django.db import models
from django.db.models import Min
from django.db.models import Max
from django.utils import timezone


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
        return self.bubble_set.aggregate(Min('time_stamp'))['time_stamp__min']

    def get_max_date(self):
        """
        :returns: Last date a bubble is registered

        """
        return self.bubble_set.aggregate(Max('time_stamp'))['time_stamp__max']

    def __str__(self):
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
