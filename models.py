import hashlib

from sqlalchemy import Column, String, Integer, Date, Float, Boolean, DateTime
from base import Base, engine
from datetime import datetime


class MovieDatabase(Base):
    __tablename__ = 'letterboxd_movie_diary'
    id = Column(Integer, primary_key=True)
    letter_boxd_id = Column(String)
    movie_title = Column(String)
    year_released = Column(Integer)
    my_rating = Column(Float)
    watchdate = Column(Date)
    letterboxd_link = Column(String)
    rewatch = Column(Boolean)
    published = Column(DateTime)
    sha = Column(String, unique=True)

    def __init__(self, **kwargs):
        self.letter_boxd_id = kwargs.get("id")
        self.movie_title = kwargs.get("letterboxd_filmtitle")
        self.year_released = kwargs.get("letterboxd_filmyear")
        self.my_rating = float(kwargs.get("letterboxd_memberrating"))
        self.watchdate = self.convert_date(kwargs.get("letterboxd_watcheddate"))
        self.letterboxd_link = kwargs.get("link")
        self.rewatch = self.convert_boolean(kwargs.get("letterboxd_rewatch"))
        self.published = self.convert_datetime(kwargs.get("published"))
        self.sha = self.sha_gen(kwargs.get("letterboxd_filmtitle"),
                                kwargs.get("letterboxd_watcheddate"))

    def sha_gen(self, movie_title, watchdate):
        wanted_sha = f"{movie_title}{watchdate}"
        return hashlib.sha1(wanted_sha.encode()).hexdigest()

    def convert_date(self, date_str):
        return datetime.strptime(date_str, "%Y-%m-%d").date()

    def convert_datetime(self, datetime_str):
        return datetime.strptime(datetime_str, "%a, %d %b %Y %H:%M:%S %z")

    def convert_boolean(self, boolean_str):
        if boolean_str == "Yes":
            return True
        else:
            return False


if __name__ == '__main__':
    db = MovieDatabase()
    db.create_table()
