import hashlib

from sqlalchemy import Column, String, Integer, Date, Float, Boolean, DateTime, ForeignKey, ARRAY, BigInteger
from sqlalchemy.orm import relationship

from src.database_pipeline_tools.base import Base
from datetime import datetime


def sha_gen(movie_title, watchdate):
    wanted_sha = f"{movie_title}{watchdate}"
    return hashlib.sha1(wanted_sha.encode()).hexdigest()


class ExtensionIMDB(Base):
    __tablename__ = 'imdb_helper_db'

    id = Column(Integer, primary_key=True)
    imdb_id = Column(String, unique=True, index=True)
    main_db = relationship("MovieDatabase", back_populates="imdb_db")
    cast = Column(ARRAY(String))
    genres = Column(ARRAY(String))
    director = Column(ARRAY(String))
    rating = Column(Float)
    votes = Column(BigInteger)
    title = Column(String)
    year = Column(Integer)
    runtimes = Column(ARRAY(Integer))
    composers = Column(String)
    languages = Column(ARRAY(String))

    def __init__(self, **kwargs):
        self.imdb_id = kwargs.get("imdb_id")
        self.cast = kwargs.get("cast")
        self.genres = kwargs.get("genres")
        self.director = kwargs.get("directors")
        self.rating = kwargs.get("rating")
        self.votes = kwargs.get("votes")
        self.title = kwargs.get("title")
        self.year = kwargs.get("year")
        self.runtimes = kwargs.get("runtimes")
        self.composers = kwargs.get("composers")
        self.languages = kwargs.get("languages")


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
    sha = Column(String, unique=True, index=True)
    imdb_id = Column(String, ForeignKey('imdb_helper_db.imdb_id'))
    imdb_db = relationship("ExtensionIMDB", back_populates="main_db")

    def __init__(self, **kwargs):
        self.letter_boxd_id = kwargs.get("id")
        self.movie_title = kwargs.get("letterboxd_filmtitle")
        self.year_released = kwargs.get("letterboxd_filmyear")
        self.my_rating = float(kwargs.get("letterboxd_memberrating"))
        self.watchdate = self.convert_date(kwargs.get("letterboxd_watcheddate"))
        self.letterboxd_link = kwargs.get("link")
        self.rewatch = self.convert_boolean(kwargs.get("letterboxd_rewatch"))
        self.published = self.convert_datetime(kwargs.get("published"))
        self.sha = sha_gen(kwargs.get("letterboxd_filmtitle"),
                           kwargs.get("letterboxd_watcheddate"))
        self.imdb_id = kwargs.get("IMDB_ID")
        self.imdb_db = kwargs.get("imdb_db_obj")

    @staticmethod
    def convert_date(date_str):
        return datetime.strptime(date_str, "%Y-%m-%d").date()

    @staticmethod
    def convert_datetime(datetime_str):
        return datetime.strptime(datetime_str, "%a, %d %b %Y %H:%M:%S %z")

    @staticmethod
    def convert_boolean(boolean_str):
        if boolean_str == "Yes":
            return True
        else:
            return False
