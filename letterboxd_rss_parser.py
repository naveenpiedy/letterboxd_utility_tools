import feedparser
import pprint

from imdb.Person import Person

from base import Base, engine, Session
from models import MovieDatabase, sha_gen, ExtensionIMDB
import imdb


class LetterBoxdRss:

    def __init__(self):
        feed = feedparser.parse("https://letterboxd.com/naveenpiedy/rss")
        self.entries = feed.entries
        self.feed_len = len(self.entries)
        self.type_entry = dict()
        Base.metadata.create_all(engine)
        self.session = Session()
        self._entry_sorter_()
        self.imdb_obj = imdb.IMDb()
        self.add_imdb_id()
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

    def add_imdb_id(self):
        existing_sha = self.get_all_letterbox_sha()
        for item in self.type_entry.get("watch"):
            title = item.get("letterboxd_filmtitle")
            year = item.get("letterboxd_filmyear")
            sha_generated = sha_gen(item.get(title), item.get(year))
            if title and sha_generated not in existing_sha:
                movie = (self.imdb_obj.search_movie(f"{title} ({year})")[0])
                movie_id = movie.getID()
                item["IMDB_ID"] = movie_id

    def get_all_imdb_ids(self):
        query = self.session.query(ExtensionIMDB.imdb_id)
        imdb_ids = query.all()
        all_imdb_ids = set([r for r, in imdb_ids])
        return all_imdb_ids

    def get_imdb_details(self, movie_id):
        movie = self.imdb_obj.get_movie(movie_id)
        keys = ["genres", "rating", "votes", "title", "year", "runtimes"]
        person_keys = ["cast", "directors", "composers"]
        imdb_args = dict()
        for key in keys:
            imdb_args[key] = movie.get(key)

        for person_key in person_keys:
            value = movie.get(person_key)
            if value:
                value = value[:10]
                new_list = [i.get("name") for i in value]
                imdb_args[person_key] = new_list

        value = movie.get("runtimes")
        if value:
            imdb_args["runtimes"] = [int(i) for i in value]
        imdb_args["imdb_id"] = movie_id
        return imdb_args

    def get_all_letterbox_sha(self):
        query = self.session.query(MovieDatabase.sha)
        existing_sha = query.all()
        existing_sha = set([r for r, in existing_sha])
        return existing_sha

    def add_to_db(self):
        existing_sha = self.get_all_letterbox_sha()
        imdb_ids = self.get_all_imdb_ids()
        for item in self.type_entry.get("watch"):
            sha_generated = sha_gen(item.get("letterboxd_filmtitle"), item.get("letterboxd_watcheddate"))
            if sha_generated not in existing_sha:
                imdb_id = item.get("IMDB_ID")
                if imdb_id not in imdb_ids:
                    imdb_args = self.get_imdb_details(imdb_id)
                    imdb_db_obj = ExtensionIMDB(**imdb_args)
                    item["imdb_db_obj"] = imdb_db_obj
                movie_obj = MovieDatabase(**item)
                self.session.add(movie_obj)

        self.session.commit()
        self.session.close()


if __name__ == '__main__':
    obj = LetterBoxdRss()
