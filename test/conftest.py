import os

import pytest
from pytest_postgresql import factories
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database_pipeline_tools.base import Base
from src.database_pipeline_tools.letterboxd_rss_parser import LetterBoxdRss

postgresql_my_proc = factories.postgresql_proc(port=None, unixsocketdir='/var/run')

postgresql_my = factories.postgresql('postgresql_my_proc')

path = os.path.join(os.path.dirname(__file__), "letterboxd_rss_feed_test.xml")


@pytest.fixture(scope='function')
def setup_database(postgresql_my):

    def dbcreator():
        return postgresql_my.cursor().connection

    engine = create_engine('postgresql+psycopg2://', creator=dbcreator)
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)
    session = session()
    yield session
    session.close()


@pytest.fixture(scope='function')
def dataset(setup_database):
    obj = LetterBoxdRss(feed_url=path)
    obj.feed_db_pipeline()
