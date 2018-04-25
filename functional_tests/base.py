
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class FunctionalBaseTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = self.open_browser()

    @staticmethod
    def open_browser():
        ff_options = webdriver.FirefoxOptions()
        ff_options.set_headless()
        browser = webdriver.Firefox(options=ff_options)
        browser.implicitly_wait(3)
        return browser

    def reset_browser(self):
        self.browser.quit()
        return self.open_browser()

    def tearDown(self):
        self.browser.close()
