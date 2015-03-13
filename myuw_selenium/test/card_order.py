from myuw_selenium.platforms import on_platforms, SeleniumLiveServerTestCase

@on_platforms()
class CardOrderTest(SeleniumLiveServerTestCase):
    """
    Tests the order and display of cards at various times in the quarter.
    """

    def test_card_order(self):
        from time import sleep

        # Allow longer failures messages
        self.maxDiff = None

        dates = [
            { 'date': "2013-04-07", 'user': 'none', 'cards': ['VisualScheduleCard', 'CourseCard', 'TuitionCard'] }, # Needs to be none to have no registrations, otherwise RegStatusCard is hidden
            { 'date': "2013-04-08", 'user': 'none', 'cards': ['SummerRegStatusCardA', 'VisualScheduleCard', 'CourseCard', 'TuitionCard'] }, # Needs to be none to have no registrations, otherwise RegStatusCard is hidden
            { 'date': "2013-04-21", 'user': 'none', 'cards': ['SummerRegStatusCardA', 'VisualScheduleCard', 'CourseCard', 'TuitionCard'] }, # Needs to be none to have no registrations, otherwise RegStatusCard is hidden
            { 'date': "2013-04-22", 'user': 'none', 'cards': ['VisualScheduleCard', 'CourseCard', 'TuitionCard', 'SummerRegStatusCard1'] }, # Needs to be none to have no registrations, otherwise RegStatusCard is hidden
            { 'date': "2013-04-25", 'user': 'none', 'cards': ['VisualScheduleCard', 'CourseCard', 'TuitionCard', 'SummerRegStatusCard1'] }, # Needs to be none to have no registrations, otherwise RegStatusCard is hidden
            { 'date': "2013-04-26", 'user': 'none', 'cards': ['RegStatusCard', 'VisualScheduleCard', 'CourseCard', 'TuitionCard', 'SummerRegStatusCard1'] }, # Needs to be none to have no registrations, otherwise RegStatusCard is hidden
            { 'date': "2013-04-29", 'user': 'none', 'cards': ['RegStatusCard', 'VisualScheduleCard', 'CourseCard', 'TuitionCard', 'SummerRegStatusCard1'] }, # Needs to be none to have no registrations, otherwise RegStatusCard is hidden
            { 'date': "2013-05-30", 'user': 'none', 'cards': ['RegStatusCard', 'VisualScheduleCard', 'CourseCard', 'TuitionCard'] }, # Same!
            { 'date': "2013-03-10", 'user': 'none', 'cards': ['RegStatusCard', 'VisualScheduleCard', 'CourseCard', 'TuitionCard'] }, # Need to go back in time, otherwise autumn makes this break - Same though
            { 'date': "2013-03-11", 'user': 'none', 'cards': ['VisualScheduleCard', 'CourseCard', 'TuitionCard'] }, # Need to go back in time, otherwise autumn makes this break
            { 'date': "2013-04-01", 'user': 'javerage', 'cards': ['FutureQuarterCardA', 'VisualScheduleCard', 'TextbookCard', 'CourseCard', 'HFSCard', 'TuitionCard', 'LibraryCard', 'AcademicCard'] },
            { 'date': "2013-04-02", 'user': 'javerage', 'cards': ['FutureQuarterCardA', 'VisualScheduleCard', 'TextbookCard', 'CourseCard', 'HFSCard', 'TuitionCard', 'LibraryCard', 'AcademicCard'] }, # Same!
            { 'date': "2013-04-03", 'user': 'javerage', 'cards': ['VisualScheduleCard', 'TextbookCard', 'CourseCard', 'HFSCard', 'TuitionCard', 'LibraryCard', 'AcademicCard', 'FutureQuarterCard1'] }, # Future quarter moves to position 1
            { 'date': "2013-04-25", 'user': 'javerage', 'cards': ['VisualScheduleCard', 'CourseCard', 'HFSCard', 'TuitionCard', 'LibraryCard', 'AcademicCard', 'FutureQuarterCard1'] }, # Same!

            { 'date': "2013-06-07", 'user': 'javerage', 'cards': ['VisualScheduleCard', 'CourseCard', 'HFSCard', 'TuitionCard', 'LibraryCard', 'AcademicCard', 'FutureQuarterCard1'] }, # Same (ish)!
            { 'date': "2013-06-08", 'user': 'javerage', 'cards': ['FinalExamCard', 'GradeCard', 'CourseCard', 'HFSCard', 'TuitionCard', 'LibraryCard', 'AcademicCard', 'FutureQuarterCard1'] },
            { 'date': "2013-06-13", 'user': 'javerage', 'cards': ['FinalExamCard', 'GradeCard', 'CourseCard', 'HFSCard', 'TuitionCard', 'LibraryCard', 'AcademicCard', 'FutureQuarterCard1'] }, # Same!
            { 'date': "2013-06-15", 'user': 'javerage', 'cards': ['GradeCard', 'CourseCard', 'HFSCard', 'TuitionCard', 'LibraryCard', 'AcademicCard', 'FutureQuarterCard1'] },
            { 'date': "2013-08-27", 'user': 'javerage', 'cards': ['GradeCard', 'CourseCard', 'HFSCard', 'TuitionCard', 'LibraryCard', 'AcademicCard', 'FutureQuarterCard1'] }, # Need to go to the future - spring's grade submission deadline is always today actual.
            { 'date': "2013-08-28", 'user': 'javerage', 'cards': ['GradeCard', 'VisualScheduleCard', 'TextbookCard', 'CourseCard', 'HFSCard', 'TuitionCard', 'LibraryCard'] }, # Need to go to the future - spring's grade submission deadline is always today actual.
            { 'date': "2013-09-24", 'user': 'javerage', 'cards': ['GradeCard', 'VisualScheduleCard', 'TextbookCard', 'CourseCard', 'HFSCard', 'TuitionCard', 'LibraryCard'] }, # Same
            { 'date': "2013-09-25", 'user': 'javerage', 'cards': ['VisualScheduleCard', 'TextbookCard', 'CourseCard', 'HFSCard', 'TuitionCard', 'LibraryCard'] },
        ]

        curUser = ''
        index = 0
        for val in dates:
            date = val["date"]
            user = val["user"]

            if user != curUser:
                self.driver.get(self.live_server_url + '/users/')
                element = self.driver.find_element_by_xpath("//input[@name='override_as']")
                element.clear()
                element.send_keys(user)
                element.submit()
                curUser = user

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

            cards = val['cards']
            for i in range(len(cards)):
                cards[i] = unicode(cards[i])
                

            self.assertEqual(cards, displayed)
            
            index = index + 1
