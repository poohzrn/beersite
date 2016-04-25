"""
    Tests for Models.py
"""
from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from autofixture import AutoFixture
from beerstats.models import Brew
from beerstats.models import Bubble

# Constant for start / end
NOW = timezone.now()
START_DATE = NOW - timedelta(hours=24)
END_DATE = NOW


class BrewTest(TestCase):

    """Test Class for Brew model"""

    def setUp(self):
        "Set up test data for Brew Test "
        self.brew = AutoFixture(
            Brew, field_values={'name': 'test', 'start_time': START_DATE}).create(1)[0]

        time_stamp = START_DATE
        while time_stamp <= END_DATE:
            AutoFixture(Bubble, field_values={'time_stamp': time_stamp}).create()
            time_stamp = time_stamp + timedelta(hours=1)

    def test_str(self):
        "Test String representation"
        self.assertEqual('test', self.brew.name)

    def test_get_max_date(self):
        "Ensure we get the max date"
        self.assertEqual(END_DATE, self.brew.get_max_date())

    def test_get_min_date(self):
        "Ensure we get the min date"
        self.assertEqual(START_DATE, self.brew.get_min_date())

    def test_bubbles_in_interval(self):
        "test bubbles in interval"
        self.assertEqual(24, self.brew.bubbles_in_interval(START_DATE, END_DATE))
