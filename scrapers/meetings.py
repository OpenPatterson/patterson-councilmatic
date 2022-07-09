# %%
from datetime import datetime
from bs4 import BeautifulSoup
import urllib.request
import ssl
if hasattr(ssl, '_create_unverified_context'): # Should only be needed when developing locally
    ssl._create_default_https_context = ssl._create_unverified_context

RSS_FEED_URL = "https://pattersonca.iqm2.com/Services/RSS.aspx?Feed=Calendar"
PAGE_URL = "https://pattersonca.iqm2.com/Citizens/calendar.aspx"
CAL_DIV_ID = "ContentPlaceholder1_pnlMeetings"
EVENT_CLASS = "Row MeetingRow"
EVENT_ALT_CLASS = "Row MeetingRow Alt"

headers = {
    'HTTP_USER_AGENT': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.13) Gecko/2009073022 Firefox/3.0.13',
    'HTTP_ACCEPT': 'text/html,application/xhtml+xml,application/xml; q=0.9,*/*; q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded'
}
# %%
# TODO:
#     GET DATE OF MEETING 
#     CANCELELED OR NOT? 
#     TYPE OF MEETING. REGULAR OR SPECIAL MEETING 
#     AGENDA LINK 
#     AGENDA PACKET LINK 
#     MINUTES LINK 
#     SUMMARY LINK 

def extract_events(url, calendar_id, event_class, event_alt_class):
    r = urllib.request.urlopen(url) 
    soup = BeautifulSoup(r, "html.parser")
    calendar = soup.find("div", {"id":calendar_id})
    events = calendar.find_all("div",{"class": event_class})
    events_alt = calendar.find_all("div",{"class": event_alt_class})
    return events + events_alt
events = extract_events(PAGE_URL, CAL_DIV_ID, EVENT_CLASS, EVENT_ALT_CLASS)

def parse_events(events_list):
    for event in events_list:
        date_string = event.find("div", {"class":"RowLink"}).text.strip()
        try:
            date = datetime.strptime(date_string, '%b %d, %Y %I:%M %p')
        except Exception as e:
            date = datetime(0,0,0,0,0)
            print("Error when parsing date(", date_string, "). Error:", e)
        info = event.find("div", {"class":"RowLink"}).a['title'].split('\r')
        for elem in info:
            if 'Board' in elem:
                board = elem.replace('\t', ' ')
            elif 'Type' in elem:
                meeting_type = elem.replace('\t', ' ')
            elif 'Status' in elem:
                meeting_status = elem.replace('\t', ' ')
                meeting_status = meeting_status.split('Status: ')[1]
                
        # print(date)
        # print(board)
        # print(meeting_type)
        print(meeting_status)

parse_events(events)

# %%
# TODO Create event/meeting class?