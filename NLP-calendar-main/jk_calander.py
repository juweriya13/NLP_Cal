from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path
import pickle
import webbrowser

# Open Google Calendar in the default web browser
# webbrowser.open("https://calendar.google.com/")


SCOPES = ["https://www.googleapis.com/auth/calendar"]

def authenticate_google():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json")

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=8080)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds

creds = authenticate_google()
print("Authentication successful!")
webbrowser.open("https://calendar.google.com/")

from googleapiclient.discovery import build
import datetime

def get_calendar_events():
    service = build("calendar", "v3", credentials=authenticate_google())

    # Get current time
    now = datetime.datetime.utcnow().isoformat() + "Z"

    # Get the next 10 events
    events_result = service.events().list(
        calendarId="primary",
        timeMin=now,
        maxResults=10,
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    events = events_result.get("items", [])

    if not events:
        print("No upcoming events found.")
        return

    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        print(f"{start} - {event['summary']}")

# get_calendar_events()
from googleapiclient.discovery import build
import datetime

def authenticate_google():
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    import os.path

    SCOPES = ["https://www.googleapis.com/auth/calendar"]
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds

def create_calendar_event():
    service = build("calendar", "v3", credentials=authenticate_google())

    event = {
        "summary": "John Birthday Event",
        "location": "Online",
        "description": "13th birthday",
        "start": {
            "dateTime": "2025-08-30T10:00:00Z",  # Adjust time to your timezone
            "timeZone": "UTC",
        },
        "end": {
            "dateTime": "2025-08-30T11:00:00Z",
            "timeZone": "UTC",
        },
        "reminders": {
            "useDefault": False,
            "overrides": [
                {"method": "email", "minutes": 24 * 60},  # Reminder 1 day before
                {"method": "popup", "minutes": 30},  # Reminder 30 minutes before
            ],
        },
    }

    event_result = service.events().insert(calendarId="primary", body=event).execute()
    
    print(f"Event created: {event_result.get('htmlLink')}")

# Call the function to create an event
create_calendar_event()

