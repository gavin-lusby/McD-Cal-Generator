# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START calendar_quickstart]
from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file gcaltoken.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

creds = None
# The file gcaltoken.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('gcaltoken.json'):
    creds = Credentials.from_authorized_user_file('gcaltoken.json', SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'gcalcredentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('gcaltoken.json', 'w') as token:
        token.write(creds.to_json())

service = build('calendar', 'v3', credentials=creds)


def doesEventExist(event):
    startTime = event['start']['dateTime']
    endTime = event['end']['dateTime']
    name = event['summary']

    now = datetime.datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(calendarId='primary', timeMin=startTime, timeMax=endTime,
                                          singleEvents=True, orderBy='startTime').execute()
    existing_event_list = events_result.get('items')

    if (startTime < now and endTime > now):
        print(
            "Event: \"" + name + "\" with start date " + startTime + " and end time " + endTime + " is currently in progress!")

    for event in existing_event_list:  # This only checks within the range of the start and end date of the event
        querySummary = event['summary']
        queryStart = event['start'].get('dateTime')
        queryEnd = event['end'].get('dateTime')

        if (querySummary == name and startTime == queryStart and endTime == queryEnd):
            if (startTime <= now and endTime > now):
                print(
                    "Event: \"" + name + "\" with start date " + startTime + " and end time " + endTime +
                    " already exists, and is currently in progress! Hurry!")
            elif (endTime <= now):
                print(
                    "Event: \"" + name + "\" with start date " + startTime + " and end time " + endTime +
                    " already exists, and has also already taken place.")
            elif(startTime > now):
                print(
                    "Event: \"" + name + "\" with start date " + startTime + " and end time " + endTime +
                    " already exists, and has not taken place yet.")

            return True

    if (startTime <= now and endTime > now):
        print(
            "Creating event: \"" + name + "\" with start date " + startTime + " and end time " + endTime +
            ". This event is in progress! Hurry!")
    elif (endTime <= now):
        print(
            "Creating event: \"" + name + "\" with start date " + startTime + " and end time " + endTime +
            ". This event has already taken place")
    elif (startTime > now):
        print(
            "Creating event: \"" + name + "\" with start date " + startTime + " and end time " + endTime +
            ". This event has not taken place yet.")
    return False


def createEvent(event):
    if doesEventExist(event):
        return

    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))


if __name__ == '__main__':
    main()
# [END calendar_quickstart]
