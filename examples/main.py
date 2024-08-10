import argparse
import os
from datetime import datetime
import feedparser
import pytz
import requests

from nhc_image_retrieval.lib.rss_entry import RssEntry

parser = argparse.ArgumentParser(description="Gets the latest uncertainty track (or relevant image) for active storm.")
parser.add_argument("--output", help="Output file name (defaults to output.png)", default="output.png")
args = parser.parse_args()

url = "https://www.nhc.noaa.gov/index-at.xml"
DEFAULT_IMAGE_URL = "https://www.nhc.noaa.gov/xgtwo/two_atl_0d0.png"


def main():
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

            download_image(entry.uncertainty_track_image_url)
            return

    # Never found an active storm with available graphics
    download_image(DEFAULT_IMAGE_URL)


def download_image(image_url):
    image_response = requests.get(image_url)
    if image_response.status_code != 200:
        print("Failed to retrieve uncertainty track!")
        return

    if os.path.exists(args.output):
        print("Image already exists!")

    with open(args.output, "wb") as img_file:
        print("Writing updated image file!")
        img_file.write(image_response.content)


if __name__ == "__main__":
    main()
