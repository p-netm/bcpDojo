import unittest

from bcpDojo.models.dojo import Dojo
from bcpDojo.models.housing import LivingSpace, Office, Staff, Fellow


class InstancesTests(unittest.TestCase):
    def setUp(self):
        self.living_space1 = LivingSpace("living_space_name")
        self.staff1 = Staff("person_name", '3254698')
        self.fellow1 = Fellow("fellow_name", '1235687')
        self.office1 = Office("office_name")

    @unittest.skip
    def test_if_instance(self):
        self.assertIsInstance(self.staff1.person_id, str,
                              msg=" the staff id should be a string")
        self.assertIsInstance(self.fellow1.person_id, str,
                              msg=" the fellow id should be a string")

class TestsForTask0(unittest.TestCase):
    """ This class tests the add_person function and the create_room function"""

    def setUp(self):
        pass

    def test_valid_room_arg(self):
        # checks if that the function works with the right inputs

        dojo1 = Dojo()
        initial_length = len(dojo1.living_space_dict)
        print("living_space: ", dojo1.living_space_dict, initial_length)
        dojo1.create_room("living_space", ['room1', 'room2', 'room3'])
        print("living_space: ", dojo1.living_space_dict, len(dojo1.living_space_dict))
        current_length = len(dojo1.living_space_dict)
        self.assertEqual(current_length - initial_length, 3,
                         msg=" three rooms increases room count to three")

    def test_valid_office_arguments(self):
        # checks that the offices are created with the right input

        dojo1 = Dojo()
        initial_length = dojo1.get_number(dojo1.office_dict)
        dojo1.create_room("office", ['office1', 'office2', 'office3'],)
        current_length = dojo1.get_number(dojo1.office_dict)
        self.assertEqual(current_length - initial_length, 3,
                         msg=" three offices increases office count to three")

    def test_invalid_room_arg(self):
        # checks if issues are brought up when wrong room_name arguments are passed

        dojo1 = Dojo()
        initial_length = dojo1.get_number(dojo1.living_space_dict)
        dojo_add_room = dojo1.create_room("living_space", ['33', ['room1', 'room2'], {}])
        self.assertEqual(dojo_add_room, "Invalid room name",
                                        msg="Invalid name for room name argument")
        current_length = dojo1.get_number(dojo1.living_space_dict)
        self.assertEqual(current_length - initial_length, 0, msg="the room list remains unimplemented")
    #
    def test_invalid_office_arguments(self):
        # checks that the create room throws error for invalid arguments

        dojo1 = Dojo()
        initial_length = dojo1.get_number(dojo1.office_dict)
        dojo_add_office = dojo1.create_room("office", ['33', ['office1', 'office2'], {}])
        self.assertEqual(dojo_add_office, "Invalid room name",
                         msg="Invalid name for office name argument")
        current_length = dojo1.get_number(dojo1.office_dict)
        self.assertEqual(current_length - initial_length, 0,
                         msg="the office list remains unimplemented")

    def test_add_person_function_without_accommodate(self):
        """ add person: takes name fellow|staff and accommodate"""

        dojo1 = Dojo()
        initial_length = dojo1.get_number(dojo1.fellow_list)
        dojo1.add_person("Kelvin", "Njogu", "fellow", "n", '32320798')
        current_length = dojo1.get_number(dojo1.fellow_list)
        self.assertEqual(current_length - initial_length, 1, msg=" fellow created should add to the fellow list count")

    def test_add_person_function_with_accommodate(self):

        dojo1 = Dojo()
        initial_length = dojo1.get_number(dojo1.fellow_list)
        dojo1.add_person("Kelvin", "Njogu", "fellow", "yes", '1234567')
        current_length = dojo1.get_number(dojo1.fellow_list)
        self.assertEqual(current_length - initial_length, 1,
                         msg=" fellow created should add to the fellow list count")

