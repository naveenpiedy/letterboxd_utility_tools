import json
import shutil

import requests
from jinja2 import Environment, FileSystemLoader

from src.card_maker.get_poster import get_image_url
from src.database_pipeline_tools.database_query_tool import DatabaseQueryTool
from os.path import join, dirname
from os import environ, remove
from dotenv import load_dotenv
from colorthief import ColorThief

dotenv_path = join(dirname(dirname(dirname(__file__))), '.env')
load_dotenv(dotenv_path)

URL_V3 = "https://api.themoviedb.org/3"
BEARER_KEY = "Bearer {}".format(environ.get('tmdb_bearer'))
CONTENT_TYPE = "application/json;charset=utf-8"
HEADER_PAYLOAD = {"Authorization": BEARER_KEY, "content-type": CONTENT_TYPE}


class CardMaker:
    __slots__ = "imdb_id"

    def __init__(self, *, imdb_id=None):
        self.imdb_id = imdb_id

    def get_content(self):
        return DatabaseQueryTool().query_db(json.dumps({'imdb_id': self.imdb_id}))

    @staticmethod
    def rotten(title):
        return title.lower().replace(' ', '_')

    def parse_content(self, query_results: dict, img_src: str, trailer_link: str) -> dict:
        query_results = next(iter(query_results.values()))
        imdb_info = query_results.get('imdb_info')
        movie = {'imgsrc': img_src, 'title': query_results.get('movie_title'),
                 'director': ', '.join(person for person in imdb_info.get('director')),
                 'cast': ', '.join(person for person in imdb_info.get('cast')[:5]),
                 'my_rating': query_results.get('my_rating'),
                 'genres': ', '.join(genre for genre in imdb_info.get('genres')),
                 'runtime': imdb_info.get('runtimes'),
                 'imdb_rating': imdb_info.get('rating'),
                 'trailer_link': trailer_link,
                 'imdb_link': f"https://www.imdb.com/title/{self.imdb_id}/",
                 'rotten_tomatoes_link':
                     f"https://www.rottentomatoes.com/m/{self.rotten(query_results.get('movie_title'))}"}

        return movie

    def get_media(self):
        base_path = get_image_url()
        url = f"{URL_V3}/find/tt{self.imdb_id}?&language=en-US&external_source=imdb_id"
        response = requests.get(url, headers=HEADER_PAYLOAD)
        response_json = json.loads(response.text)
        movie_data = response_json.get("movie_results").pop()
        trailer_string = f"https://youtu.be/{self.get_trailer_link(movie_data.get('id'))}"
        poster_string = f"{base_path}w600_and_h900_bestv2{movie_data.get('poster_path')}"
        return poster_string, trailer_string

    @staticmethod
    def get_trailer_link(tmdb_id):
        url = f"{URL_V3}/movie/{tmdb_id}/videos"
        response = requests.get(url, headers=HEADER_PAYLOAD)
        response_json = json.loads(response.text)
        for item in response_json.get('results'):
            if item.get('type') == 'Trailer' and item.get('site') == 'YouTube' and item.get('size') in (1080, 720):
                return item.get('key')

    @staticmethod
    def get_color(poster_path):
        response = requests.get(poster_path, stream=True)
        with open('img.png', 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response
        color_thief = ColorThief("img.png")
        # get the dominant color
        dominant_color = color_thief.get_color(quality=1)
        remove("img.png")
        return '#%02x%02x%02x' % dominant_color

    def make_card_html(self):
        query_results = json.loads(self.get_content())
        poster_link, trailer_link = self.get_media()
        content_dict = self.parse_content(query_results=query_results, img_src=poster_link, trailer_link=trailer_link)
        dominant_color = self.get_color(poster_link)
        file_loader = FileSystemLoader('templates')
        env = Environment(loader=file_loader)
        template = env.get_template('body.html')
        output = template.render(movie=content_dict, dom_color=dominant_color)
        print(output)


if __name__ == '__main__':
    CardMaker(imdb_id='0265666').make_card_html()
