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


class UtilTest(TestCase):

    """Tests for utils.py"""

    def setUp(self):
        """Setup test data"""
        self.end_date = timezone.now()
        self.start_date = self.end_date - timedelta(days=1)

        AutoFixture(Brew, field_values={'name': 'test', 'start_time': self.start_date}).create(1)

        for hour in range(0, 24):
            AutoFixture(Bubble, field_values={'time_stamp': self.start_date -
                                                            timedelta(hours=hour)}
                       ).create()

    def test_get_intervals(self):
        " Tests wether we get the correct amount of intervals "
        interval_size = 1
        intervals = _get_intervals(interval_size, self.start_date, self.end_date)
        self.assertEqual(len(intervals), 24)
        interval_size = 12
        intervals = _get_intervals(interval_size, self.start_date, self.end_date)
        self.assertEqual(len(intervals), 2)
        self.assertEqual(intervals[0], self.start_date)
        self.assertEqual(intervals[-1], self.end_date - timedelta(hours=interval_size))
