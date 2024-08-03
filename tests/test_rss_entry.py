from datetime import datetime

import pytz

from nhc_image_retrieval.lib.rss_entry import RssEntry


def test_get_from_json_happy_path():
    happy_json = {
        "title": "A simple title!",
        "summary": "This is a summary",
        "published": "Sat, 03 Aug 2024 11:36:56 GMT"
    }

    entry = RssEntry.get_from_json(happy_json)

    assert entry.title == "A simple title!"
    assert entry.summary == "This is a summary"
    assert entry.published == datetime(year=2024, month=8, day=3, hour=11, minute=36, second=56, tzinfo=pytz.utc)


def test_get_from_json_missing_attributes():
    happy_json = {}

    entry = RssEntry.get_from_json(happy_json)

    assert entry.title is None
    assert entry.summary is None
    assert entry.published is None
