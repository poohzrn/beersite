from django.core.management.base import BaseCommand
from beerstats.models import Brew
from beerstats.models import Bubble
from autofixture import AutoFixture
from django.utils import timezone
from datetime import timedelta
from random import randint


class Command(BaseCommand):

    """Loads test data"""

    help = 'Tracks bubbles on a specified GPIO port'

    def handle(self, *args, **options):
        """handle bubbletrack command
        :*args: Add later
        :**options: ..
        """
        AutoFixture(Brew, field_values={
                    'start_time': timezone.now() - timedelta(days=7)}).create(3)
        for day in range(0, 7):
            for hour in range(0, 24):
                bubbles = randint(hour, hour + 400)
                AutoFixture(Bubble, field_values={'time_stamp': timezone.now(
                ) - timedelta(hours=hour, days=day)}).create(bubbles)
