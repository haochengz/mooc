
from datetime import datetime

from django.test import TestCase

from apps.utils.tools import minutes_ago


class ToolsTest(TestCase):

    def test_minutes_ago(self):
        now = datetime.now()
        early = minutes_ago(now, 30)

        diff = (now - early).total_seconds()
        self.assertEqual(diff, 1800)
