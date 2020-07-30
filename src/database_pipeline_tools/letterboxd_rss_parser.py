import logging

import feedparser
from src.database_pipeline_tools.base import Base, engine, Session
from src.database_pipeline_tools.models import MovieDatabase, sha_gen, ExtensionIMDB
import imdb

logging.getLogger("imdb").setLevel(logging.WARNING)
logging.basicConfig(level=logging.INFO)


class LetterBoxdRss:

    def __init__(self, feed_url: str = "None"):
        """
        This class is meant to be a one stop tool box for anything
        concerning to do with letterboxd RSS Feed and your local DB.

        Has methods to parse your RSS Feed, join relevant IMDB data
        and write it to your local db.

        :param feed_url: Your RSS Feed url
        """
        feed = feedparser.parse(feed_url)
        self.entries = feed.entries
        self.feed_len = len(self.entries)
        self.type_entry = dict()
        Base.metadata.create_all(engine)
        self.session = Session()
        self.imdb_obj = imdb.IMDb()
        self.all_letterbox_sha = None

    def feed_db_pipeline(self):
        """
        Parses your feed, joins with IMDB data and writes to database.
        """
        self.all_letterbox_sha = self._get_all_letterbox_sha()
        self._entry_sorter_()
        self._add_imdb_id()
        self._add_to_db()

    def _entry_sorter_(self):
        """
        Segregates the items of the RSS Feed based on the type.
        """
        type_of = set()
        for item in self.entries:
            id_value = item.get("id").split('-')
            type_item = id_value[1]
            logging.debug(f"Reading item \"{item.get('title')}\" in entry_sorter")
            if type_item in type_of:
                self.type_entry[type_item].add(item)
            else:
                self.type_entry[type_item] = {item}
                type_of.add(type_item)

    def _add_imdb_id(self):
        """
        Adds IMDB ID to the a `watch` entry.
        Picks first from the result and is not always guaranteed to be correct.
        Until LetterBoxd has a reverse lookup, this is the best I have.
        """
        for item in self.type_entry.get("watch"):
            title = item.get("letterboxd_filmtitle")
            year = item.get("letterboxd_filmyear")
            watch_date = item.get("letterboxd_watcheddate")
            sha_generated = sha_gen(title, watch_date)
            try:
                if title and sha_generated not in self.all_letterbox_sha:
                    movie = (self.imdb_obj.search_movie(f"{title} ({year})")[0])
                    movie_id = movie.getID()
                    item["IMDB_ID"] = movie_id
                    logging.info(f"IMDB id used for {title} is {movie_id}")
            except Exception as e:
                logging.warning(f"Exception Caught for movie {title}. Exception: {e}")
                continue

    def _get_all_imdb_ids(self) -> set:
        """
        :return: set containing all IMDB ids in database
        """
        query = self.session.query(ExtensionIMDB.imdb_id)
        imdb_ids = query.all()
        all_imdb_ids = set([r for r, in imdb_ids])
        return all_imdb_ids

    def get_imdb_details(self, movie_id: str) -> dict:
        """
        Creates a dictionary with all necessary IMDB values compatible with ExtensionIMDB (models.py)
        :param movie_id: The IMDB ID (str)
        :return: Relevant IMDB values (dict)
        """
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
            imdb_args["runtimes"] = int(value[0])
        imdb_args["imdb_id"] = movie_id
        return imdb_args

    def _get_all_letterbox_sha(self):
        """
        :return: set containing all SHA's in the database
        """
        query = self.session.query(MovieDatabase.sha)
        existing_sha = query.all()
        existing_sha = set([r for r, in existing_sha])
        return existing_sha

    def _add_to_db(self):
        """
        Checks if entry is already in database. If so, skips writing it again.
        Checks if entry already has an IMDB entry. If so, skips writing an extra IMDB entry.
        """
        imdb_ids = self._get_all_imdb_ids()
        sha_so_far = set()
        imdb_ids_so_far = dict()

        for item in self.type_entry.get("watch"):
            sha_generated = sha_gen(item.get("letterboxd_filmtitle"), item.get("letterboxd_watcheddate"))
            if sha_generated not in self.all_letterbox_sha and sha_generated not in sha_so_far:
                imdb_id = item.get("IMDB_ID")
                if imdb_id and imdb_id not in imdb_ids and imdb_id not in imdb_ids_so_far:
                    imdb_args = self.get_imdb_details(imdb_id)
                    imdb_db_obj = ExtensionIMDB(**imdb_args)
                    item["imdb_db_obj"] = imdb_db_obj
                    imdb_ids_so_far[imdb_id] = imdb_db_obj
                elif imdb_id in imdb_ids_so_far:
                    item["imdb_db_obj"] = imdb_ids_so_far[imdb_id]
                movie_obj = MovieDatabase(**item)
                self.session.add(movie_obj)
                logging.info(f"{item.get('letterboxd_filmtitle')} watched on {item.get('letterboxd_watcheddate')} "
                             f"added to be database. Relevant IMDB ID : {imdb_id}. Relevant SHA: {sha_generated}"
                             f"IMDB Link: https://www.imdb.com/title/tt{imdb_id}/")
                sha_so_far.add(sha_generated)

        self.session.commit()
        self.session.close()

    def correct_imdb_entry(self, sha: str, wrong_id: str, correct_id: str, delete_imdb_id: bool = False) -> None:
        """
        Sometimes a wrong IMDB is joined. For those cases, we can manually correct the ID.
        :param sha: SHA from the database (str)
        :param wrong_id: Wrong ID joined. Just a check (str)
        :param correct_id: Correct ID manually looked up. (str)
        :param delete_imdb_id: Delete the wrong IMDB entry. (bool, default is False)
        """
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
    obj = LetterBoxdRss(feed_url="https://letterboxd.com/naveenpiedy/rss")
    obj.feed_db_pipeline()
    # obj.correct_imdb_entry("b256ac175e487d230a02b6ed074becf81a85fa74", None, "1606183", delete_imdb_id=True)
    # #obj.correct_imdb_entry("5e7b10b98624ff14df350ad77728665b8c52725c", "11462134", "2527338", delete_imdb_id=True)
