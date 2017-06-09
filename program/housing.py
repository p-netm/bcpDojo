import random

class Room(object):
    max_space = 0
    name = ""

    def __init__(self):
        pass

    def get_type(self):
        pass


class LivingSpace(Room):
    max_space = 4

    def __init__(self, name):
        self.name = name

    def get_type(self):
        return "LivingSpace"


class Office(Room):
    max_space = 6

    def __init__(self, name):
        self.name = name

    def get_type(self):
        return "Office"


class Person(object):
    person_id = ""
    # remove id_placeholder -> ADDING ID AS SECOND PARAMETER
    person_name = ""

    def __init__(self):
        pass

    def get_type(self):
        pass


class Staff(Person):
    def __init__(self, name, person_id):
        self.person_name = name
        self.person_id = person_id

    def __del__(self):
        pass

    def get_type(self):
        return "Staff"


class Fellow(Person):

    def __init__(self, name, person_id):
        self.person_name = name
        self.person_id = person_id

    def __del__(self):
        pass

    def get_type(self):
        return "Fellow"