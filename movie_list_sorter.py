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


class MovieListSorter:

    def __init__(self, file_location):
        self.file_location = file_location
        self.item_dicts = dict()
        self.sorted_dict = dict()
        self.movie_names = list()
        pass

    def read_csv(self):
        with open(self.file_location) as csvfile:
            contents = csv.reader(csvfile, delimiter=',')
            next(contents)
            next(contents)
            next(contents)
            next(contents)
            next(contents)
            for line in contents:
                self.item_dicts[line[1]] = MovieObject(line[0], line[1], line[2], line[3], line[4])
                self.movie_names.append(line[1])

    def movie_sorter(self, movie_list):
        if len(movie_list) > 1:
            mid = len(movie_list) // 2
            left_side = movie_list[:mid]
            right_side = movie_list[mid:]
            self.movie_sorter(left_side)
            self.movie_sorter(right_side)

            i = j = k = 0

            while i < len(left_side) and j < len(right_side):
                print(f"1.{left_side[i]}\n2.{right_side[j]}")
                answer = input("which one is greater 1 or 2?")
                if answer == "1":
                    movie_list[k] = left_side[i]
                    i += 1
                    k += 1
                elif answer == "2":
                    movie_list[k] = right_side[j]
                    j += 1
                    k += 1
                else:
                    print("Wrong Choice")

            while i < len(left_side):
                movie_list[k] = left_side[i]
                i += 1
                k += 1

            while j < len(right_side):
                movie_list[k] = right_side[j]
                j += 1
                k += 1

    def movie_object_sorter(self):
        for i, val in enumerate(self.movie_names):
            item = self.item_dicts.get(val)
            item.position = i+1
            self.sorted_dict[val] = item

    def write_csv(self):
        with open('sorted_list.csv', mode='w',  newline='') as sorted_list_csv:
            headers = ['Position', 'Name', 'Year', 'URL', 'Description']
            writer = csv.DictWriter(sorted_list_csv, fieldnames=headers)
            writer.writeheader()
            for i in self.sorted_dict.values():
                writer.writerow({"Position": i.position, "Name": i.name, "Year": i.year, "URL": i.url,
                                 "Description": i.description})


if __name__ == '__main__':
    mls = MovieListSorter("E:\\Movie Data\\letterboxd-naveenpiedy-jun\\lists\\all-time-favorites.csv")
    mls.read_csv()
    # mls.movie_sorter(mls.movie_names)
    # print(mls.movie_names)

    sorted_list = ['Moonrise Kingdom', 'The Grand Budapest Hotel', 'The Royal Tenenbaums', 'Parasite', 'Pulp Fiction',
                   'La La Land', 'Portrait of a Lady on Fire', 'Jojo Rabbit', 'Kill Bill: Vol. 1',
                   'Inglourious Basterds', 'Kill Bill: Vol. 2', 'Lady Bird', 'The Dark Knight', 'Little Women',
                   'Marriage Story', 'Avengers: Endgame', 'The Avengers', 'The Iron Giant',
                   'Scott Pilgrim vs. the World', 'Knives Out', 'Back to the Future', 'About Time',
                   'When Harry Met Sally...', "Ocean's Eleven", 'Alaipayuthey']
    mls.movie_names = sorted_list
    mls.movie_object_sorter()
    mls.write_csv()
