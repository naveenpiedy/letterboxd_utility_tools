from src.movie_list_tools.movie_list_sorter import ListBaseClass


class MovieListMergeSorter(ListBaseClass):

    def __init__(self, file_location: str, list_name: str):
        """
        The __init__ function should perform end to end operation from reading the CSV to sorting to generating a csv.
        """
        super().__init__(file_location, list_name)
        self._perform_merge_sort()

    def _sorter(self, movie_list: list):
        """
        Uses Merge Sort (based on user input) to sort list of movies. Sorts In-Place.
        Recommended to use self.movie_names

        :type movie_list: list
        """
        if len(movie_list) > 1:
            mid = len(movie_list) // 2
            left_side = movie_list[:mid]
            right_side = movie_list[mid:]
            self._sorter(left_side)
            self._sorter(right_side)

            left_half_index = right_half_index = keeper = 0

            while left_half_index < len(left_side) and right_half_index < len(right_side):
                print("\n\n")
                print(f"Left Side: {left_side}Right Side: {right_side}")
                print("")
                print(f"{'1.'+ left_side[left_half_index]:^40}")
                print(f"{self.list_item_dicts.get(left_side[left_half_index])}")
                print("")
                print(f"{'2.'+right_side[right_half_index]:^40}")
                print(f"{self.list_item_dicts.get(right_side[right_half_index])}")
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
                    print("Invalid Choice! Please input only '1' or '2'")

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
            item = self.list_item_dicts.get(val)
            item.position = i+1
            self.sorted_dict[val] = item

    def _perform_merge_sort(self):

        self._read_list_csv()
        self._sorter(self.movie_names)
        self._movie_object_sorter()
        self._write_list_csv()


if __name__ == '__main__':
    MovieListMergeSorter("E:\\Movie Data\\letterboxd-naveenpiedy-jun", "all-time-favorites.csv")
