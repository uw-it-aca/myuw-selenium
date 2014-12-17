# From https://github.com/Victory/django-travis-saucelabs
import os
import sys
import re

from unittest2 import skipIf

try:
    from selenium import webdriver
    has_selenium = True
except Exception as ex:
    print ex
    has_selenium = False

from django.test import LiveServerTestCase

RUN_ON_SAUCE = os.environ.get('RUN_TESTS_SAUCELAB') == 'True'
RUN_LOCAL = not RUN_ON_SAUCE

if RUN_LOCAL:
    # could add Chrome, PhantomJS etc... here
    browsers = ['Firefox']
else:
    try:
        from sauceclient import SauceClient
        USERNAME = os.environ.get('SAUCE_USERNAME')
        ACCESS_KEY = os.environ.get('SAUCE_ACCESS_KEY')
        sauce = SauceClient(USERNAME, ACCESS_KEY)
    except Exception as ex:
        print "EX: ", ex
        pass

    if has_selenium:
        iphone = webdriver.DesiredCapabilities.IPHONE
        iphone['platform'] = "OS X 10.9"
        iphone['version'] = "8.1"
        iphone['browserName'] = "iPhone"
        iphone['device-orientation'] = 'portrait'

        ipad = webdriver.DesiredCapabilities.IPAD
        ipad['platform'] = "OS X 10.9"
        ipad['version'] = "8.1"
        ipad['browserName'] = "iPad"
        ipad['device-orientation'] = 'portrait'

        android_nexus = webdriver.DesiredCapabilities.ANDROID
        android_nexus['platform'] = "Linux"
        android_nexus['version'] = "4.4"
        android_nexus['deviceName'] = "Google Nexus 7 HD Emulator"
        android_nexus['device-orientation'] = 'portrait'

        browsers = [
            android_nexus,
            iphone,
            ipad,
            {"platform": "Mac OS X 10.9",
             "browserName": "chrome",
             "version": "35"},
            {"platform": "Windows 8.1",
             "browserName": "internet explorer",
             "version": "11"},
            {"platform": "Linux",
             "browserName": "firefox",
             "version": "29"}
        ]

        browsers = [
            {"platform": "Linux",
             "browserName": "firefox",
             "version": "29"}
        ]
    else:
        browsers = []

def on_platforms(platforms, local):
    if local:
        def decorator(base_class):
            module = sys.modules[base_class.__module__].__dict__
            for i, platform in enumerate(platforms):
                d = dict(base_class.__dict__)
                d['browser'] = platform
                name = "%s_%s" % (base_class.__name__, i + 1)
                module[name] = type(name, (base_class,), d)
            pass
        return decorator

    def decorator(base_class):
        module = sys.modules[base_class.__module__].__dict__
        for i, platform in enumerate(platforms):
            d = dict(base_class.__dict__)
            d['desired_capabilities'] = platform
            name = "%s_%s" % (base_class.__name__, i + 1)
            module[name] = type(name, (base_class,), d)

    return decorator

from django.conf import settings


class SeleniumLiveServerTestCase(LiveServerTestCase):

    def __init__(self, *args, **kwargs):
        super(SeleniumLiveServerTestCase, self).__init__(*args, **kwargs)
        if settings.DEBUG == False:
            settings.DEBUG = True


