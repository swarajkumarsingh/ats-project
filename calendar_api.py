import utils
import os.path
from datetime import datetime

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow


def get():
  SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
  creds = None
  if os.path.exists("token_read.json"):
    creds = Credentials.from_authorized_user_file("token_read.json", SCOPES)
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    with open("token_read.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("calendar", "v3", credentials=creds)

    now = datetime.utcnow().isoformat() + "Z"
    print("Getting the upcoming 10 events")
    events_result = (
        service.events().list(calendarId="primary",timeMin=now,maxResults=10,singleEvents=True,orderBy="startTime",).execute()
    )
    events = events_result.get("items", [])

    if not events:
      print("No upcoming events found.")
      return

    for event in events:
      start = event["start"].get("dateTime", event["start"].get("date"))
      print(event)

  except HttpError as error:
    print(f"An error occurred: {error}")


def create(candidateName, candidateEmail):
  SCOPES = ['https://www.googleapis.com/auth/calendar.events']

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

  try:
    service = build("calendar", "v3", credentials=creds)
  except Exception as e:
    print("Unable to create calender service")
  today_date = datetime.now().strftime('%Y-%m-%d')
  event = {
      'summary': 'Interview Meeting',
      'location': 'Virtual',
      'description': f"Interview with candidate {candidateName}: {candidateEmail}",
      'colorId': 6,
      'start': {
          'date': today_date,
          'timeZone': 'Asia/Kolkata',
      },
      'end': {
          'date': today_date,
          'timeZone': 'Asia/Kolkata',
      },
      'attendees': [{'email': candidateEmail}],
      'conferenceData': {
          'createRequest': {
              'requestId': utils.generate_random_string(),
              'conferenceSolutionKey': {
                  'type': 'hangoutsMeet'
              },
          },
      },
      'reminders': {
          'useDefault': False,
          'overrides': [
              {'method': 'email', 'minutes': 24 * 60},
              {'method': 'popup', 'minutes': 10},
          ],
      },
  }
  try:
      event = service.events().insert(calendarId='primary', body=event, conferenceDataVersion=1, sendUpdates='all').execute()
      print(f"Event created successfully. Event Link: {event.get('htmlLink')}")
      return event
  except HttpError as error:
    print(f"An error occurred: {error}")
