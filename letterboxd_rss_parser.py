import logging

import feedparser
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
        self.imdb_obj = imdb.IMDb()

    def feed_db_pipeline(self):
        self._entry_sorter_()
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
            try:
                if title and sha_generated not in existing_sha:
                    movie = (self.imdb_obj.search_movie(f"{title} ({year})")[0])
                    movie_id = movie.getID()
                    item["IMDB_ID"] = movie_id
            except Exception as e:
                logging.warning(f"Exception Caught for movie {title}. Exception: {e}")
                continue

    def get_all_imdb_ids(self):
        query = self.session.query(ExtensionIMDB.imdb_id)
        imdb_ids = query.all()
        all_imdb_ids = set([r for r, in imdb_ids])
        return all_imdb_ids

    def get_imdb_details(self, movie_id: str) -> dict:
        movie = self.imdb_obj.get_movie(movie_id)
        keys = ["genres", "rating", "votes", "title", "year", "runtimes", "languages"]
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
        sha_so_far = set()
        imdb_ids_so_far = dict()
        for item in self.type_entry.get("watch"):
            sha_generated = sha_gen(item.get("letterboxd_filmtitle"), item.get("letterboxd_watcheddate"))
            if sha_generated not in existing_sha and sha_generated not in sha_so_far:
                imdb_id = item.get("IMDB_ID")
                if imdb_id not in imdb_ids and imdb_id not in imdb_ids_so_far:
                    imdb_args = self.get_imdb_details(imdb_id)
                    imdb_db_obj = ExtensionIMDB(**imdb_args)
                    item["imdb_db_obj"] = imdb_db_obj
                    imdb_ids_so_far[imdb_id] = imdb_db_obj
                elif imdb_id in imdb_ids_so_far:
                    item["imdb_db_obj"] = imdb_ids_so_far[imdb_id]
                movie_obj = MovieDatabase(**item)
                self.session.add(movie_obj)
                sha_so_far.add(sha_generated)

        self.session.commit()
        self.session.close()

    def correct_imdb_entry(self, sha: str, wrong_id: str, correct_id: str, delete_imdb_id: bool = False) -> None:
        movie = self.session.query(MovieDatabase).filter(MovieDatabase.sha == sha).scalar()

        if movie.imdb_id == wrong_id:
            movie.imdb_id = correct_id
            imdb_data = self.get_imdb_details(correct_id)
            imdb_db_obj = ExtensionIMDB(**imdb_data)
            movie.imdb_db = imdb_db_obj

        if delete_imdb_id:
            self.session.query(ExtensionIMDB).filter(ExtensionIMDB.imdb_id == wrong_id).delete()

        self.session.commit()
        self.session.close()


if __name__ == '__main__':
    obj = LetterBoxdRss()
    obj.feed_db_pipeline()
    # obj.correct_imdb_entry("6d88bd1318b2f37a19bcce884ac0e01c9a20b7d8", "0272440", "0386422", delete_imdb_id=True)
    # #obj.correct_imdb_entry("5e7b10b98624ff14df350ad77728665b8c52725c", "11462134", "2527338", delete_imdb_id=True)
