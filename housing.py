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

    def set_person_id(self):
        """ i need a unique id every time; so i thought of using the date and
         time as string alphanum that make a unique id every instance"""
        bool_counter = True
        while bool_counter:
            print('Please type in your id(q to quit): ')
            input_id = str(input())
            if input_id .isdigit() and (7 == len(input_id) or len(input_id) == 8):
                bool_counter = False
                return input_id
            elif input_id == 'q':
                raise TypeError("\nid not assigned; person not created")
            else:
                print("The id should be numeric with either 8 or 7 digits")

    def get_type(self):
        pass


class Staff(Person):
    def __init__(self, name):
        try:
            self.person_name = name
            self.person_id = super().set_person_id()
        except TypeError as error:
            self.__del__

    def __del__(self):
        pass

    def get_type(self):
        return "Staff"


class Fellow(Person):

    def __init__(self, name):
        try:
            self.person_name = name
            self.person_id = super().set_person_id()
        except TypeError:
            self.__del__

    def __del__(self):
        pass

    def get_type(self):
        return "Fellow"