"""
Calendar application making use of Google Calendar API

Initial base code adapted from
    # https://developers.google.com/calendar/quickstart/python


NOTE: If the Google Calendar allows to set more than one default setting for Calendar/Event
reminders , it must be noted that this application will only support the retrieval of 
one default reminder setting.
"""

__author__ = "Sadeeptha Bandara, Kaveesha Nissanka"


import datetime
import pickle
import os.path
from dateutil.relativedelta import relativedelta
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly', 'https://www.googleapis.com/auth/calendar']


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
    DEFAULT_FUTURE_YEAR_RANGE = 2
    DEFAULT_PAST_YEAR_RANGE = 5


    def __init__(self, api, calendar_id: str = DEFAULT_CALENDAR_ID):
        self.api = api
        self.calendar_id = calendar_id
        self.reminder_defaults = self.get_calendar_reminder_defaults()
        self.event_reminder_defaults = self.reminder_defaults


    def get_calendar_reminder_defaults(self):
        """
        Get the global reminder defaults for calendar 
        """
        calendar_resource = self.api.calendarList().get(calendarId=self.calendar_id).execute()
        return calendar_resource['defaultReminders'][0]       #REVIEW: Retrieve reminder 'method' as well?


    def get_upcoming_events(self, starting_time: str, number_of_events: int):
        """
        Prints the start and name of the next n events on the user's calendar.
        """
        if number_of_events <= 0:
            raise ValueError("Number of events must be at least 1")

        events_response = self.api.events().list(calendarId=self.calendar_id, timeMin=starting_time,
                                                 maxResults=number_of_events, singleEvents=True,
                                                 orderBy='startTime').execute()

        self.event_reminder_defaults = events_response['defaultReminders'][0]    #REVIEW: Retrieve reminder 'method' as well?
        return events_response.get('items', [])


    def _get_events_from_year(self, years):
        """
        Get events within specified year limit
            positive for years to the future, negative for years in the past
        """
        time_now = datetime.datetime.utcnow()
        change_date = time_now + relativedelta(years=years)

        time_min = get_date_iso(min(time_now, change_date))
        time_max = get_date_iso(max(time_now, change_date))

        events_response = self.api.events().list(calendarId=self.calendar_id, singleEvents=True,
                                                 orderBy='startTime', timeMin=time_min,
                                                 timeMax=time_max).execute()

        self.event_reminder_defaults = events_response['defaultReminders'][0]     #REVIEW: Retrieve reminder 'method' as well?
        return events_response.get('items', [])


    def get_past_events(self, years_past: int = DEFAULT_PAST_YEAR_RANGE):
        """
         Get events within specified year limit in the past
        """
        if years_past < 0:
            raise ValueError("Year Input cannot be negative")

        year_input = - years_past
        return self._get_events_from_year(year_input)


    def get_future_events(self, years_future: int = DEFAULT_FUTURE_YEAR_RANGE):
        """
         Get events within specified year limit in the future
        """
        if years_future < 0:
            raise ValueError("Year Input cannot be negative")
        return self._get_events_from_year(years_future)


    def get_events_with_reminders(self, events):
        """
        Get reminders under a given event, provided the list of events
        """
        for event in events:
            if event['reminders']['useDefault']:
                event['reminders'] = [self.reminder_defaults]
            else:
                try:
                    event['reminders']['overrides'] 
                except KeyError:
                    event['reminders'] = []
                else:
                    event['reminders'] = event['reminders']['overrides']

        return events


    def get_event_reminder(self, event):
       if event['reminders']['useDefault']:
            event['reminders'] = [self.reminder_defaults]
            try:
                event['reminders']['overrides'] 
            except KeyError:
                event['reminders'] = []
            else:
                event['reminders'] = event['reminders']['overrides']
       return event


    def navigate_to_events(self, time):
        events = self.get_past_events()
        events += self.get_future_events()
        resultList = []
        for event in events:
            eventTime = event['start']['dateTime'].split('T', 1)
            if time in eventTime[0]:
                result = 'Event:' + event['summary'] + ' at ' + event['start'].get('dateTime',
                                                                                   event['start'].get('date'))
                if event['reminders']['useDefault']:
                    result += 'Reminder in 10 minutes before event'
                else:
                    for reminder in event['reminders']['overrides']:
                        result += 'Reminder in ' + str(reminder['minutes']) + ' minutes before event as ' + reminder['method']
                resultList.append(result)
        if len(resultList) < 1:
            resultList = "Nothing showed up in your search"
        return resultList
        

    def search_events(self, keyword: str):
        """"
        Allows the user to search for events
        """
        events = []
        events += self.get_past_events()
        events += self.get_future_events()
        resultList = []

        for event in events:
            if keyword.lower() in event['summary'].lower():
                result = 'Event:' + event['summary'] + ' at ' + event['start'].get('dateTime', event['start'].get('date'))
                if event['reminders']['useDefault']:
                    result += 'Reminder in 10 minutes before event'
                else:
                    for reminder in event['reminders']['overrides']:
                        result += 'Reminder in ' + str(reminder['minutes']) + ' minutes before event as ' + reminder['method']
                resultList.append(result)
        if len(resultList) < 1:
            resultList.append("Nothing showed up in your search")
        return resultList

    def delete_events(self, event):
        eventId = event['id']
        self.api.events().delete(calendarId=self.calendar_id, eventId=eventId).execute()


def get_date_iso(date_str: str):
    """
    :param: date_str should be in utc format
    """
    return date_str.isoformat() + 'Z'


def main():
    primary_calendar = Calendar(get_calendar_api())
    print(primary_calendar.get_events_with_reminders(primary_calendar.get_future_events()))

    # print('Please enter your choice')
    # print('1. View past events.')
    # print('2. View future events')
    # print('3. Feature 3')
    # print('4. Search for an event and reminders')
    # print('5. Delete an event and reminders')
    # print('6. Exit')

    # time_now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

    # choice = input('Your choice as an integer: ')

    # events = primary_calendar.get_upcoming_events(time_now, 10)
    # # events = primary_calendar.get_past_events()
    # # events = primary_calendar.get_future_events()
    # x = input("Enter date for search: ")

    # while len(x) < 2:
    #     print("Keyword should be at least 2 characters long")
    #     x = input("Enter Keyword: ")
    # print(primary_calendar.navigate_to_events(x))
    # if not events:
    #     print('No upcoming events found.')

    # i = 0
    # for event in events:
    #     i += 1
    #     start = event['start'].get('dateTime', event['start'].get('date'))
    #     print(i, start, event['summary'])


if __name__ == "__main__":  # Prevents the main() function from being called by the test suite runner
    main()

# Requirements --------------------------------
#   Events, reminders 5 years past, 2 years future least; all events
#   Navigate through days, months, years, view details of events (events, reminders)
#   Send invitations to attendees with student.monash.edu address
#          Do not support other emails
#   Search events and reminders using different keywords
#   Delete events and reminders

