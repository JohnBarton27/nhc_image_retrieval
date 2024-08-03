import argparse
from datetime import datetime
import feedparser
import pytz
import requests

from lib.rss_entry import RssEntry

parser = argparse.ArgumentParser(description="Gets the latest uncertainty track (or relevant image) for active storm.")
parser.add_argument("--output", help="Output file name (defaults to output.png)", default="output.png")
args = parser.parse_args()

url = "https://www.nhc.noaa.gov/index-at.xml"


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

            image_response = requests.get(entry.uncertainty_track_image_url)
            if image_response.status_code != 200:
                print("Failed to retrieve uncertainty track!")
                continue

            with open(args.output, "wb") as img_file:
                img_file.write(image_response.content)


if __name__ == "__main__":
    main()
