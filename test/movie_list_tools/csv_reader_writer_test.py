import unittest
import os
from datetime import datetime

from src.movie_list_tools.dataclass_helpers import ListMovieObject, ListMovieMetadata
from src.movie_list_tools.csv_reader_writer import MovieListCSVReader, MovieListCSVWriter

path = os.path.join(os.path.dirname(__file__), "test_csvs")


class CSVReaderTest(unittest.TestCase):

    def test_read_csv(self):
        mlcr = MovieListCSVReader(directory=path, list_name="list1.csv")
        list_items = mlcr.read_list_csv()
        lmd = ListMovieMetadata(date=datetime.strptime("2020-04-13", '%Y-%m-%d').date(), name='list_1',
                                url='https://letterboxd.com/test_user/list/list_1/', description='')
        expected = {'The Nice Guys': ListMovieObject(position=1, name='The Nice Guys', year=2016,
                                                     url='https://letterboxd.com/film/the-nice-guys/',
                                                     metadata=lmd,
                                                     description=''),
                    'True Lies': ListMovieObject(position=2, name='True Lies', year=1994,
                                                 url='https://letterboxd.com/film/true-lies/',
                                                 metadata=lmd,
                                                 description='')}

        self.assertEqual(expected, list_items)

    def test_wrong_directory(self):
        obj = MovieListCSVReader(directory="", list_name="list1.csv")
        self.assertRaises(FileNotFoundError, obj.read_list_csv)

    def test_wrong_list_name(self):
        obj = MovieListCSVReader(directory="", list_name="list1.csv")
        self.assertRaises(FileNotFoundError, obj.read_list_csv)

    def test_empty_list_file(self):
        obj = MovieListCSVReader(directory=path, list_name="list4.csv")
        self.assertRaises(Exception, obj.read_list_csv)


class CSVWriterTest(unittest.TestCase):

    def test_write_csv(self):

        lmd = ListMovieMetadata(date=datetime.strptime("2020-04-13", '%Y-%m-%d').date(), name='list_1',
                                url='https://letterboxd.com/test_user/list/list_1/', description='')
        list_items = {'The Nice Guys': ListMovieObject(position=1, name='The Nice Guys', year=2016,
                                                       url='https://letterboxd.com/film/the-nice-guys/',
                                                       metadata=lmd,
                                                       description=''),
                      'True Lies': ListMovieObject(position=2, name='True Lies', year=1994,
                                                   url='https://letterboxd.com/film/true-lies/',
                                                   metadata=lmd,
                                                   description='')}

        mlcw = MovieListCSVWriter(directory=path, list_items=list_items)

        mlcw.write_list_csv()

        with open(os.path.join(path, "output", "list_1_output.csv"), 'r') as output,\
                open(os.path.join(path, "lists", "list1.csv"), 'r') as input_:
            self.assertEqual(output.readlines(), input_.readlines())

    def test_none_items(self):
        obj = MovieListCSVWriter(directory=path, list_items={})
        self.assertRaises(Exception, obj.write_list_csv)

    def test_none_path(self):
        obj = MovieListCSVWriter(directory="", list_items={})
        self.assertRaises(Exception, obj.write_list_csv)


if __name__ == '__main__':
    unittest.main()
