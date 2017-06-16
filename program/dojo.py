__author__ = 'Sudo Pnet'
from .housing import LivingSpace, Staff, Office, Fellow
import random, sys
import re
import os
from .print_ import p_info, p_danger, p_warning, p_success
from .migration import Person, Room , base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


class Dojo(object):

    def __init__(self):
        """ The Dojo class contains the required utilities that will automate the process of calling
        instances of the other classes think of it as the main logic area that links the class' models
        and the arguments parsed through the docopt in order to accomplish certain defined tasks.
        """
        self.person_list = list()
        self.room_list = list()
        self.room_name_set = set()
        #  optional, soon to become obsolete
        self.unallocated_list = []
        self.unallocated_living_list = []  # contains only fellow objects who requested accommodation but did not get
        self.staff_list = []
        self.fellow_list = []
        self.office_dict = {}
        self.living_space_dict = {}

    def instant_room(self, room_type, parsed_list):
        """check that a room is non_existent before is is added to list of current rooms:
           implementation is now one fold """
        if room_type == "office":
            housing_class = Office
        elif room_type == "living_space":
            housing_class = LivingSpace
        else:
            raise TypeError("room type was not found")
        for room_name in parsed_list:
            try:
                if room_name not in self.room_name_set:
                    self.room_list.append(housing_class(room_name))
                    p_success("An %s called %s has been successfully created!" %
                          (room_type, housing_class(str(room_name)).room_name.capitalize()))
                else:
                    raise ValueError("Room named: %s is already created" % room_name.capitalize())
            except ValueError as error:
                p_danger(error)
                # return "{} {} exists.".format(room_type.capitalize(), room_name.capitalize())
        return self.room_list

    def create_room(self, room_type, parsed_name_list):
        """ uses room_type to decide what type of rooms to create, then loops through
        parsed_name_list creating a room for each element in the list, no two rooms shall
        share the same name"""
        self.compute_variables()
        rooms_list = list()
        for i in parsed_name_list:
            if not str.isalnum(str(i)):
                return "Invalid room name"
        rooms_list += self.instant_room(room_type, parsed_name_list)
        return rooms_list

    def set_person_id(self, person_id):
        """ Task0: set a person's id ; if id is not given, ask for it
         else if id is not given and select flag is set then generate a random"""
        bool_counter = person_id
        input_id = person_id
        while bool_counter is None:
            p_info('Please type in your id(q to quit): ')
            input_id = str(input())
            if input_id .isdigit() and (7 == len(input_id) or len(input_id) == 8):
                bool_counter = False
                return input_id
            elif input_id == 'q':
                raise TypeError("\nid not assigned; person not created")
            else:
                p_warning("The id should be numeric with either 8 or 7 digits")
        if bool_counter == 'select':
            input_id = random.randrange(0000000, 99999999 + 1)
            return input_id
        return input_id

    def get_all_ids(self):
        """ retrieve the main list that store people with ids an returns a list containing the ids"""
        person_ids_list = []
        for person_obj in self.person_list:
            person_ids_list.append(person_obj.person_id)
        return person_ids_list

    def id_is_present(self, person_id):
        """Returns true if passed id is in the system"""
        all_ids = self.get_all_ids()
        if person_id in all_ids:
            return True
        else:
            return False

    def get_empty_rooms(self, room_type):
        """ return a list of room objects whose occupants are less than max_space"""
        non_full_list = list()
        for room in self.room_list:
            if room.get_type() == room_type and room.occupants < room.max_space:
                non_full_list.append(room)
        return non_full_list

    def view_person_id(self):
        """Seeing that ids are assigned by the system i thought it wise to include a function that lists
        a person and his/her id"""
        p_info("(Occupation)Person_name \t Person_id")
        for person in self.person_list:
            print("%s" % person.get_type(), person.person_name, ": \t", person.person_id)

    def compute_variables(self):
        self.room_name_set = set()
        self.unallocated_list = []
        self.unallocated_living_list = []  # contains only fellow objects who requested accommodation but did not get
        self.staff_list = []
        self.fellow_list = []
        self.office_dict = {}
        self.living_space_dict = {}

        for room_obj in self.room_list:
            self.room_name_set.add(room_obj.room_name)
            if room_obj.get_type() == 'office':
                self.office_dict[room_obj.room_name] = []
            elif room_obj.get_type() == 'living_space':
                self.living_space_dict[room_obj.room_name] = []

        for person in self.person_list:
            if person.office is None:
                self.unallocated_list.append(person)
            if person.get_type() == "fellow" and person.space is None:
                self.unallocated_living_list.append(person)
            if person.get_type() == "staff":
                self.staff_list.append(person)
            if person.get_type() == "fellow":
                self.fellow_list.append(person)
            if person.office is not None:
                self.office_dict[person.office].append(person.person_name)
            if person.get_type() == "fellow" and person.space is not None:
                self.living_space_dict[person.space].append(person.person_name)

    def assign_office(self, person_object, office_name=""):
        """ takes a person_object and fills up the person.office property randomly with an office object,
            however if the office_name argument is given the system retrieves the office object by that name
            and specifically assigns that"""
        empty_office_list = self.get_empty_rooms('office')
        if not office_name:
            try:
                office_obj = random.choice(empty_office_list)
            except IndexError:
                return False
        else:
            office_obj = self.get_room_by_room_name(office_name, 'office')
        if office_obj not in empty_office_list:
            return "Room is full"
        person_object.office = office_obj

        p_success(person_object.person_name + " has been allocated the office " +
              office_obj.room_name)
        office_obj.occupants += 1
        return True

    def get_room_by_room_name(self, room_name, room_type=None):
        if room_type is not None:
            for room_obj in self.room_list:
                if room_obj.get_type() == room_type and room_obj.room_name == room_name:
                    return room_obj
        elif room_type is None:
            for room_obj in self.room_list:
                if room_obj.room_name == room_name:
                    return room_obj
        return False

    def assign_living_space(self, person_object, space_name=""):
        if person_object.get_type() != 'Fellow':
            raise ValueError("Only Fellows can be assigned to living spaces")
        empty_space_list = self.get_empty_rooms('living_space')
        if not space_name:
            try:
                space_obj = random.choice(empty_space_list)
            except IndexError:
                return False
        else:
            space_obj = self.get_room_by_room_name(space_name, 'living_space')
        if space_obj not in empty_space_list:
            return "Room is full"
        person_object.space = space_obj
        p_success(person_object.person_name + " has been allocated to the living space: " +
              space_obj.room_name)
        space_obj.occupants += 1
        return True

    def retrieve_person_by_id(self, person_id):
        """ Task2: Thought: have a function that can retrieve a person object when only given either the person's id"""
        for person in self.person_list:
            if person.person_id == person_id:
                return person
        p_danger("No one was found with the id: " + person_id)
        return False

    def retrieve_person_by_name(self, person_name):
        for person in self.person_list:
            if person.person_name == person_name:
                return person
        p_danger("No one was found with the name: " + person_name)
        return False











