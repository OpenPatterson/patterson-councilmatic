from datetime import datetime
from bs4 import BeautifulSoup
import urllib.request
import ssl
import json
import logging

# DELETE THIS?
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

RSS_FEED_URL = "https://pattersonca.iqm2.com/Services/RSS.aspx?Feed=Calendar"
PAGE_URL = "https://pattersonca.iqm2.com/Citizens/calendar.aspx"
MEETING_URL = "https://pattersonca.iqm2.com/Citizens/Detail_Meeting.aspx?ID="
BASE_URL = "https://pattersonca.iqm2.com/"
CAL_DIV_ID = "ContentPlaceholder1_pnlMeetings"
EVENT_CLASS = "Row MeetingRow"
EVENT_ALT_CLASS = "Row MeetingRow Alt"

# TODO:
#     GET DATE OF MEETING ✅
#     CANCELELED OR NOT? ✅
#     TYPE OF MEETING. REGULAR OR SPECIAL MEETING ✅
#     AGENDA LINK
#     AGENDA PACKET LINK
#     MINUTES LINK
#     SUMMARY LINK


def extract_events(url, calendar_id, event_class, event_alt_class):
    r = urllib.request.urlopen(url)
    soup = BeautifulSoup(r, "html.parser")
    calendar = soup.find("div", {"id": calendar_id})
    events = calendar.find_all("div", {"class": event_class})
    events_alt = calendar.find_all("div", {"class": event_alt_class})
    return events + events_alt


events = extract_events(PAGE_URL, CAL_DIV_ID, EVENT_CLASS, EVENT_ALT_CLASS)


def parse_events(events_list):
    meetings = []
    meetings_json = {}
    for event in events_list:
        meeting = {}
        date_string = event.find("div", {"class": "RowLink"}).text.strip()
        try:
            # meeting['date'] = datetime.strptime(date_string, '%b %d,
            #                                     %Y %I:%M %p')
            meeting['date'] = date_string
        except Exception as e:
            # meeting['date'] = datetime(0,0,0,0,0)
            meeting['date'] = "Jan 1, 2001 12:00 AM"
            print("Error when parsing date(", date_string, "). Error:", e)
        info = event.find("div", {"class": "RowLink"}).a['title'].split('\r')
        id = event.find("div", {"class": "RowLink"}).find(
            href=True)['href'].split('ID=')[1]
        meeting['meeting_id'] = id
        meeting['meeting_url'] = MEETING_URL + str(id)
        for elem in info:
            if 'Board' in elem:
                board = elem.replace('\t', ' ')
                meeting['board'] = board.split('Board: ')[1]
            elif 'Type' in elem:
                meeting_type = elem.replace('\t', ' ')
                meeting['meeting_type'] = meeting_type.split('Type: ')[1]
            elif 'Status' in elem:
                meeting_status = elem.replace('\t', ' ')
                meeting['status'] = meeting_status.split('Status: ')[1]
        meetings.append(meeting)
    meetings_json['meetings'] = meetings
    return meetings_json


json_meetings = parse_events(events)

output = open("../meetings.json", "w")
json.dump(json_meetings, output, indent=6)
