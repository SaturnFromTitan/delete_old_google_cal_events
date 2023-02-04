"""
Copied from
https://developers.google.com/calendar/api/quickstart/python?hl=de#configure_the_sample
& increased scope

Use this script to give the file sufficient credentials
"""
from __future__ import print_function

import datetime

from dotenv import dotenv_values
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar"]

CONFIG = dotenv_values(".env")
CALENDAR_ID = CONFIG["CALENDAR_ID"]
DATE = datetime.datetime.strptime(CONFIG["DATE"], "%Y-%m-%d")
QUERY = CONFIG["QUERY"]


def main():
    client = get_events_client()
    params = {
        "calendarId": CALENDAR_ID,
        "timeMax": DATE.isoformat() + "Z",
        "q": QUERY,
        "singleEvents": True,
    }
    events = list_all_pages(client, params)

    print("Number of events:", len(events))
    print("Unique summaries:", {event["summary"] for event in events})

    dates = sorted({event["start"]["dateTime"] for event in events})
    print("Earliest date:", max(dates))
    print("Latest date:", min(dates))

    for event in events:
        delete_event(client, calendar_id=CALENDAR_ID, event_id=event["id"])


def get_events_client():
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    calendar_client = build("calendar", "v3", credentials=creds)
    return calendar_client.events()


def delete_event(client, calendar_id, event_id):
    client.delete(calendarId=calendar_id, eventId=event_id).execute()


def list_all_pages(client, params):
    result = list()
    page_token = None
    while True:
        events = client.list(
            **params,
            pageToken=page_token,
        ).execute()

        items = events["items"]
        result.extend(items)

        page_token = events.get("nextPageToken")
        if not page_token:
            break
    return result


if __name__ == "__main__":
    main()
