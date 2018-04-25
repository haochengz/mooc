
from .base import FunctionalBaseTest


class UserModuleTest(FunctionalBaseTest):

    def test_starts(self):

        # Open index page
        self.browser.get(self.live_server_url)