@on_platforms(browsers, RUN_LOCAL)
class CardOrderTest(SeleniumLiveServerTestCase):
    """
    Runs a test using travis-ci and saucelabs
    """

    def setUp(self):
        if RUN_LOCAL:
            self.setUpLocal()
        else:
            self.setUpSauce()

    def tearDown(self):
        if RUN_LOCAL:
            self.tearDownLocal()
        else:
            self.tearDownSauce()

    def setUpSauce(self):
        self.desired_capabilities['name'] = self.id()
        self.desired_capabilities['tunnel-identifier'] = \
            os.environ.get('TRAVIS_JOB_NUMBER', '')
        self.desired_capabilities['build'] = os.environ.get('TRAVIS_BUILD_NUMBER', '')
        self.desired_capabilities['tags'] = \
            [os.environ.get('TRAVIS_PYTHON_VERSION', ''), 'CI']

        print self.desired_capabilities

        sauce_url = "http://%s:%s@ondemand.saucelabs.com:80/wd/hub"
        self.driver = webdriver.Remote(
            desired_capabilities=self.desired_capabilities,
            command_executor=sauce_url % (USERNAME, ACCESS_KEY)
        )
        self.driver.implicitly_wait(5)

    def setUpLocal(self):
        self.driver = getattr(webdriver, self.browser)()
        self.driver.implicitly_wait(3)

    def tearDownLocal(self):
        self.driver.quit()

    def tearDownSauce(self):
        print("\nLink to your job: \n "
              "https://saucelabs.com/jobs/%s \n" % self.driver.session_id)
        try:
            if sys.exc_info() == (None, None, None):
                sauce.jobs.update_job(self.driver.session_id, passed=True)
            else:
                sauce.jobs.update_job(self.driver.session_id, passed=False)
        finally:
            self.driver.quit()

    def test_myuw(self):
        from time import sleep

        dates = [
            { 'date': "2013-04-01", 'user': 'javerage' },
            { 'date': "2013-04-25", 'user': 'javerage' }, # Same!
            { 'date': "2013-04-26", 'user': 'none' }, # Needs to be none to have no registrations, otherwise RegStatusCard is hidden
            { 'date': "2013-05-30", 'user': 'none' }, # Same!
            { 'date': "2013-03-10", 'user': 'none' }, # Need to go back in time, otherwise autumn makes this break - Same though
            { 'date': "2013-03-11", 'user': 'none' }, # Need to go back in time, otherwise autumn makes this break
            { 'date': "2013-06-07", 'user': 'javerage' }, # Same (ish)!
            { 'date': "2013-06-08", 'user': 'javerage' },
            { 'date': "2013-06-13", 'user': 'javerage' }, # Same!
            { 'date': "2013-06-15", 'user': 'javerage' },
            { 'date': "2013-08-27", 'user': 'javerage' }, # Need to go to the future - spring's grade submission deadline is always today actual.
            { 'date': "2013-08-28", 'user': 'javerage' }, # Need to go to the future - spring's grade submission deadline is always today actual.
            { 'date': "2013-09-24", 'user': 'javerage' }, # Same
            { 'date': "2013-09-25", 'user': 'javerage' },
        ]

        correct_cards = [
            [u'FutureQuarterCardA', u'VisualScheduleCard', u'CourseCard', u'HFSCard', u'TuitionCard', u'LibraryCard', u'AcademicCard'],
            [u'FutureQuarterCardA', u'VisualScheduleCard', u'CourseCard', u'HFSCard', u'TuitionCard', u'LibraryCard', u'AcademicCard'],
            [u'RegStatusCard', u'VisualScheduleCard', u'CourseCard', u'HFSCard', u'TuitionCard', u'LibraryCard', u'AcademicCard', u'FutureQuarterCard1'],
            [u'RegStatusCard', u'VisualScheduleCard', u'CourseCard', u'HFSCard', u'TuitionCard', u'LibraryCard', u'AcademicCard', u'FutureQuarterCard1'],
            [u'RegStatusCard', u'VisualScheduleCard', u'CourseCard', u'HFSCard', u'TuitionCard', u'LibraryCard', u'AcademicCard', u'FutureQuarterCard1'],
            [u'VisualScheduleCard', u'CourseCard', u'HFSCard', u'TuitionCard', u'LibraryCard', u'AcademicCard', u'FutureQuarterCard1'],
            [u'FutureQuarterCardA', u'VisualScheduleCard', u'CourseCard', u'HFSCard', u'TuitionCard', u'LibraryCard', u'AcademicCard'],
            [u'GradeCard', u'FinalExamCard', u'FutureQuarterCardA', u'CourseCard', u'HFSCard', u'TuitionCard', u'LibraryCard', u'AcademicCard'],
            [u'GradeCard', u'FinalExamCard', u'FutureQuarterCardA', u'CourseCard', u'HFSCard', u'TuitionCard', u'LibraryCard', u'AcademicCard'],
            [u'GradeCard', u'FutureQuarterCardA', u'CourseCard', u'HFSCard', u'TuitionCard', u'LibraryCard', u'AcademicCard'],
            [u'GradeCard', u'FutureQuarterCardA', u'CourseCard', u'HFSCard', u'TuitionCard', u'LibraryCard', u'AcademicCard'],
            [u'GradeCard', u'VisualScheduleCard', u'CourseCard', u'HFSCard', u'TuitionCard', u'LibraryCard', u'AcademicCard', u'FutureQuarterCard1'],
            [u'GradeCard', u'VisualScheduleCard', u'CourseCard', u'HFSCard', u'TuitionCard', u'LibraryCard', u'AcademicCard', u'FutureQuarterCard1'],
            [u'VisualScheduleCard', u'CourseCard', u'HFSCard', u'TuitionCard', u'LibraryCard', u'AcademicCard', u'FutureQuarterCard1'],
        ]

        index = 0
        for val in dates:
            date = val["date"]
            user = val["user"]
            self.driver.get(self.live_server_url + '/users/')
            element = self.driver.find_element_by_xpath("//input[@name='override_as']")
            element.clear()
            element.send_keys(user)
            element.submit()

            self.driver.get(self.live_server_url + '/mobile/admin/dates/')
            element = self.driver.find_element_by_xpath("//input[@name='date']")
            element.clear()
            element.send_keys(date)
            element.submit()
            self.driver.get(self.live_server_url + '/mobile/landing/')
            # XXX - this is lame.  need to add something to wait on here instead
            sleep(2)
            title = self.driver.title
            self.assertEquals(self.driver.title, "MyUW Mobile Home")

            divs = self.driver.find_elements_by_css_selector("#landing_content > div")

            displayed = []
            for div in divs:
                if div.get_attribute("style") != "display: none;":
                    displayed.append(div.get_attribute("id"))

            cards = correct_cards[index]
            for i in range(0, len(cards)-1):
                self.assertEquals(cards[i], displayed[i])

            index = index + 1
