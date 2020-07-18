import os
import pytest


from src.database_pipeline_tools.letterboxd_rss_parser import LetterBoxdRss

path = os.path.join(os.path.dirname(__file__), "letterboxd_rss_feed_test.xml")


@pytest.fixture(scope='function')
def dataset():
    obj = LetterBoxdRss(feed_url=path)
    obj.feed_db_pipeline()
