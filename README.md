# McD-Cal-Generator

This was an app I created for myself to automatically add my scheduled work shifts to my google calendar. It searches for the last email by a specific sender
(the automated email that sends you your schedule), and it reads the info in as plain text and converts the pertinent information into google calendar type events
and adds them to the google calendar of the account specified. It requires readonly email permissions from the account you are reading info from, and read-write
permissions on the account you are adding the google calendar events to(The reason it isn't writeonly is because it reads the calendar to make sure it isnt creating
a duplicate event). Both emails must be google users.

If I were writing this again, I would have it create ICS files for the events rather than uploading to google calendar, but I did not know about that file type at the 
time. This way the user could chose to add the calendar events to any calendar service. 

This project gave me good experience working with Google Cloud Console and accessing Googles Gmail and Google Calendar APIs.


Requires OAuth Credentials from Google Cloud Project (Not included in github). Named "gcalcredentials.json" and "gmailcredentials.json" respectively

Also, need to run the following commands:

"pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib"

It's worth noting that this GitHub is merely a proof of concept for most people and will not work as intended without modifications. This worked for me but I didn't bother to make it work for a general use case given that the core program is already catered to search for VERY specific criteria in a weekly schedule email. As such,  the email must already be automated and constructed in a very specific way for this to work, so theres no point solving the other commutability issues when this main flaw is something that can't be resolved. Also, users would have to create their own project & credentials or be authorized manually to my Google Cloud Console project in developer mode, because otherwise I would have to pay money. This is a tedious process, and as such I decided I did not need to make the program work for anybody else but me, since it would require either money or technical knowledge to get to work for even my own co-workers.
