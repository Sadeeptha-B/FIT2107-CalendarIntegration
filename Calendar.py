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


def get_calendar_api():  # pragma: no cover
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

    def __init__(self, api, calendar_id: str = DEFAULT_CALENDAR_ID):
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

    def search_events(self, keyword: str):
        """"
        Allows the user to search for events
        """
        events = self.get_past_events()
        events += self.get_future_events()
        search_Yield = False
        for event in events:
            if keyword.lower() in event['summary'].lower():
                search_Yield = True
                print('Event:' + event['summary'] + ' at ' + event['start'].get('dateTime', event['start'].get('date')))
                if event['reminders']['useDefault']:
                    print('Reminder in 10 minutes before event')
                else:
                    for reminder in event['reminders']['overrides']:
                        print('Reminder in ' + str(reminder['minutes']) + ' minutes before event as ' + reminder['method'])
        if not search_Yield:
            print("Nothing showed up in your search")


def get_date_iso(date_str: str):
    """
    :param: date_str should be in utc format
    """
    return date_str.isoformat() + 'Z'


def main():
    primary_calendar = Calendar(get_calendar_api())

    # print('Please enter your choice')
    # print('1. View past events.')
    # print('2. View future events')
    # print('3. Feature 3')
    # print('4. Search for an event and reminders')
    # print('5. Delete an event and reminders')
    # print('6. Exit')

    time_now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

    # choice = input('Your choice as an integer: ')

    # events = primary_calendar.get_upcoming_events(time_now, 10)
    # events = primary_calendar.get_past_events()
    # events = primary_calendar.get_future_events()
    # x = input("Enter Keyword for search: ")

    # while len(x) < 2:
    #    print("Keyword should be at least 2 characters long")
    #    x = input("Enter Keyword: ")

    # primary_calendar.search_events(x)


if __name__ == "__main__":  # Prevents the main() function from being called by the test suite runner
    main()

# Requirements --------------------------------
#   Events, reminders, notifications 5 years past, 2 years future least; all events
#   Navigate through days, months, years, view details of events (events, reminders, notifications)
#   Send invitations to attendees with student.monash.edu address
#          Do not support other emails
#   Search events and reminders using different keywords
#   Delete events and reminders
