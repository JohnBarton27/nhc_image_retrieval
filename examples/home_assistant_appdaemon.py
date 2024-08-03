import hassapi as hass

from datetime import datetime
import feedparser
import pytz
import requests

import nhc_image_retrieval
from nhc_image_retrieval.lib.rss_entry import RssEntry


def download_image(entity, attribute, old, new, kwargs):
    url = "https://www.nhc.noaa.gov/index-at.xml"

    feed = feedparser.parse(url)

    now = datetime.now(tz=pytz.utc)

    entries = feed.get("entries")
    for raw_entry in entries:
        entry = RssEntry.get_from_json(raw_entry)
        time_since_update = now - entry.published

        # Only grab an update from the past day
        if time_since_update.days >= 1:
            continue

        if "Graphics" in entry.title:
            if not entry.uncertainty_track_page_url:
                continue

            image_response = requests.get(entry.uncertainty_track_image_url)
            if image_response.status_code != 200:
                print("Failed to retrieve uncertainty track!")
                continue

            # TODO replace with filepath that works for your Home Assistant instance
            with open("/config/local_media_folder/hurricane_cone.png", "wb") as img_file:
                print("Writing updated image file!")
                img_file.write(image_response.content)
                break


class DownloadNhcImage(hass.Hass):

    def initialize(self):
        self.log("Hello!")
        # TODO tie this to the change in an input_datetime or some other sensor in your HA instance
        self.listen_state(download_image, "input_datetime.last_nhc_update")
