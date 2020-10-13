import unittest
from unittest.mock import Mock
from Calendar import Calendar


class CalendarTestGetEvents(unittest.TestCase):
    """
    Test suite to test for upcoming events
    """
    def setUp(self) -> None:
        self.mock_api = Mock()
        self.Calendar = Calendar(self.mock_api)

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
        self.assertRaises(ValueError, self.Calendar.get_upcoming_events,time, num_events)

        num_events = -5
        self.assertRaises(ValueError, self.Calendar.get_upcoming_events, time, num_events)

    def test_get_upcoming_events_api_call(self):
        num_events = 2
        time = "2020-08-03T00:00:00.000000Z"

        # Call count
        events = self.Calendar.get_upcoming_events(time, num_events)
        access_event_list = self.mock_api.events().list().execute.return_value
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

        self.assertRaises(ValueError, self.Calendar.get_past_events,year_input)  # Past
        self.assertRaises(ValueError, self.Calendar.get_future_events, year_input) # future

        # Default Obeyed
        self.assertEqual(self.Calendar.get_future_events.__defaults__[0], default_future_year_limit)
        self.assertEqual(self.Calendar.get_past_events.__defaults__[0], default_past_year_limit)

    def test_events_future(self):
        events = self.Calendar.get_future_events()

        # Check if non empty number of events is returned.
        self.assertNotEqual(events.items, [])


def main():
    # Create the test suite from the cases above.
    suite = unittest.TestLoader().loadTestsFromTestCase(CalendarTestGetEvents)

    # This will run the test suite.
    unittest.TextTestRunner(verbosity=2).run(suite)


main()