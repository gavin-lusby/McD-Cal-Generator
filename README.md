# McD-Cal-Generator

This was an app I created for myself to automatically add my scheduled work shifts to my google calendar. It searches for the last email by a specific sender
(the automated email that sends you your schedule), and it reads the info in as plain text and converts the pertinent information into google calendar type events
and adds them to the google calendar of the account specified. It requires readonly email permissions from the account you are reading info from, and read-write
permissions on the account you are adding the google calendar events to(The reason it isn't writeonly is because it reads the calendar to make sure it isnt creating
a duplicate event). Both emails must be google users.

If I were writing this again, I would have it create ICS files for the events rather than uploading to google calendar, but I did not know about that file type at the 
time. This way the user could chose to add the calendar events to any calendar service. 

This project gave me good experience working with Google Cloud Console and accessing Googles Gmail and Google Calendar APIs.


Requires OAuth Credentials (Not included in github)

Also, need to run the following commands:

"pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib"
