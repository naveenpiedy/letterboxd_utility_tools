# Letterboxd Utility Tools ![master badge](https://img.shields.io/travis/com/naveenpiedy/letterboxd_utility_tools/master.svg?logo=travis&labelColor=abcdef&color=03cffc&label=Master%20Build&link=https://travis-ci.com/naveenpiedy/letterboxd_utility_tools&style=for-the-badge)

Unofficial scripts to work with Letterboxd RSS feed and CSV's. From a pipeline to a DB to generating and sorting lists.

## Getting Started

I suppose people reading this will already have a [Letterboxd account](https://letterboxd.com/). Exporting your data could be done through [settings](https://letterboxd.com/settings/data/). If you still have trouble, a link to their [FAQ](https://letterboxd.com/about/frequent-questions/#:~:text=To%20export%20a%20list%20from,of%20creating%20a%20new%20list.) 

### Prerequisites

Scripts make use of dataclasses, so Python 3.7+.

This was was written on a Windows machine (Win10). Nothing OS specific was used. 

### Installing

Clone the project and install the requirements from requirement.txt using the following command.

```
pip install -r requirements.txt
```

If you want to make use of database scripts, you need [PostGresSQL](https://www.postgresql.org/download/).

Will update more instructions on how to get the DB set up (this is still a WIP). Minor changes to [config file](https://github.com/naveenpiedy/letterboxd_utility_tools/blob/master/src/database_pipeline_tools/base.py) should be all that is needed.  

## Using the scripts

This is still a work in progress. Will definitely add CLI support or at least a main script file to call other scripts.

For now, database scripts can be found under `src/database_pipeline_tools` [here](https://github.com/naveenpiedy/letterboxd_utility_tools/tree/master/src/database_pipeline_tools) and list tools under `src/movie_list_tools` [here](https://github.com/naveenpiedy/letterboxd_utility_tools/tree/master/src/movie_list_tools).

Alternatively you can refer to tests for now on how to run the scripts. If you need more info, feel free to reach me. 

## Running the tests

Tests were written using Python's unittest and is hooked up to Travis. Build status can be found on the top. If you want to run tests locally, running the following command from the root of the directory will suffice.

```
pytest
```
Tests are constantly being added to have better code coverage. 

### And coding style tests

For linting, flake8 is used. You could run it using the following command from the root of the directory. 

```
flake8
```

## Contributing

As of writing this, there is no definite contributing guide (Will add one later). Feel free to submit a feature request or open bug. If you have implemented it already, please submit a pull request for me to take a look.  

Please read [CODE_OF_CONDUCT.md](https://github.com/naveenpiedy/letterboxd_utility_tools/blob/master/CODE_OF_CONDUCT.md) for details on our code of conduct.

## Authors

* **[Naveen Piedy](https://github.com/naveenpiedy)** - *Initial work* - [Letter Boxd Utility Tools](https://github.com/naveenpiedy/letterboxd_utility_tools)

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/naveenpiedy/letterboxd_utility_tools/blob/master/LICENSE) file for details

## Acknowledgments

* For [LetterBoxd](https://letterboxd.com/) being such a great website for movie lovers.
* To that one Reddit Thread asking if there was a script to merge sort a movie list.
* And for 2020, for giving me time and motivation to finally do my pet project. 
* etc
