import unittest
from unittest.mock import Mock, MagicMock, patch
from Calendar import Calendar


class CalendarTestGetEvents(unittest.TestCase):
    """
    Test suite to test for upcoming events
    """

    def setUp(self) -> None:
        self.mock_api = MagicMock()
        self.Calendar = Calendar(self.mock_api)

    def test_get_reminders(self):
    #     Removed temporarily

    def test_get_upcoming_events_number(self):
        """
        Number of upcoming events
        """
        time = "2020-08-03T00:00:00.000000Z"

        # Valid case
        num_events = 2
        try:
            self.Calendar.get_upcoming_events(time, num_events)
        except ValueError:
            self.fail("ValueError Raised: Test failed")

        # Invalid Cases : Events cannot be zero
        num_events = 0
        self.assertRaises(ValueError, self.Calendar.get_upcoming_events, time, num_events)

        num_events = -5
        self.assertRaises(ValueError, self.Calendar.get_upcoming_events, time, num_events)

    def test_get_upcoming_events_api_call(self):
        num_events = 2
        time = "2020-08-03T00:00:00.000000Z"

        # Call count
        events = self.Calendar.get_upcoming_events(time, num_events)
        access_event_list = self.mock_api.events().list().execute.return_value
        print(access_event_list)
        self.assertEqual(access_event_list.get.call_count, 1)

        # num_events properly passed
        args, kwargs = self.mock_api.events.return_value.list.call_args_list[0]
        self.assertEqual(kwargs['maxResults'], num_events)

        # Check if non empty number of events is returned.
        self.assertNotEqual(events.items, [])

    def test_year_input_valid(self):
        default_future_year_limit = 2
        default_past_year_limit = 5

        # Invalid Inputs
        year_input = -3

        self.assertRaises(ValueError, self.Calendar.get_past_events, year_input)  # Past
        self.assertRaises(ValueError, self.Calendar.get_future_events, year_input)  # future

        # Default Obeyed
        self.assertEqual(self.Calendar.get_future_events.__defaults__[0], default_future_year_limit)
        self.assertEqual(self.Calendar.get_past_events.__defaults__[0], default_past_year_limit)

    def test_get_events_no_event_case(self):
        self.mock_api.events().list().execute()["items"] = MagicMock(side_effect=KeyError())

        try:
            self.Calendar.get_future_events()
        except KeyError:
            self.fail("Test failed: KeyError raised for no event instance.")


