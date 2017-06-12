class Room(object):
    def __init__(self, name, max_space):
        self.max_space = max_space
        self.room_name = name
        self.occupants = 0

    def get_type(self):
        pass


class Person(object):
    def __init__(self, name, p_id):
        self.person_id = p_id
        self.person_name = name
        # track allocations as objects
        self.office = None


    def get_type(self):
        pass


class Staff(Person):
    def __init__(self, name, p_id):
        super().__init__(name=name, p_id=p_id)

    def get_type(self):
        return "Staff"


class Fellow(Person):

    def __init__(self, name, p_id):
        super().__init__(name=name, p_id=p_id)
        self.space = None

    def get_type(self):
        return "Fellow"

class LivingSpace(Room):
    def __init__(self, name):
        super().__init__(name=name, max_space=6)


    def get_type(self):
        return "living_space"


class Office(Room):
    def __init__(self, name):
        super().__init__(name=name, max_space=4)

    def get_type(self):
        return "office"

