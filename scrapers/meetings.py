# %%
import requests
from bs4 import BeautifulSoup


RSS_FEED_URL = "https://pattersonca.iqm2.com/Services/RSS.aspx?Feed=Calendar"
PAGE_URL = "https://pattersonca.iqm2.com/Citizens/calendar.aspx"
DIV = "ContentPlaceholder1_pnlMeetings"

# %%
r = requests.get(PAGE_URL)
soup = BeautifulSoup(r.text, "html.parser")
soup

