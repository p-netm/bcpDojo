import unittest

from bcpDojo.models.dojo import Dojo
from bcpDojo.models.housing import LivingSpace, Office, Staff, Fellow

class Task2tests(unittest.TestCase):
    def setup(self):
        pass

    def test_if_file_exists_function(self):
        dojo = Dojo()
        self.assertEqual(dojo.if_file_exists("asdhjdaw.txt"), False,
                         msg="such a file should not be existing")

    # dose()ef test_read_file_function_using_golden_file(self):
    #     # the read file function returns data in form of a multidimensional list
    #
    #     dojo = Dojo()
    #     file_handler = open("golden_files\read_file_function_golden_file.txt", 'r')
    #     file_contents = file_handler.read()
    #     self.assertListequl()
    #     file_handler.cl

    # def test_read_file_function_using_golden_file_with_several_lines(self):
    #     pass
    #
    def test_load_people_for_unexistent_file(self):
        dojo = Dojo()
        self.assertEqual(dojo.load_people("ashdvhadvashdbkagc.txt"), False,
                         msg="Dojo opened an inexistent file, very wierd")
    #
    # def test_for_line_feed(self):
    #     pass

class testsForReallocatePerson(unittest.TestCase):
    def setUp(self):
        pass

    def test_read_file_names_function(self):
        file_name = "load_people.txt"
        dojo = Dojo()
        self.assertIsInstance(dojo.read_file_names(file_name), list,
                              msg="the returned type should be a list")
        self.assertListEqual(dojo.read_file_names(file_name), [['OLUWAFEMI SULE', 'FELLOW', 'Y'],
                                                               ['DOMINIC WALTERS', 'STAFF', 'n'],
                                                               ['SIMON PATTERSON', 'FELLOW', 'Y'],
                                                               ['MARI LAWRENCE', 'FELLOW', 'Y'],
                                                               ['LEIGH RILEY', 'STAFF', 'n'],
                                                               ['TANA LOPEZ', 'FELLOW', 'Y'],
                                                               ['KELLY McGUIRE', 'STAFF', 'n']],
                             msg=" does not properly extract the names of people in the load people file")

    def test_if_load_people_adds_number_of_people(self):
        """will check to see if the number of fellows or staff increase accordingly, after adding them to the system """
        dojo = Dojo()
        file_name = "load_people.txt"
        dojo.load_people(file_name)
        self.assertEqual(len(dojo.fellow_list), 4, msg="there were four fellows to be added")
        self.assertEqual(len(dojo.staff_list), 3, msg="there were supposed to be three new additions to staff")

    # def tests_for_non_existent_id(self):
    #     pass
    #
    # def tests_for_non_existent_room(self):
    #     pass
    #
    # def tests_if_room_is_full(self):
    #     pass
    #
    # def test_if_unallocated_people_decrease(self):
    #     pass
    # def test_if_staff_can_rellocate_to_living_space(self):
    #     pass
    # def test_retrieve_person_by_id(self):
    #     """ create a person with an id then check if the name f the returned object is equal to
    #     what we will create the person with"""
    # def test_retrieve_room(self):
    #     pass

class RetrieveFunctions(unittest.TestCase):

    def setUp(self):
        self.dojo = Dojo()
        file_name = "load_people.txt"
        self.dojo.load_people(file_name)

    def test_retrieve_person_by_id(self):
        """will try and see if we can retrieve OLUWAFEMI SULE who should have an id of 0000001 """
        person = self.dojo.retrieve_person_by_id("0000001")
        self.assertEqual(person.get_type, "fellow", msg="the person was added as a fellow")
        self.assertEqual(person.person_name, "OLUWAFEMI SULE",
                         msg="the person name is what? ")