import hassapi as hass

from datetime import datetime
import feedparser
import os
import pytz
import requests

from nhc_image_retrieval.lib.rss_entry import RssEntry

IMAGE_PATH = "/homeassistant/www/hurricane_cone.png"
DEFAULT_IMAGE_URL = "https://www.nhc.noaa.gov/xgtwo/two_atl_0d0.png"


def download_uncertainty_cone_image(entity, attribute, old, new, kwargs):
    rss_feed_url = "https://www.nhc.noaa.gov/index-at.xml"

    feed = feedparser.parse(rss_feed_url)

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

            download_image(entry.uncertainty_track_image_url)
            return

    # Never found an active storm with available graphics
    download_image(DEFAULT_IMAGE_URL)


def download_image(image_url):
    image_response = requests.get(image_url)
    if image_response.status_code != 200:
        print("Failed to retrieve uncertainty track!")
        return

    if os.path.exists(IMAGE_PATH):
        print("Image already exists!")

    with open(IMAGE_PATH, "wb") as img_file:
        print("Writing updated image file!")
        img_file.write(image_response.content)


class DownloadNhcImage(hass.Hass):

    def initialize(self):
        self.log("Hello!")
        self.listen_state(download_uncertainty_cone_image, "input_datetime.last_nhc_update")

