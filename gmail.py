from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from datetime import datetime

"""Locates newest email from specified sender and returns it"""


# If modifying these scopes, delete the file gmailtoken.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']#, 'https://www.googleapis.com/auth/calendar']



creds = None
# The file gmailtoken.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('gmailtoken.json'):
    creds = Credentials.from_authorized_user_file('gmailtoken.json', SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'gmailcredentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('gmailtoken.json', 'w') as token:
        token.write(creds.to_json())

service = build('gmail', 'v1', credentials=creds)

#
def getNewestEmailBySender(desiredSender):

    emailList = service.users().messages().list(userId='me').execute()['messages'] # Gets list of emails as list with email id and threadID
    for emailIds in emailList:

        email = service.users().messages().get(userId='me',id=emailIds['id']).execute()
        sender = 'Not Found'
        headers = email['payload']['headers']

        # Checks for sender in headers and stops once it is found
        for header in headers:
            if header['name'] == 'From':
                sender = header['value']
                break

        # Checks if sender is the desired sender which should be McDonalds. Once found, returns desired email
        if desiredSender in sender:
            return email



if __name__ == '__main__':
    startTime = datetime.now()
    getNewestEmailBySender('"mcd40367@ext.mcdonalds.com" <mcd40367@ext.mcdonalds.com>')
    totalTime = datetime.now()-startTime
    print("execution took " + str(totalTime))

