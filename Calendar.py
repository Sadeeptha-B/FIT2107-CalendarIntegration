# Code adapted from https://developers.google.com/calendar/quickstart/python
import datetime
from dateutil.relativedelta import relativedelta
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def get_calendar_api():   # pragma: no cover
    """
    Get an object which allows you to consume the Google Calendar API.
    You do not need to worry about what this function exactly does, nor create test cases for it.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('calendar', 'v3', credentials=creds)


class Calendar:
    DEFAULT_CALENDAR_ID = "primary"

    def __init__(self, api=get_calendar_api(), calendar_id: str = DEFAULT_CALENDAR_ID):
        self.api = api
        self.calendar_id = calendar_id

    def get_upcoming_events(self, starting_time: str, number_of_events: int):
        """
        Shows basic usage of the Google Calendar API.
        Prints the start and name of the next n events on the user's calendar.
        """
        if number_of_events <= 0:
            raise ValueError("Number of events must be at least 1.")

        events_response = self.api.events().list(calendarId=self.calendar_id, timeMin=starting_time,
                                                 maxResults=number_of_events, singleEvents=True,
                                                 orderBy='startTime').execute()
        return events_response.get('items', [])

    def __get_events_from_year(self, years):
        time_now = datetime.datetime.utcnow()
        change_date = time_now + relativedelta(years=years)

        time_min = get_date_iso(min(time_now, change_date))
        time_max = get_date_iso(max(time_now, change_date))

        events_response = self.api.events().list(calendarId=self.calendar_id, singleEvents=True,
                                                 orderBy='startTime', timeMin=time_min,
                                                 timeMax=time_max).execute()

        return events_response.get('items', [])

    def get_past_events(self, years_past: int = 5):
        year_input = - years_past
        return self.__get_events_from_year(year_input)

    def get_future_events(self, years_future: int = 2):
        return self.__get_events_from_year(years_future)


def get_date_iso(date_str: str):
    """
    :param: date_str should be in utc format
    """
    return date_str.isoformat() + 'Z'


def main():
    primary_calendar = Calendar()

    time_now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    # events = primary_calendar.get_upcoming_events(time_now, 10)
    # events = primary_calendar.get_past_events()
    events = primary_calendar.get_future_events()


    if not events:
        print('No upcoming events found.')

    i = 0
    for event in events:
        i += 1
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(i, start, event['summary'])


if __name__ == "__main__":  # Prevents the main() function from being called by the test suite runner
    main()


# Requirements --------------------------------
#   Events, reminders, notifications 5 years past, 2 years future least; all events
#   Navigate through days, months, years, view details of events (events, reminders, notifications)
#   Send invitations to attendees with student.monash.edu address
#          Do not support other emails
#   Search events, reminders, notifications using different keywords
#   Delete events, reminders, notifications


