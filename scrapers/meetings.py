# %%
from email import message_from_string
import requests
from bs4 import BeautifulSoup
import urllib.request
import ssl
if hasattr(ssl, '_create_unverified_context'): # Should only be needed when developing locally
    ssl._create_default_https_context = ssl._create_unverified_context

RSS_FEED_URL = "https://pattersonca.iqm2.com/Services/RSS.aspx?Feed=Calendar"
PAGE_URL = "https://pattersonca.iqm2.com/Citizens/calendar.aspx"
DIV = "ContentPlaceholder1_pnlMeetings"

headers = {
    'HTTP_USER_AGENT': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.13) Gecko/2009073022 Firefox/3.0.13',
    'HTTP_ACCEPT': 'text/html,application/xhtml+xml,application/xml; q=0.9,*/*; q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded'
}


# %%
r = urllib.request.urlopen(PAGE_URL) 
soup = BeautifulSoup(r, "html.parser")
calendar = soup.find("div", {"id":"ContentPlaceholder1_pnlMeetings"})
row_items = calendar.find_all("div",{"class":"Row MeetingRow"})
row_items_alt = calendar.find_all("div",{"class":"Row MeetingRow Alt"})

len(row_items), len(row_items_alt)

# TODO:
#     GET DATE OF MEETING 
#     CANCELELED OR NOT? 
#     TYPE OF MEETING. REGULAR OR SPECIAL MEETING 
#     AGENDA LINK 
#     AGENDA PACKET LINK 
#     MINUTES LINK 
#     SUMMARY LINK 
# %%
row_items[0]
# %%
row_items_alt[0]
# %%
