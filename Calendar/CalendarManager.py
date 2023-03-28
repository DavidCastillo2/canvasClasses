from __future__ import print_function
import datetime
import pickle
import os.path

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from Calendar.Event import Event


class CalendarManager:
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    def _login(self):
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        
        #TODO credentials deleted from Google Console since this github is now public. Will have to remake, these do not work.
        if os.path.exists('Calendar/token.pickle'):
            with open('Calendar/token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'), self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('Calendar/token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        return build('calendar', 'v3', credentials=creds)

    def upcomingEvents(self, Max=30):
        service = self._login()

        # This goes backwards 1 day so HomeBase doesn't stack events that have already happened.
        shift = datetime.timedelta(days=1)
        now = (datetime.datetime.utcnow() - shift).isoformat() + 'Z'  # 'Z' indicates UTC time

        # Call the Calendar API
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=Max, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        return events, service

    def updateCalendar(self, assignmentsDict):
        upcomingEvents, service = self.upcomingEvents()
        toAdd = sortEvents(assignmentsDict, upcomingEvents)
        for event in toAdd:
            service.events().insert(calendarId='primary', body=event.body).execute()

        if len(toAdd) == 0:
            print("No new events found")
        else:
            print("%d Google events added successfully!" % len(toAdd))

    def clear(self):
        service = self._login()  # Authenticate future requests

        # This goes backwards 1 day so HomeBase doesn't stack events that have already happened.
        shift = datetime.timedelta(days=1)
        now = (datetime.datetime.utcnow() - shift).isoformat() + 'Z'  # 'Z' indicates UTC time

        # Get our events from google
        results = service.events().list(
            calendarId='primary', timeMin=now, maxResults=80, singleEvents=True,
            orderBy='startTime').execute()
        events = results.get('items', [])

        # Find automated events and delete them
        deleted = []
        for event in events:
            try:
                if event['description'] == 'Automated Event - David Castillo':
                    service.events().delete(calendarId="primary", eventId=event['id']).execute()
                    deleted.append(event)
            except KeyError:
                pass  # Just means event didn't have a description.

        # Print that we did things :)
        print('Events Deleted: %d' % len(deleted))
        print("Calendar Cleared!")


def sortEvents(assignmentsDict, events):
    retVal = []
    for courseTitle, assList in assignmentsDict.items():
        for ass in assList:
            addMe = True
            for curr in events:
                if curr['summary'] == ass.name + " - " + courseTitle:
                    # Event already exists in our calendar
                    addMe = False
                    break
            if addMe:
                # Event does not exist in our calendar
                e = Event(title=ass.name + " - " + courseTitle, startTime=ass.due_at, endTime=ass.due_at)
                retVal.append(e)
    return retVal




