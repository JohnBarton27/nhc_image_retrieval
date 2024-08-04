import hassapi as hass

from datetime import datetime
import feedparser
import os
import pytz
import requests

import nhc_image_retrieval
from nhc_image_retrieval.lib.rss_entry import RssEntry

IMAGE_PATH = "/homeassistant/www/hurricane_cone.png"


def download_image(entity, attribute, old, new, kwargs):
    url = "https://www.nhc.noaa.gov/index-at.xml"

    feed = feedparser.parse(url)

    now = datetime.now(tz=pytz.utc)

    entries = feed.get("entries")
    for raw_entry in entries:
        entry = RssEntry.get_from_json(raw_entry)
        time_since_update = now - entry.published
        if time_since_update.days >= 1:
            # Old update
            continue

        if "Graphics" in entry.title:
            if not entry.uncertainty_track_page_url:
                continue

            image_response = requests.get(entry.uncertainty_track_image_url)
            if image_response.status_code != 200:
                print("Failed to retrieve uncertainty track!")
                continue

            if os.path.exists(IMAGE_PATH):
                print("Image already exists!")

            with open(IMAGE_PATH, "wb") as img_file:
                print("Writing updated image file!")
                img_file.write(image_response.content)


class DownloadNhcImage(hass.Hass):

    def initialize(self):
        self.log("Hello!")
        self.listen_state(download_image, "input_datetime.last_nhc_update")