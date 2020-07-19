from typing import List, Dict


class MovieListMergeSorter:
    __slots__ = "list_items"

    def __init__(self, list_items: Dict):
        if not list_items:
            raise Exception("Please provide a non empty dict. Use CSV Reader to read the csv")
        self.list_items = list_items

    def _merge_sort(self, movie_list: List):
        """
        Uses Merge Sort (based on user input) to sort list of movies. Sorts In-Place.
        Recommended to use self.movie_names

        :type movie_list: list
        """

        if len(movie_list) > 1:
            mid = len(movie_list) // 2
            left_side = movie_list[:mid]
            right_side = movie_list[mid:]
            self._merge_sort(left_side)
            self._merge_sort(right_side)

            left_half_index = right_half_index = keeper = 0

            while left_half_index < len(left_side) and right_half_index < len(right_side):
                print("\n\n")
                print(f"Left Side: {left_side}Right Side: {right_side}")
                print("")
                print(f"{'1.'+ left_side[left_half_index]:^40}")
                print(f"{self.list_items.get(left_side[left_half_index])}")
                print("")
                print(f"{'2.'+right_side[right_half_index]:^40}")
                print(f"{self.list_items.get(right_side[right_half_index])}")
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

    def merge_sort_items(self) -> Dict:
        movie_names = list(self.list_items.keys())
        self._merge_sort(movie_names)
        result_dict = dict()
        for i, val in enumerate(movie_names):
            item = self.list_items.get(val)
            item.position = i+1
            result_dict[val] = item

        return result_dict
