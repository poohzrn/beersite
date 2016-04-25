"""
    Tests for Util
"""
from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from autofixture import AutoFixture
from beerstats.models import Brew
from beerstats.models import Bubble
from beerstats.utils import _get_intervals


# Constant for start / end
NOW = timezone.now()
START_DATE = NOW - timedelta(hours=24)
END_DATE = NOW

class UtilTest(TestCase):

    """Tests for utils.py"""

    def setUp(self):
        "Set up test data for Brew Test "
        self.brew = AutoFixture(
            Brew, field_values={'name': 'test', 'start_time': START_DATE}).create(1)[0]

        time_stamp = START_DATE
        while time_stamp <= END_DATE:
            AutoFixture(Bubble, field_values={'time_stamp': time_stamp, 'brew': self.brew}).create()
            time_stamp = time_stamp + timedelta(hours=1)

    def test_get_intervals(self):
        " Tests wether we get the correct amount of intervals "
        interval_size = 1
        intervals = _get_intervals(interval_size, START_DATE, END_DATE)
        self.assertEqual(len(intervals), 24)
        interval_size = 12
        intervals = _get_intervals(interval_size, START_DATE, END_DATE)
        self.assertEqual(len(intervals), 2)
        self.assertEqual(intervals[0], START_DATE)
        self.assertEqual(intervals[-1], END_DATE - timedelta(hours=interval_size))