###############################################test####################################################################

    def add_person(self, first_name, second_name, occupation, accommodate="n", id=None):
        """ uses occupation and decides what constructor of either the subclasses
        fellow or staff that it should call. depending on the accommodate parameter
         a fellow occupant can be assigned an office and a living_space"""
        self.compute_variables()
        person_name = first_name.capitalize() + " " + second_name.capitalize()
        occupation = occupation.lower()
        accommodate = accommodate.lower()
        try:
            person_id = self.set_person_id(id)
        except:
            p_danger("Person not created.")
            return

        if occupation == "fellow":
            if accommodate == "yes" or accommodate == "y":
                if not self.id_is_present(person_id):
                    fellow_obj = Fellow(str(person_name), person_id)
                    self.person_list.append(fellow_obj)
                    # randomise adding this fellow to the living_space_list
                    office_assign_check = self.assign_office(fellow_obj)
                    print(fellow_obj.person_name, "has been successfully added")
                    living_assign_check = self.assign_living_space(fellow_obj)
                    if not office_assign_check:
                        # the fellow was not assigned to an office
                        p_warning(person_name, "has been added but not assigned to any office")
                    if not living_assign_check:
                        p_warning(person_name, "has been added but not assigned to any living_space")
                else:
                    print(person_name, "has not been added; the id is already in the system")

            elif accommodate == "no" or accommodate == "n":
                if not self.id_is_present(person_id):
                    fellow_obj = Fellow(str(person_name), person_id)
                    self.person_list.append(fellow_obj)
                    office_assign_check = self.assign_office(fellow_obj)
                    p_success(person_name + " has been successfully added")
                    if not office_assign_check:
                        p_warning(person_name + " has been added but not assigned to any office")
                else:
                    p_danger(person_name + " has not been added; the id is already in the system")

        elif occupation == "staff":
            if not self.id_is_present(person_id):
                staff_obj = Staff(str(person_name), person_id)
                self.person_list.append(staff_obj)
                # add the staff to the office dict ?
                office_assign_check = self.assign_office(staff_obj)
                if not office_assign_check:
                    p_warning(person_name + " has been added but not allocated to any office")
            else:
                p_danger("detected an id collision for " + person_name)

    def retrieve_room_by_room_name(self, room_name):
        for room_obj in self.room_list:
            if room_obj.room_name == room_name:
                return room_obj
        return False

    def modify_room(self, room_name, room_type=False, new_name=False, d=False, D=False, c=False, C=False):
        self.compute_variables()
        if new_name:
            self.modify_room_name(room_name, new_name, room_type)
        if d:
            """ We are gona delete a room"""
            self.delete_room(room_name)
        if c:
            """ We are just to clear a room """
            self.clear_room(room_name)

    def modify_room_name(self, room_name, new_room_name, room_type=False):
        # first check the room is existent and then retrieve the room name
        if room_name not in self.room_name_set:
            p_warning("%s room was not found" % room_name)
            return False
        # if room_name was found
        room_obj = self.get_room_by_room_name(room_name=room_name)
        if room_type and room_obj.get_type() != room_type:
            p_warning("No {} was found with the name {}".format(room_type, room_name))
        else:
            room_obj.room_name = new_room_name
        return room_obj

    def clear_room(self, room_name, room_type):
        if room_name not in self.room_name_set:
            p_warning("%s room was not found" % room_name)
            return False
        room_obj = self.get_room_by_room_name(room_name=room_name)
        if room_type and room_type != room_obj.get_type():
            p_warning("No {} was found with the name {}". format(room_type, room_name))
            return False
        deallocate_names = list()
        for person_obj in self.person_list:
            if person_obj.office is room_obj:
                person_obj.office = None
                deallocate_names.append(person_obj.fullname)
            elif person_obj.get_type() == 'fellow' and person_obj.space is room_obj:
                person_obj.space = None
                deallocate_names.append(person_obj.fullname)
            # maybe we can append the deallocated person_objects to a list and then print that they were deallocated
        p_success(", ".join(deallocate_names) + " were successfully cleared from %s" % room_name.capitalize())
        return room_obj

    def delete_room(self, room_name, room_type=False):
        # first get the cleared room object, pop it from the room_list and then delete it
        cleared_room_obj = self.clear_room(room_name, room_type)
        self.room_list.pop(self.room_list.index(cleared_room_obj))
        del cleared_room_obj

    def clear_reassign(self, room_name, room_type=False):
        if room_name not in self.room_name_set:
            p_warning("%s room was not found" % room_name)
            return False
        room_obj = self.get_room_by_room_name(room_name=room_name)
        if room_type and room_type != room_obj.get_type():
            p_warning("No {} was found with the name {}". format(room_type, room_name))
            return False
        deallocate_names = list()
        deallocate_obj = list()
        for person_obj in self.person_list:
            if person_obj.office is room_obj:
                person_obj.office = None
                deallocate_names.append(person_obj.fullname)
                deallocate_obj.append(person_obj)
            elif person_obj.get_type() == 'fellow' and person_obj.space is room_obj:
                person_obj.space = None
                deallocate_names.append(person_obj.fullname)
                deallocate_obj.append(person_obj)
            # maybe we can append the deallocated person_objects to a list and then print that they were deallocated
        p_success(", ".join(deallocate_names) + " were successfully cleared from %s" % room_name.capitalize())
        room_obj.occupants = room_obj.max_space
        if room_obj.get_type == 'office':
            for person_obj in deallocate_obj:
                self.assign_office(person_obj)
        elif room_obj.get_type() == 'living_space':
            for person_obj in deallocate_obj:
                self.assign_living_space(person_obj)
        room_obj.occupants = 0
        return room_obj

    def delete_reassign(self, room_name, room_type=False):
        # first empty room and while at it reassign members to a different room, then pop room if len of value is 0
        cleared_room = self.clear_reassign(room_name, room_type)
        if cleared_room.occupants > 0:
            p_info("%s is occupied" % room_name.capitalize())
        else:
            self.room_list.pop(self.room_list.index(cleared_room))
            del cleared_room

    def modify_person(self, old_id, new_id=None, f_name=None, s_name=None, delete=None):
        # for starters modify person can modify several aspects of a person synchronously
        # get person by the said id and replace the id
        person_obj = self.retrieve_person_by_id(old_id)
        if person_obj:
            if new_id is not None:
                person_obj.person_id = new_id
            if f_name is not None:
                full_name = person_obj.person_name.split(" ")
                full_name[0] = f_name
                person_obj.person_name = " ".join(full_name)
            if s_name is not None:
                full_name = person_obj.person_name.split(" ")
                full_name[1] = s_name
                person_obj.person_name = " ".join(full_name)
            if delete is not None:
                # the person_obj fails to exist, pop the object from the person_list
                self.person_list.pop(self.person_list.index(person_obj))
                del person_obj
        else:
            p_danger("No person found with the Id: %s" % old_id)
            p_info("Consider the view_ids or the search_id_for functions, to verify if an id is in the system")

    def reallocate_person(self, person_id, new_room):
        """ takes in two inputs the personal id and new room name.
        assign the person identified by the id to a new room name"""
        self.compute_variables()
        if self.id_is_present(person_id):
            movable_person = self.retrieve_person_by_id(person_id)
            # check if the room given by new_room exists
            destin_room = self.retrieve_room_by_room_name(new_room)
            if destin_room:
                # destination room was succesfully returned
                if destin_room.get_type() == 'office':
                    movable_person.office = None
                    assign_check = self.assign_office(movable_person, office_name=new_room)
                    if assign_check :
                        p_success("%s of %s was succesfully moved to %s " % (movable_person.person_name, movable_person.person_id, new_room))
                    else:
                        p_danger(assign_check)
                elif destin_room.get_type() == 'living_space' and movable_person.get_type() == 'Fellow':
                    movable_person.space = None
                    assign_check = self.assign_living_space(movable_person, space_name=new_room)
                    if assign_check:
                        p_success("%s of %s was succesfully moved to %s " % (movable_person.person_name, movable_person.person_id, new_room))
                    else:
                        p_danger(assign_check)
                else:
                    p_danger("Person not reallocated")
            else:
                p_danger("Room with the name %s was not found" % new_room.capitalize())
        else:
            p_danger("Id not found within the system")
        return True

    def print_room(self, room_name):
        """ Task1: input: room_name
        takes that room_name and prints all the people allocated to that room """
        self.compute_variables()
        serial = 0
        if self.search_name(room_name):
            print('x'*12, '==> ', room_name.upper(), ' <==', 'x'*12, '\n')
            if room_name in self.living_space_dict.keys():
                if len(self.living_space_dict[room_name]) > 0:
                    for list_index in self.living_space_dict[room_name]:
                        serial += 1
                        print("\t" + str(serial) + ").", list_index)
                else:
                    print("No one has yet been allocated to this Living space")
                    return False
            elif room_name in self.office_dict.keys():
                if len(self.office_dict[room_name]) > 0:
                    for list_index in self.office_dict[room_name]:
                        serial += 1
                        print("\t" + str(serial) + ").", list_index)
                else:
                    print("No one has yet been allocated to this office")
                    return False
            print("\nEnd of file reached")
        else:
            print("Room_", room_name, "was not found")
            return False

    def print_allocations(self, file_name=''):
        """Task1: Input: nothing; output:  print allocations to the screen.
         if -o argument is given => dump the allocations in a text file """
        """ Retrieve the office_dict and living_space_dict;Loops through them and prints the room name and
            comma separated names of the occupants"""
        self.compute_variables()
        print_string = ""
        for space_obj in self.living_space_dict.keys():
            if len(self.living_space_dict[space_obj]) == 0:
                pass  # i do not know yet what to do for the rooms that do not have occupants
            elif len(self.living_space_dict[space_obj]) == 1:
                print_string += "\n" + '(living_space)' + space_obj.upper() + "\n" + "-" * 37 + "\n"
                print_string += self.living_space_dict[space_obj][len(self.living_space_dict[space_obj]) - 1] + "\n"
            elif len(self.living_space_dict[space_obj]) > 1:
                print_string += "\n" + '(living_space)' + space_obj.upper() + "\n" + "-" * 37 + "\n"
                for person_index in range(0, len(self.living_space_dict[space_obj]) - 1):
                    print_string += self.living_space_dict[space_obj][person_index] + ", "
                print_string += self.living_space_dict[space_obj][len(self.living_space_dict[space_obj]) - 1] + "\n"
        for office_object in self.office_dict.keys():
            if len(self.office_dict[office_object]) == 0:
                pass
            if len(self.office_dict[office_object]) == 1:
                print_string += "\n" + '(office)' + office_object.upper() + "\n" + "-" * 37 + "\n"
                print_string += self.office_dict[office_object][len(self.office_dict[office_object]) - 1] + "\n"
            if len(self.office_dict[office_object]) > 1:
                print_string += "\n" + '(office)' + office_object.upper() + "\n" + "-" * 37 + "\n"
                for person_index in range(0, len(self.office_dict[office_object]) - 1):
                    print_string += self.office_dict[office_object][person_index] + ", "
                print_string += self.office_dict[office_object][len(self.office_dict[office_object]) - 1] + "\n"
        print(print_string)
        # Now for the file handling
        self.file_handler_func(print_string, file_name)
        return print_string

    def file_handler_func(self, print_string, file_name):
        """ Writes content to files """
        if file_name:  # checks if file_name arguments was given
            """ Check if file's content is more than 0, if true; query on an append or overwrite"""
            file_path = self.return_file_dir(file_name, 'output')
            if not os.path.exists(file_path):
                print("\nTrying to create a file called: ", file_name, "\n")
                file_handler = open(file_path, 'w+')
                file_handler.close()

            file_handler = open(file_path, 'r')
            if len(file_handler.read()) > 0:
                print("**file is not Empty,key in y to append, n to overwrite: ")
                choice = input()
                file_handler.close()
                if choice == 'Y' or choice == 'y':
                    file_handler = open(file_path, 'a')
                    file_handler.write(print_string)
                    print("Allocations succesfully appended to: ", file_name)
                    file_handler.close()
                elif choice == 'N' or choice == 'n':
                    file_handler = open(file_path, 'w')
                    file_handler.write(print_string)
                    print("succesfully overwrote: ", file_name)
                    file_handler.close()
            elif len(file_handler.read()) == 0:
                file_handler = open(file_path, 'w')
                file_handler.write(print_string)
                print("succesfully wrote to: ", file_name)
                file_handler.close()

    def print_unallocated(self, file_name=""):
        """Task1: Input: nothing; output:  print names of unallocated people on the screen.
         if -o argument is given => dump the names to a text file """
        # first write the print strings then call the file handler function
        self.compute_variables()
        print_string = " \n Names of both staff and fellows who are not allocated to Offices"
        second_print_string = " \n Names of only Fellows who are not yet allocated to Living Spaces"
        for person in self.unallocated_list:
            print_string += "\n" + person.person_name + "\n"
        for person in self.unallocated_living_list:
            second_print_string += "\n" + person.person_name + "\n"
        total_string = print_string + second_print_string
        if not file_name:
            print(print_string)
            print(second_print_string)
        else:
            self.file_handler_func(total_string, file_name)
            p_success("File succesfully updated")

    def load_people(self, file_name):
        """ will take in one compulsory argument, which is the name of the file from which to read data
        from. for each record in this file we can then add_people """
        # retrieve file_path and check if file exists
        file_path = self.return_file_dir(file_name, 'input')
        if os.path.isfile(file_path):
            multi_list = self.read_file_names(file_path)
            for person in multi_list:
                self.add_person(person[0], person[1], person[2], person[3], id="select")
            return True
        else:
            p_danger("Dojo could not find any file by the name: " + file_name)
            return False

    def return_file_dir(self, file_name, action):
        """ Task2: identify where a file is supposed to be and return the path, the working directory
         is bcpDojo/ home directory for the project"""
        parent_dir = os.getcwd()
        proper_dir = os.path.join(parent_dir, 'files', action, file_name)
        return proper_dir

    def read_file_names(self, file_name):
        file_handler = open(file_name, 'r')
        return_list = []
        for line in file_handler:
            # maybe like create like a multi dimensional list; the main index will contain the line number
            # while the secondary index will like contain the list contents for each line.
            temp = line.strip("\n").split(" ")
            return_list.append(self.refractor_line_feed(temp))
        file_handler.close()
        return return_list

    def refractor_line_feed(self, temp_list):
        """ Task2 : takes in a list and refactor the contents accordingly so that they can be properly
             parsed into the add_person function"""
        temp = []
        temp.extend([temp_list[0], temp_list[1], temp_list[2]])
        if len(temp_list) == 3:
            temp.append("n")
            return temp
        elif len(temp_list) == 4:
            temp.append(temp_list[3])
            return temp

    def save_state(self, db_name="state.sqlite"):
        """ Task3: consume the dojo instance, parse data to save function from migration"""
        dir = self.return_file_dir(db_name, "database")
        if os.path.exists(dir):
            pass
        else:
            open(dir, 'w+')
            p_info(db_name, "database created")

        engine = create_engine('sqlite:///' + dir)
        base.metadata.create_all(engine)
        session = Session(bind=engine)

        for room_obj in self.room_list:
            room_entry = Room(room_obj.room_name, room_obj.get_type(), room_obj.occupants)
            session.add(room_entry)

        for person in self.person_list:
            try:
                person_entry = Person(person.person_id, person.full_name, person.get_type(), person.office.room_name,
                                      person.space.room_name)
            except AttributeError:
                person_entry = Person(person.person_id, person.full_name, person.get_type(), person.office.room_name)
            session.add(person_entry)

        session.commit()

    def load_state(self, db_file):
        """ more like reverse engineering the above method"""
        # retrieve all rooms,
        self.compute_variables()
        dir = self.return_file_dir(db_file, "database")
        if os.path.exists(dir):
            # our loading database logic
            engine = create_engine('sqlite:///' + dir)
            base.metadata.create_all(engine)
            session = Session(bind=engine)

            # we load offices and spaces first
            rooms_ = session.query(Room).all()
            office_list = list()
            space_list = list()
            for room in rooms_:
                if room.room_type == 'office':
                    office_list.append(room.room_name)
                elif room.room_type == 'living-space':
                    space_list.append(room.room_name)
            self.instant_room('office', office_list)
            self.instant_room('living_space', space_list)

            persons_ = session.query(Person).all()
            for person in persons_:
                if person.occupation == 'Staff':
                    person_obj = Staff(person.full_name, person.person_id)
                    if person.space_name != 'None':
                        raise Exception("A staff should not have a living_space")
                    elif person.office_name != 'None':
                        self.assign_office(person_obj, office_name=person.office_name)
                if person.occupation == 'Fellow':
                    person_obj = Fellow(person.full_name, person.person_id)
                    if person.space_name != 'None':
                        self.assign_living_space(person_obj, person.space_name)
                    elif person.office_name != 'None':
                        self.office_name(person_obj, person.office_name)
        else:
            p_danger("Database was not found")
            return False
        return

    def search_id_for(self, name, other_name=None):
        """return a list of people who have the said name """
        # retrieving a person by a single name regardless of whether its their fast or second
        # we need a list to append this
        identity_list = list()
        if other_name:
            for person in self.person_list:
                if name in person.person_name:
                    identity_list.append("{}    {}".format(person.person_id, person.person_name))
        else:
            for person in self.person_list:
                if name in person.person_name:
                    identity_list.append("{}    {}".format(person.person_id, person.person_name))
        print(identity_list) # maybe you could consider pretty printing this
        return identity_list







