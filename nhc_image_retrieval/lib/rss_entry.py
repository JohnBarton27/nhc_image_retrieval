from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import requests


class RssEntry:

    def __init__(self, title: str, summary: str, published: datetime, raw: dict):
        self.title = title
        self.summary = summary
        self.published = published
        self.raw = raw

    def __repr__(self):
        return self.title

    def __str__(self):
        return self.summary

    @property
    def uncertainty_track_page_url(self):
        soup = BeautifulSoup(self.summary, "html.parser")

        img_tag = soup.find("img", alt=lambda alt: "Uncertainty Track Image" in alt)
        if img_tag and img_tag.find_parent("a"):
            return img_tag.find_parent("a")["href"]

        return None

    @property
    def uncertainty_track_image_url(self):
        # Must have an uncertainty track page in order to get the image
        if not self.uncertainty_track_page_url:
            return None

        uncertainty_page = requests.get(self.uncertainty_track_page_url)

        if uncertainty_page.status_code != 200:
            print("Failed to retrieve the uncertainty track page.")
            return None

        uncertainty_content = uncertainty_page.text
        soup = BeautifulSoup(uncertainty_content, "html.parser")
        img_tag = soup.find("img", id="coneimage")
        if img_tag:
            return f'https://nhc.noaa.gov{img_tag["src"]}'

        return None

    @staticmethod
    def __convert_to_eastern_time(date_str):
        if not date_str:
            return None

        gmt_datetime = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %Z")

        # Set the timezone to UTC
        return gmt_datetime.replace(tzinfo=pytz.utc)

    @classmethod
    def get_from_json(cls, json: dict):
        title = json.get("title")
        summary = json.get("summary")

        published_str = json.get("published")
        published = RssEntry.__convert_to_eastern_time(published_str)

        return cls(title, summary, published, json)
