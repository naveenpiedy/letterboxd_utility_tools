import feedparser
import pprint
from base import Base, engine, Session
from models import MovieDatabase
from sqlalchemy.orm import sessionmaker

class LetterBoxdRss:

    def __init__(self):
        feed = feedparser.parse("https://letterboxd.com/naveenpiedy/rss")
        self.entries = feed.entries
        self.feed_len = len(self.entries)
        self.type_entry = dict()
        self._entry_sorter_()
        self.add_to_db()

    def _entry_sorter_(self):
        type_of = set()
        for item in self.entries:
            id_value = item.get("id").split('-')
            type_item = id_value[1]
            if type_item in type_of:
                self.type_entry[type_item].add(item)
            else:
                self.type_entry[type_item] = {item}
                type_of.add(type_item)

    def add_to_db(self):
        Base.metadata.create_all(engine)
        session = Session()
        for item in self.type_entry.get("watch"):
            movie_obj = MovieDatabase(**item)
            sha_gen = movie_obj.sha_gen(item.get("letterboxd_filmtitle"), item.get("letterboxd_watcheddate"))
            exists = session.query(MovieDatabase).filter_by(sha=str(sha_gen)).count()
            if exists == 0:
                session.add(movie_obj)

        session.commit()
        session.close()


if __name__ == '__main__':
    obj = LetterBoxdRss()