#  #####################################################################################################################


    def display(self):
        """ using this only for debugging purposes"""
        # change the presentation view  #########################
        self.compute_variables()
        print("\nliving_space ", self.living_space_dict)
        print("office_dict", self.office_dict)
        print("staff_list", self.staff_list)
        print("fellow_list", self.fellow_list)
        print("unallocate_list", self.unallocated_list)
        print("unallocated_living_list", self.unallocated_living_list, "\n")

    def search_name(self, search_parameter, category=None):
        """" Task1: Takes in a str name of any object and finds the object associated with that string"""
        # i need an alternative implementation where you can use one word to search for a person -> maybe use
        # additional optional arguments to check through; category can take "person" or "room"
        self.compute_variables()
        def selective_search_name(search_parameter):
            for person in self.fellow_list:
                if search_parameter in person.person_name:
                    return "Fellow"
            for person in self.staff_list:
                if search_parameter in person.person_name:
                    return "Staff"
        if category == "person":
            return selective_search_name(search_parameter)
        if len(re.findall('\S+', search_parameter)) < 2:
            if search_parameter in self.living_space_dict:
                return "LivingSpace"
            elif search_parameter in self.office_dict:
                return "Office"
        elif len(re.findall('\S+', search_parameter)) >= 2:
            return selective_search_name(search_parameter)

        return False


