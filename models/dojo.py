__author__ = 'Sudo Pnet'
from .housing import LivingSpace, Staff, Office, Fellow
import random
import re
import os
from .migration import Person, Office as db_office, Living_space as db_space, base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Dojo(object):

    def __init__(self):
        """ The Dojo class contains the required utilities that will
        automate the process of calling instances of the other classes
        think of it as the main logic area that links the class' models and
        the arguments parsed through the docopt in order to accomplish certain
        defined tasks.
        """
        self.unallocated_list = []
        self.unallocated_living_list = []
        self.staff_list = []
        self.fellow_list = []
        self.office_dict = {}
        self.living_space_dict = {}

    @staticmethod
    def get_number(list_arg):
        # will return the length of any list or dictionary passed to it.
        return len(list_arg)

    def instant_room(self, room_type, room_listing, diction, housing_class):
        """check that a room is non_existent before is is added to list of current rooms:
           implementation is now one fold """
        for i in room_listing:
            try:
                if i not in diction.keys():
                    diction[housing_class(str(i)).name] = []
                    print("An %s called %s has been successfully created!" %
                          (room_type, housing_class(str(i)).name))
                else:
                    raise ValueError("Room named: %s is already created" % housing_class(str(i)).name)
            except ValueError as error:
                print(error)
        return diction

    def create_room(self, room_type, parsed_name_list):
        """ uses room_type to decide what type of rooms to create, then loops through
        room_name_list creating a room for each element in the list"""
        for i in parsed_name_list:
            if not str.isalnum(str(i)):
                return "Invalid room name"
        if room_type == "living_space":
            self.instant_room(room_type, parsed_name_list, self.living_space_dict, LivingSpace)
        if room_type == "office":
            self.instant_room(room_type, parsed_name_list, self.office_dict, Office)

    def set_person_id(self, person_id):
        """ Task0: set a person's id """
        bool_counter = person_id
        while bool_counter == None:
            print('Please type in your id(q to quit): ')
            input_id = str(input())
            if input_id .isdigit() and (7 == len(input_id) or len(input_id) == 8):
                bool_counter = False
                return input_id
            elif input_id == 'q':
                raise TypeError("\nid not assigned; person not created")
            else:
                print("The id should be numeric with either 8 or 7 digits")

    def add_person(self, first_name, second_name, occupation, accommodate="n", id=None):
        """ uses occupation and decides what constructor of either the subclasses
        fellow or staff that it should call. depending on the accommodate parameter
         a fellow occupant can be assigned an office and a living_space"""
        person_name = first_name.lower() + " " + second_name.lower()
        occupation = occupation.lower()
        accommodate = accommodate.lower()
        person_id = self.set_person_id(id)
        if occupation == "fellow":
            if accommodate == "yes" or accommodate == "y":
                fellow_obj = Fellow(str(person_name), person_id)
                if not self.id_is_present(fellow_obj.person_id):
                    self.fellow_list.append(fellow_obj)
                    # randomise adding this fellow to the living_space_list
                    office_assign_check = self.assign_office(fellow_obj)
                    print(fellow_obj.person_name, "has been successfully added")
                    living_assign_check = self.assign_living_space(fellow_obj)
                    if not office_assign_check:
                        # the fellow was not assigned to an office
                        print(fellow_obj.person_name, "has been added but not assigned to any office")
                        self.unallocated_list.append(fellow_obj)
                    if not living_assign_check:
                        self.unallocated_living_list.append(fellow_obj)
                        print(fellow_obj.person_name, "has been added but not assigned to any living_space")
                else:
                    print(fellow_obj.person_name, "has not been added; the id is already in the system")

            elif accommodate == "no" or accommodate == "n":
                fellow_obj = Fellow(str(person_name), person_id)
                if not self.id_is_present(fellow_obj.person_id):
                    self.fellow_list.append(fellow_obj)
                    office_assign_check = self.assign_office(fellow_obj)
                    print(fellow_obj.person_name, "has been successfully added")
                    if not office_assign_check:
                        print(fellow_obj.person_name, "has been added but not assigned to any office")
                        self.unallocated_list.append(fellow_obj)
                else:
                    print(fellow_obj.person_name, "has not been added; the id is already in the system")

        elif occupation == "staff":
            staff_obj = Staff(str(person_name), person_id)
            if not self.id_is_present(staff_obj.person_id):
                self.staff_list.append(staff_obj)
                # add the staff to the office dict ?
                office_assign_check = self.assign_office(staff_obj)
                if not office_assign_check:
                    print(staff_obj.person_name, "has been added but not allocated to any office")
                    self.unallocated_list.append(staff_obj)
            else:
                print("detected an id collision for", staff_obj.person_name)

    def assign_office(self, person_object, office_name=""):
        empty_office_dict = self.get_empty_rooms(self.office_dict, 6)
        if not office_name:
            try:
                random_office_key = random.choice(list(empty_office_dict.keys()))
            except IndexError:
                return False
        else:
            random_office_key = office_name
        self.office_dict[random_office_key].append(person_object.person_name)
        print(person_object.person_name, "has been allocated the office",
              random_office_key)
        return True

    def assign_living_space(self, person_object, space_name=""):
        empty_living_space_dict = self.get_empty_rooms(self.living_space_dict, 4)
        if not space_name:
            try:
                random_living_key = random.choice(list(empty_living_space_dict.keys()))
            except IndexError:
                return False
        else:
            random_living_key = space_name
        self.living_space_dict[random_living_key].append(person_object.person_name)
        print(person_object.person_name, "has been allocated to the living space: ",
              random_living_key)
        return True

    def reallocate_unallocated(self, unallocate_list, person_id):
        for person in unallocate_list:
            if person.person_id == person_id:
                person_of_interest = person
                # pop from sequence
                unallocate_list.pop(person_of_interest)

    def reallocate_person(self, person_id, new_room):
        """ takes in two inputs the personal id and new room name.
        assign the person identified by the id to a new room name"""
        # logic: check if id exists; if it does check that room exists and is not full;
        # if it to exists remove the person with the specified id from all unallocated_lists, and listings
        # can also be used to assign an unallocated person to a room -> so far not

        if self.id_is_present(person_id):
            #  first retrieve the room that the person_id is in and then restrict movement
            #  within that line(living_space or office)

            if new_room in self.office_dict.keys():
                double_list = self.retrieve_office_room(person_id)
                # the whole logic : remember to consider that staff should not rellocate to living space
                # unimplemented consideration : reallocating a fellow who does not want accommodation to
                # a living_space
                if len(self.office_dict[new_room]) < 6:
                    # use this section to pop a person from unallocated to office incorporate with double list
                    if double_list:
                        if new_room != double_list[0]:
                            if double_list[1] == "office":
                                # pop the person name from its current office and append it to the new office
                                self.office_dict[double_list[0]].pop(self.office_dict[double_list[0]].index(double_list[2]))
                                self.office_dict[new_room].append(double_list[2])
                            else:
                                print("cannot rellocate from office to living_space")
                        else:
                            print("Person already in", new_room)
                    else:
                        # implies person is unallcated
                        self.reallocate_unallocated(self.unallocated_list, person_id)
                        self.assign_office(self.retrieve_person_by_id(person_id), new_room)
                else:
                    print(new_room, "seems to be full.")

            elif new_room in self.living_space_dict.keys():
                double_list = self.retrieve_space_room(person_id)
                if len(self.living_space_dict[new_room]) < 4:
                    # use this section to pop a person from unallocated_space to living_space
                    if double_list:
                        if new_room != double_list[0]:
                            if double_list[1] == "living_space":
                                # pop the name from current living_space and append it to the new living space
                                self.living_space_dict[double_list[0]].pop(self.living_space_dict[double_list[0]].index(double_list[2]))
                                self.living_space_dict[new_room].append(double_list[2])
                            else:
                                print("cannot rellocate from living_space to office")
                        else:
                            print("Person already in", new_room)
                    else:
                        # unpop from unallocated living space and give a room
                        if self.retrieve_person_by_id(person_id).get_type == "fellow":
                            self.reallocate_unallocated(self.unallocated_living_list, person_id)
                            self.assign_living_space(self.retrieve_person_by_id(person_id), new_room)
                        else:
                            print(" person with id %s is not a fellow and thus cannot be given a living space!.." %
                                  person_id)
                else:
                    print(new_room, "seems to be full")
            else:
                print("The room " + new_room + " has not yet been created")
        else:
            print("no one by the id " + person_id + " was found\n")

    def retrieve_office_room(self, person_id):
        """Thought: to return a rooms information from a person_id """
        # so first retrieve the person name through its person object
        # then use the person name to identify the name of the office in which the name is listed in the occupants
        person_obj = self.retrieve_person_by_id(person_id)
        person_name = person_obj.person_name
        # now we use the name to get the room
        for office in self.office_dict.keys():
            if person_name in self.office_dict[office]:
                return [office, "office", person_name]
        return False

    def retrieve_space_room(self, person_id):
        person_obj = self.retrieve_person_by_id(person_id)
        person_name = person_obj.person_name
        for space in self.living_space_dict.keys():
            if person_name in self.living_space_dict[space]:
                return [space, "living_space", person_name]
        # returns a list of the room name and its type; its an index in the respective dictionary
        return False  # returns false if person is unallocated

    def print_room(self, room_name):
        """ Task1: input: room_name
        takes that room_name and prints all the people allocated to that room """
        if self.search_name(room_name):
            print('x'*12, '==> ', room_name.upper(), ' <==', 'x'*12, '\n')
            if room_name in self.living_space_dict.keys():
                if len(self.living_space_dict[room_name]) > 0:
                    for list_index in self.living_space_dict[room_name]:
                        print(list_index)
                else:
                    print("Not a single soul is in this room")
                    return False
            elif room_name in self.office_dict.keys():
                if len(self.office_dict[room_name]) > 0:
                    for list_index in self.office_dict[room_name]:
                        print(list_index)
                else:
                    print("Not a single soul is in this room")
                    return False
            print("End of file reached")
        else:
            print("Room_", room_name, "was not found")
            return False

    def print_allocations(self, file_name=''):
        """Task1: Input: nothing; output:  print allocations to the screen.
         if -o argument is given => dump the allocations in a text file """
        """ Retrieve the office_dict and living_space_dict;Loops through them and prints the room name and
            comma separated names of the occupants"""
        print_string = ""
        for space_obj in self.living_space_dict.keys():
            if len(self.living_space_dict[space_obj]) == 0:
                pass  # i do not know yet what to do for the rooms that do not have occupants
            elif len(self.living_space_dict[space_obj]) == 1:
                print_string += "\n" + '(living_space)' + space_obj.upper() + "\n"
                print_string += self.living_space_dict[space_obj][len(self.living_space_dict[space_obj]) - 1] + "\n"
            elif len(self.living_space_dict[space_obj]) > 1:
                print_string += "\n" + '(living_space)' + space_obj + "\n"
                print_string += "\n" + space_obj.upper() + "\n"
                for person_index in range(0, len(self.living_space_dict[space_obj]) - 1):
                    print_string += self.living_space_dict[space_obj][person_index] + ", "
                print_string += self.living_space_dict[space_obj][len(self.living_space_dict[space_obj]) - 1] + "\n"
        for office_object in self.office_dict.keys():
            if len(self.office_dict[office_object]) == 0:
                pass
            if len(self.office_dict[office_object]) == 1:
                print_string += "\n" + '(office)' + office_object.upper() + "\n"
                print_string += self.office_dict[office_object][len(self.office_dict[office_object]) - 1] + "\n"
            if len(self.office_dict[office_object]) > 1:
                print_string += "\n" + '(office)' + office_object.upper() + "\n"
                for person_index in range(0, len(self.office_dict[office_object]) - 1):
                    print_string += self.office_dict[office_object][person_index] + ", "
                print_string += self.office_dict[office_object][len(self.office_dict[office_object]) - 1] + "\n"
        print(print_string)
        # Now for the file handling
        self.file_handler_func(print_string, file_name)

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
        self.file_handler_func(total_string, file_name)

    def load_people(self, file_name):
        """ will take in one compulsory argument, which is the name of the file from which to read data
        from. for each record in this file we can then add_people """
        # retrieve file_path and check if file exists
        file_path = self.return_file_dir(file_name, 'input')
        if os.path.isfile(file_path):
            multi_list = self.read_file_names(file_path)
            for person in multi_list:
                self.add_person(person[0], person[1], person[2], person[3])
            return True
        else:
            print("Dojo could not find any file by the name: " + file_name)
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
        # decided to start with room_names
        dir = self.return_file_dir(db_name, "database")
        if os.path.exists(dir):
            pass
        else:
            open(dir, 'w+')
            print(db_name, "database created")

        engine = create_engine('sqlite:///' + dir)
        base.metadata.bind = engine
        base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()

        for room_instance in self.office_dict.keys():
            session.add(db_office(room_instance))
        for room_name in self.living_space_dict.keys():
            session.add(db_space(room_name))

        def add_people(person, office_name, space_name):
            if office_name and space_name:
                # def __init__(self, id, f_name, occupation, office="None", space="None")
                session.add(Person(id=person.person_id, f_name=person.person_name, occupation=person.get_type,
                                   office=office_name, space=space_name))
            elif office_name and not space_name:
                session.add(Person(id=person.person_id, f_name=person.person_name, occupation=person.get_type,
                                   office=office_name))
            elif not office_name and space_name:
                session.add(Person(id=person.person_id, f_name=person.person_name, occupation=person.get_type,
                                   space=space_name))
            elif not office_name and not space_name:
                session.add(Person(id=person.person_id, f_name=person.person_name, occupation=person.get_type))

        for person in self.fellow_list:
            office_name = self.retrieve_office_room(person.person_id)
            space_name = self.retrieve_space_room(person.person_id)
            add_people(person, office_name, space_name)
        for person in self.staff_list:
            office_name = self.retrieve_office_room(person.person_id)
            space_name = self.retrieve_space_room(person.person_id)
            add_people(person, office_name, space_name)
            # there is a problem here ___##################################################

        session.commit()

    def load_state(self, db_file):
        """ more like reverse engineering the above method"""
        # retrieve all rooms,
        dir = self.return_file_dir(db_file, "database")
        if os.path.exists(dir):
            # our loading database logic
            engine = create_engine('sqlite:///' + dir)
            base.metadata.bind = engine
            base.metadata.create_all(engine)
            Session = sessionmaker(bind=engine)
            session = Session()

            # query statements
            # we load offices and spaces first
            for office_name, space_name in session.query(db_office, db_space).all():
                self.office_dict[office_name] = list()
                self.living_space_dict[space_name] = list()
            # we then load people
            for person in session.query(Person).filter(Person.office_name == 'None').filter(Person.living_space_name == 'None'):
                # create_ this person's object and append it to the relevant lists/ dictionaries
                if person.occupation == "fellow":
                    person_obj = Fellow(person.full_name, person.person_id)
                    self.fellow_list.append(person_obj)
                    self.unallocated_list.append(person_obj)
                elif person.occupation == "staff":
                    person_obj = Staff(person.full_name, person.person_id)
                    self.staff_list.append(person_obj)
                    self.unallocated_list.apend(person_obj)
            for person in session.query(Person).filter(Person.office_name != 'None').filter(Person.living_space_name == 'None'):
                # people who have offices buut no livng_space
                if person.occupation == "fellow":
                    person_obj = Fellow(person.full_name, person.person_id)
                    self.fellow_list.append(person_obj)
                    self.unallocated_living_list.append(person_obj)
                    self.office_dict[person.office_name].append(person.full_name)
                if person.occupation == "staff":
                    person_obj = Staff(person.full_name, person.person_id)
                    self.staff_list.append(person_obj)
                    self.office_dict[person.office_name].append(person.full_name)
            for person in session.query(Person).filter(Person.office_name != 'None'). filter(Person.living_space_name != 'None'):
                if person.occupation == "staff":
                    raise TypeError("staff should not have an living space")
                elif person.occupation == "fellow":
                    person_obj = Fellow(person.full_name, person.person_id)
                    self.fellow_list.append(person_obj)
                    self.office_dict[person.office_name].append(person.full_name)
                    self.living_space_dict[person.living_space_name].append(person.full_name)

        else:
            print("database was not found")
            return False

    def get_empty_rooms(self, current_diction, max_num_of_rooms):
        """ gets a diction with rooms that are full and others that are not full
        it then returns the offices that are not full"""
        non_full_diction = {}
        for i in current_diction.keys():
            if len(current_diction[i]) < max_num_of_rooms:
                non_full_diction[i] = current_diction[i]
        return non_full_diction

    def get_number_in_room_dictionary(self, dictionary):
        count = 0
        for i in dictionary.keys():
            for list_value in dictionary[i]:
                if list_value:
                    count += 1
        return count

    def display(self):
        """ using this only for debugging purposes"""
        print("\nliving_space ", self.living_space_dict)
        print("office_dict", self.office_dict)
        print("staff_list", self.staff_list)
        print("fellow_list", self.fellow_list)
        print("unallocate_list", self.unallocated_list)
        print("unallocated_living_list", self.unallocated_living_list, "\n")

    def search_name(self, search_parameter):
        """" Task1: Takes in a str name of any object and finds the object associated with that string"""

        if len(re.findall('\S+', search_parameter)) < 2:
            if search_parameter in self.living_space_dict:
                return "LivingSpace"
            elif search_parameter in self.office_dict:
                return "Office"
        elif len(re.findall('\S+', search_parameter)) >= 2:
            for i in self.unallocated_list:
                if i.person_name == search_parameter:
                    return i.get_type
            for i in self.fellow_list:
                if i.person_name == search_parameter:
                    return i.get_type
            for i in self.staff_list:
                if i.person_name == search_parameter:
                    return i.get_type
        return False

    def get_all_ids(self):
        """ retrieve all dictionaries that store people with ids an returns a list containing the ids"""
        person_ids_list = []
        for obj_index in self.fellow_list:
            person_ids_list.append(obj_index.person_id)
        for obj_index in self.staff_list:
            person_ids_list.append(obj_index.person_id)

        return person_ids_list

    def id_is_present(self, person_id):
        """ retrieve the all ids list"""
        # then checks if the parsed in id is present and then returns True or False
        all_ids = self.get_all_ids()
        if person_id in all_ids:
            return True
        else:
            return False

    def retrieve_person_by_id(self, person_id):
        """ Task2: Thought: have a function that can retrieve a person object when only given either the person's id
         or the person's name"""
        for person in self.fellow_list:
            if person.person_id == person_id:
                return person
        for person in self.staff_list:
            if person.person_id == person_id:
                return person
        return "no one was found with the id: " + person_id

    def view_person_id(self):
        """Seeing that ids are assigned by the system i thought it wise to include a function that lists
        a person and his/her id"""
        # for person in fellow and staff list, format string output, first column as name and second as id
        for person in self.fellow_list:
            print(person.person_name, ": ", person.person_id)
        for person in self.staff_list:
            print(person.person_name, ": ", person.person_id)

        """                                     NOTES
            CONSIDERATIONS:

                3 using mock module to simulate a user's input for successful testing -->

                6. in several places i find that using the with keyword will shorten code; this are esp. areas
                    in operning and reading files


                7. just a thought, whatif the person's object did track their allocation status i think this would
                be quite computationaly significant.
                8. remove the broker stage between the application and the database, the stage where there is pending
                data within the system that is yet to be commited, this is to help secure against system failure.
                9. a user cannot load state unless he/she has saved the state --> to avoid session data collision
                10. quiz: if we tried saving data that is already in the database what happens
                11. correcty review the logic of especially how fellow who requested accomodation and did not recieve
                is handled when being saved to the database as well as being retrieved
                12 i find there is still an issue with input file loaded data because of person ids; i think i
                     the way about this randomising the id process where one is not given

                                            ADDITIONAL FEATURES
                1.add text conditional coloring
                2. consider adding  a gui
                3. rename_room
                4. delete_room
                    maybe we can say modify room with optional flags that specify whether rename or delete
                5.modify person: flags: remove_person, modify any property of a person's data including the id, name, and
                    occupation. the last however is onedirectional, only fellows can become staff and nor vice versa
                6.Print_room: considerations : the general output lookout, add csv output support, add printing capabilities
                7.Print_allocations: styling, csv output support; add physical print capabilities
                8. print_unallocations: styling, consider csv output; consider physical print
                9: reallocate Person level seems not to have a way in which it can be upgraded
                10. load_people: Addd csv input capabilities,

                                                        RESOLVED
                1 the reallocate person should have also been used to allocate unallocated persons to a room.
                2 i also think that the os.path module can help simplify on the functionality of testing to see
                if a certain file is existent.
                5. the return boolean value for sel.id_is_present are inverted
                4 the add_person maybe can have a fourth parameter that takes in a person's id => the problem
                    is that if we say that a person can be assigned an id after their objects are initialised then
                    that would mean that we are not fully initialising our objects. -> resolved

                2.8 Also on a same note, there is the question that where should a file be so that it can be accessed
                 by the system; i mean is there some specific place where the user must place a file that is being used
                 by the system and in what way can we make this process more dynamic and more user friendly
                    """
