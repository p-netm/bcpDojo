__author__ = 'Sudo Pnet'
import unittest

from bcpDojo.models.dojo import Dojo
from bcpDojo.models.housing import LivingSpace, Office, Staff, Fellow


class Task0AdditionalUtilityMethods(unittest.TestCase):

    def test_get_empty_dictionary_method(self):
            # testing for living space

        dojo1 = Dojo()
        diction = {'room2': ['bang', 'big', 'theory'],
                   'room3': ['red', 'green', 'orange', 'violet', 'purple', 'yellow'],
                   'room1': [],
                   'room4': ['coast', 'Nairobi', 'Kisumu', 'Central']}
        new_diction = dojo1.get_empty_rooms(diction, 4)
        self.assertDictEqual(new_diction, {'room2': ['bang', 'big', 'theory'], 'room1': []},
                             msg="review the get empty dictionary for living space")

        # testing for offices
        new_diction = dojo1.get_empty_rooms(diction, 6)
        self.assertDictEqual(new_diction, {'room2': ['bang', 'big', 'theory'], 'room1': [],
                                       'room4': ['coast', 'Nairobi', 'Kisumu', 'Central']},
                         msg="review the get empty dictionary for offices ")

    def test_get_number_of_people_in_rooms_dict(self):
        # assert that get numbers counts the number of people in a dictionary key value pair as shown below

        dojo1 = Dojo()
        diction = {'room2': ['bang', 'big', 'theory'],
                   'room3': ['red', 'green', 'orange', 'violet', ' purple', 'yellow'],
                   'room1': [],
                   'room4': ['coast', 'Nairobi', 'Kisumu', 'Central']}
        number = dojo1.get_number_in_room_dictionary(diction)
        self.assertEqual(number, 13, msg="get the number of people function malfunctioned")

    def test_assign_living_space_function(self):
        # checks that a no rooms created message is returned when there are no rooms to assign people

        dojo1 = Dojo()
        fellow1 = Fellow("fellow name", '3254879')
        self.assertEqual(dojo1.assign_living_space(fellow1), False,
                         msg="assign living_space failed")

    def test_assign_office_space_function(self):
        # checks that a no rooms created message is returned when there are no rooms to assign people

        dojo1 = Dojo()
        fellow1 = Fellow("fellow name", '5687432')
        self.assertEqual(dojo1.assign_office(fellow1), False, msg="assign office failed")


        # Read Me: i changed this implementation so that we can use the number of offices to check of the duplicate rooms
        # were indeed created instead of returning before the program execution has finished

    # def test_duplicate_offices(self):
    #     # creates a room twice checks if it detects rooms has already been created
    #
    #     dojo1 = Dojo()
    #     initial_dict = dojo1.create_room("office", ['room1'])
    #     self.assertDictEqual(initial_dict, {'room1': []}, msg="room was not created ")
    #     statement = "Room named: room1 is already created"
    #     current_dict = dojo1.create_room('office', ['room1'])
    #     self.assertEqual("Error raised", current_dict, msg="room should not have been created")
    #
    # def test_duplicate_living_spaces(self):
    #     # create a living_space twice and see  if it throws an error
    #
    #     dojo1 = Dojo()
    #     initial_dict = dojo1.create_room("living_space", ['room1'])
    #     current_dict = dojo1.create_room("living_space", ['room1'])
    #     self.assertEqual("Error raised", current_dict, msg="room should not have been created")
    #
