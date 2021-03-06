"""
This is where we define our model used in the project

"""
from django.db import models
from django.db.models import Min
from django.db.models import Max
from django.utils import timezone


class Brew(models.Model):
    """A brew class"""
    name = models.CharField(max_length=50)
    bubble_sensor_gpio = models.SmallIntegerField(blank=True, null=True)
    start_time = models.DateTimeField(default=timezone.now)
    finished = models.BooleanField(default=False)

    def bubbles_in_interval(self, time_from, time_to):
        """Get the number of bubbles in a given time interval

        :time_from: Time from
        :time_to: Time to
        :returns: Number of bubbles

        """
        if time_from > time_to:
            return self.bubble_set.filter(time_stamp__gte=time_to,
                                          time_stamp__lt=time_from).count()
        else:
            return self.bubble_set.filter(time_stamp__gte=time_from,
                                          time_stamp__lt=time_to).count()

    def get_min_date(self):
        """ First date a bubble is registered
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
        """ String representation of Bubble objects
        :returns: pretty a string

        """
        return self.brew.name + ": " + str(self.time_stamp.isoformat())
