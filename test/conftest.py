import os

import pytest
from pytest_postgresql import factories
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.database_pipeline_tools.letterboxd_rss_parser import LetterBoxdRss

postgresql_my_proc = factories.postgresql_proc(port=None, unixsocketdir='/var/run')

postgresql_my = factories.postgresql('postgresql_my_proc')

path = os.path.join(os.path.dirname(__file__), "letterboxd_rss_feed_test.xml")


@pytest.fixture(scope='function')
def dataset():
    engine = create_engine("postgresql+psycopg2://admin:admin@localhost/travis_ci_test")
    Session = sessionmaker(bind=engine)
    Base = declarative_base()
    obj = LetterBoxdRss(feed_url=path, base=Base, engine=engine, session=Session)
    obj.feed_db_pipeline()
