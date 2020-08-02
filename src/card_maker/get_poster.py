import requests
import os
import json

from pprint import pprint

from os.path import join
from dotenv import load_dotenv

dotenv_path = join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
load_dotenv(dotenv_path)

URL_V3 = "https://api.themoviedb.org/3"
BEARER_KEY = "Bearer {}".format(os.environ.get('tmdb_bearer'))
CONTENT_TYPE = "application/json;charset=utf-8"
HEADER_PAYLOAD = {"Authorization": BEARER_KEY, "content-type": CONTENT_TYPE}


def get_image_url():
    response = requests.get(URL_V3 + "/configuration", headers=HEADER_PAYLOAD)
    response_json = json.loads(response.text)
    # pprint(response_json)
    return response_json["images"]["base_url"]


def get_poster(imdb_id):
    base_path = get_image_url()
    url = f"{URL_V3}/find/tt{imdb_id}?&language=en-US&external_source=imdb_id"
    response = requests.get(url, headers=HEADER_PAYLOAD)
    response_json = json.loads(response.text)
    movie_data = response_json.get("movie_results").pop()
    pprint(movie_data)
    get_images(movie_data.get("id"))
    poster_string = f"{base_path}w600_and_h900_bestv2{movie_data.get('poster_path')}"
    print(poster_string)


def get_images(tmdb_id):
    url = f"{URL_V3}/movie/{tmdb_id}/videos"
    response = requests.get(url, headers=HEADER_PAYLOAD)
    response_json = json.loads(response.text)
    pprint(response_json)


if __name__ == '__main__':
    get_poster("1748122")
