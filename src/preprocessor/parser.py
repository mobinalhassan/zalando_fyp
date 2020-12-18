import re
from src import lists


def make_string(list1, s_string):
    print(list1)
    return s_string.join(str(v) for v in list1)


def make_list(string_a, spliter):
    print(string_a)
    return list(str(string_a).split(spliter))


class Parser:
    def __init__(self):
        pass

    def parse_missing_value(self, cloth_single):

        if len(cloth_single['colors'].split('/')) > 1:
            for color in lists.color_List:
                check_fabric = cloth_single['colors'].find(color)
                if check_fabric != -1:
                    cloth_single['colors'] = color
                    print(f"Product color ==> {color}")
                    break
