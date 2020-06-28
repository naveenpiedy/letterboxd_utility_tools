import csv
from dataclasses import dataclass
from datetime import date


@dataclass
class MovieObject:
    position: int
    name: str
    year: date
    url: str
    description: str = ''


class MovieListMergeSorter:

    def __init__(self, file_location: str):
        """
        The __init__ function should perform end to end operation from reading the CSV to sorting to generating a csv.
        """
        self.file_location = file_location
        self.item_dicts = dict()
        self.sorted_dict = dict()
        self.movie_names = list()
        self.first_lines = []
        self._perform_merge_sort()

    def _read_csv(self):
        """
        Reads LetterBoxd List csv. Preserves first four lines containing list metadata in self.first_lines
        for csv generation later.
        """
        with open(self.file_location) as csvfile:
            contents = csv.reader(csvfile, delimiter=',')
            for index, line in enumerate(contents):
                if index <= 4:
                    self.first_lines.append(line)
                else:
                    self.item_dicts[line[1]] = MovieObject(line[0], line[1], line[2], line[3], line[4])
                    self.movie_names.append(line[1])

    def _merge_sorter(self, movie_list: list):
        """
        Uses Merge Sort (based on user input) to sort list of movies. Sorts In-Place.
        Recommended to use self.movie_names

        :type movie_list: list
        """
        if len(movie_list) > 1:
            mid = len(movie_list) // 2
            left_side = movie_list[:mid]
            right_side = movie_list[mid:]
            self._merge_sorter(left_side)
            self._merge_sorter(right_side)

            left_half_index = right_half_index = keeper = 0

            while left_half_index < len(left_side) and right_half_index < len(right_side):
                print(f"\n\n")
                print(f"Left Side: {left_side}, Right Side: {right_side}")
                print(f"1.{left_side[left_half_index]}\n2.{right_side[right_half_index]}")
                answer = input("which one is greater 1 or 2?\n")
                if answer == "1":
                    movie_list[keeper] = left_side[left_half_index]
                    left_half_index += 1
                    keeper += 1
                elif answer == "2":
                    movie_list[keeper] = right_side[right_half_index]
                    right_half_index += 1
                    keeper += 1
                else:
                    print("Wrong Choice! Please input only '1' or '2'")

            while left_half_index < len(left_side):
                movie_list[keeper] = left_side[left_half_index]
                left_half_index += 1
                keeper += 1

            while right_half_index < len(right_side):
                movie_list[keeper] = right_side[right_half_index]
                right_half_index += 1
                keeper += 1

    def _movie_object_sorter(self):
        """
        Sorts items from self.item_dicts into self.sorted_dict (contains MovieObjects) based on order of
        self.movie_names.
        """
        for i, val in enumerate(self.movie_names):
            item = self.item_dicts.get(val)
            item.position = i+1
            self.sorted_dict[val] = item

    def _write_csv(self):
        """
        Generates a LetterBoxd compliant list csv based on order in self.sorted_dict
        """
        with open('../sorted_list.csv', mode='w', newline='') as sorted_list_csv:
            headers = ['Position', 'Name', 'Year', 'URL', 'Description']
            first_lines_writer = csv.writer(sorted_list_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for line in self.first_lines:
                first_lines_writer.writerow(line)
            writer = csv.DictWriter(sorted_list_csv, fieldnames=headers)
            writer.writeheader()
            for item in self.sorted_dict.values():
                writer.writerow({"Position": item.position, "Name": item.name, "Year": item.year, "URL": item.url,
                                 "Description": item.description})

    def _perform_merge_sort(self):

        self._read_csv()
        self._merge_sorter(self.movie_names)
        self._movie_object_sorter()
        self._write_csv()


if __name__ == '__main__':
    MovieListMergeSorter("E:\\Movie Data\\letterboxd-naveenpiedy-jun\\lists\\all-time-favorites.csv")
