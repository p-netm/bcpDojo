__author__ = 'Sudo Pnet'
import unittest

from bcpDojo.models.dojo import Dojo
from bcpDojo.models.housing import LivingSpace, Office, Staff, Fellow


class TestsForPrintRoom(unittest.TestCase):
    def setUp(self):
        self.dojo = Dojo()

    def tests_room_if_non_existent(self):
        """ checks that it throws an error if the room is non-existent"""

        self.assertEqual(self.dojo.print_room("bdhsgfa"),
                              False, msg="print room should first check that there is such a room")
    def test_get_type(self):
        # this function is implemented the same in each class it basically returns the class as a string
        office = Office("office1")
        self.assertEqual(office.get_type(), "Office", msg="created office object should return 'Office'")

        living_space = LivingSpace("Living")
        self.assertEqual(living_space.get_type(), "LivingSpace", msg="created living space should return 'living_space")

    def test_search_name_function(self):
        """ a little bit level dip: returns an object whose name is the str_parameter"""

        office = self.dojo.create_room('office', ["office1"])
        string_type = self.dojo.search_name("office1")
        self.assertEqual(string_type, "Office", msg="return should be the string Office")

        living_space = self.dojo.create_room('living_space', ["room1"])
        string_type = self.dojo.search_name("room1")
        self.assertEqual(string_type, "LivingSpace", msg="returned value should have been the string 'LivingSpace'")

    def test_if_occupied(self):
        """" checks that the room is occupied."""

        self.dojo.create_room("office", ['office123'])
        self.assertEqual(self.dojo.print_room('office123'), False,
                         msg="if the room is not occupied, print room should return False")

    class TestPrintAllocations(unittest.TestCase):
        def setUp(self):
            self.dojo = Dojo()

    def test_against_golden_file(self):
        pass

    def test_against_a_formatted_string(self):
        pass

    def test_if_it_creates_a_file_if_not_found(self):
        pass