class CalendarTestNavigateEvents(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_api = MagicMock()
        self.Calendar = Calendar(self.mock_api)

    @patch('Calendar.Calendar')
    def test_navigate_events_with_reminders(self, mock_cal):
        mock_cal.get_past_events = MagicMock(return_value=[{'id': '1olba0rgbijmfv72m1126kpftf',
                                             'summary': 'Past Event Summary',
                                             'start': {'date': '2020-10-13'},
                                             'reminders': {'useDefault': True}},
                                            {'id': '2insr0pnrijmfv72m1126kpftf',
                                             'summary': 'Past Event 2 Summary',
                                             'start': {'date': '2020-11-13'},
                                             'reminders': {'useDefault': True}}])


        mock_cal.get_future_events = MagicMock(return_value=[{'id': '4odta0egtjvboj82p4326esnvw',
                                           'summary': 'Future Event Summary',
                                           'start': {'dateTime': '2020-10-22T18:30:00+05:30'},
                                           'reminders': {'useDefault': False, 'overrides': [
                                               {'method': 'email', 'minutes': 20},
                                               {'method': 'popup', 'minutes': 10}]}}])


        print(mock_cal.get_past_events.return_value)
        print(mock_cal.get_future_events.return_value)
        search_result = mock_cal.navigate_to_events('2020-10').return_value

        print(search_result)
        self.assertEqual(
            ['Event:Future Event Summary at 2020-10-22T18:30:00+05:30\nReminder in 20 minutes before event as email\nReminder in 10 minutes before event as popup'],
            search_result)

    def test_navigate_to_non_existent_events_(self):
        search_result = self.Calendar.navigate_to_events('2020-10')
        self.assertEqual(["Nothing showed up at this time: 2020-10"], search_result)


class CalendarTestSearchEvents(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_api = MagicMock()
        self.Calendar = Calendar(self.mock_api)

    def test_search_events_with_default_reminders(self):
        self.Calendar.get_past_events = MagicMock(return_value=[{'id': '1olba0rgbijmfv72m1126kpftf',
                                                                 'summary': 'Past Event Summary',
                                                                 'start': {'dateTime': '2020-10-13T11:30:00+05:30'},
                                                                 'reminders': {'useDefault': True}}])
        self.Calendar.get_future_events = MagicMock(return_value=[{'id': '4odta0egtjvboj82p4326esnvw',
                                                                   'summary': 'Future Event Summary',
                                                                   'start': {'dateTime': '2020-10-22T18:30:00+05:30'},
                                                                   'reminders': {'useDefault': True}}])

        search_result = self.Calendar.search_events('past')
        self.assertEqual(
            ['Event:Past Event Summary at 2020-10-13T11:30:00+05:30\nReminder in 10 minutes before event'],
            search_result)

    def test_search_events_with_user_reminders(self):
        self.Calendar.get_past_events = MagicMock(return_value=[{'id': '1olba0rgbijmfv72m1126kpftf',
                                                                 'summary': 'Past Event Summary',
                                                                 'start': {'dateTime': '2020-10-13T11:30:00+05:30'},
                                                                 'reminders': {'useDefault': True}}])
        self.Calendar.get_future_events = MagicMock(return_value=[{'id': '4odta0egtjvboj82p4326esnvw',
                                                                   'summary': 'Future Event Summary',
                                                                   'start': {'dateTime': '2020-10-22T18:30:00+05:30'},
                                                                   'reminders': {'useDefault': False, 'overrides': [
                                                                       {'method': 'email', 'minutes': 20},
                                                                       {'method': 'popup', 'minutes': 10}]}
                                                                   }])

        search_result = self.Calendar.search_events('future')
        self.assertEqual(
            [
                'Event:Future Event Summary at 2020-10-22T18:30:00+05:30\nReminder in 20 minutes before event as email\nReminder in 10 minutes before event as popup'],
            search_result)

    def test_search_non_existent_events(self):
        self.Calendar.get_past_events = MagicMock(return_value=[{'id': '1olba0rgbijmfv72m1126kpftf',
                                                                 'summary': 'Past Event Summary',
                                                                 'start': {'dateTime': '2020-10-13T11:30:00+05:30'},
                                                                 'reminders': {'useDefault': True}}])
        self.Calendar.get_future_events = MagicMock(return_value=[{'id': '4odta0egtjvboj82p4326esnvw',
                                                                   'summary': 'Future Event Summary',
                                                                   'start': {
                                                                       'dateTime': '2020-10-22T18:30:00+05:30'},
                                                                   'reminders': {'useDefault': True}}])
        searchResult = self.Calendar.search_events('anything')
        self.assertEqual(
            ["Nothing showed up in your search"],
            searchResult)


class CalendarTestDeleteEvents(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_api = MagicMock()
        self.Calendar = Calendar(self.mock_api)

    def test_delete_api_call(self):

        event = {'id': '1olba0rgbijmfv72m1126kpftf', 'summary': 'Past Event Summary',
                 'start': {'dateTime': '2020-10-13T11:30:00+05:30'}, 'reminders': {'useDefault': True}}

        self.Calendar.delete_events(event)
        delete_event = self.mock_api.events().delete().execute()
        self.assertEqual(delete_event.get.call_count, 1)

    @patch('Calendar.Calendar.get_past_events')
    @patch('Calendar.Calendar.get_future_events')
    def test_delete_method(self, mock_future, mock_past):

        event = {'id': '1olba0rgbijmfv72m1126kpftf', 'summary': 'Past Event Summary'}
        self.Calendar.get_past_events.return_value = [event]
        self.Calendar.delete_events(event)
        self.assertEqual(self.Calendar.get_past_events.return_value, [])


def main():
    # Create the test suite from the cases above.

    navigateSuite = unittest.TestLoader().loadTestsFromTestCase(CalendarTestNavigateEvents)
    searchSuite = unittest.TestLoader().loadTestsFromTestCase(CalendarTestSearchEvents)
    # deleteSuite = unittest.TestLoader().loadTestsFromTestCase(CalendarTestDeleteEvents)

    # This will run the test suite.
    unittest.TextTestRunner(verbosity=2).run(navigateSuite)
    unittest.TextTestRunner(verbosity=2).run(searchSuite)
    # unittest.TextTestRunner(verbosity=2).run(deleteSuite)

if __name__ == "__main__":
    main()
