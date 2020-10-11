import unittest
from unittest.mock import Mock
from Calendar import Calendar


class CalendarTestUpcoming(unittest.TestCase):
    """
    Test suite to test for upcoming events
    """

    # This test tests number of upcoming events.
    def test_get_upcoming_events_number(self):
        num_events = 2
        time = "2020-08-03T00:00:00.000000Z"

        mock_api = Mock()
        test_calendar = Calendar(mock_api)
        events = test_calendar.get_upcoming_events(time, num_events)

        self.assertEqual(
            mock_api.events.return_value.list.return_value.execute.return_value.get.call_count, 1)

        args, kwargs = mock_api.events.return_value.list.call_args_list[0]
        self.assertEqual(kwargs['maxResults'], num_events)

    # Add more test cases here


def main():
    # Create the test suite from the cases above.
    suite = unittest.TestLoader().loadTestsFromTestCase(CalendarTestUpcoming)

    # This will run the test suite.
    unittest.TextTestRunner(verbosity=2).run(suite)


main()