import unittest

from bcpDojo.program.dojo import Dojo
from bcpDojo.program.housing import LivingSpace, Office, Staff, Fellow


class InstancesTests(unittest.TestCase):
    def setUp(self):
        self.living_space1 = LivingSpace("living_space_name")
        self.staff1 = Staff("person_name", '3254698')
        self.fellow1 = Fellow("fellow_name", '1235687')
        self.office1 = Office("office_name")

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

    def test_modify_room_function(self):
        """test to see that room attributes change accordingly. """
        pass


class SearchName(unittest.TestCase):
    def setUp(self):
        self.util = Dojo()
        # load 2 rooms , load 2 space, load 2 fellows, load 2 staff
        self.util.create_room("office", ['mombasa', 'Nairobi'])
        self.util.create_room("living_space", ['21', '22'])
        self.util.add_person('Peter', 'Muriuki', 'fellow', 'y', '89702323')
        self.util.add_person('Dennis', 'Njuguna', 'fellow', 'n', '5687432')
        self.util.add_person('James', 'Mwendia', 'staff', 'n', '4421222')
        self.util.add_person('derrick', 'Muriithi', 'staff', 'n', '2162187')

    def tearDown(self):
        # please go through a proper definition of what this is supposed to do
        del(self.util)

    def test_search_name_function(self):
        """ This function is given a name and returns the type of the object with that name as a string"""
        # normal operations
        self.assertEqual(self.util.search_name('mombasa'), "Office")
        self.assertEqual(self.util.search_name('21'), "LivingSpace")
        self.assertEqual(self.util.search_name('peter muriuki'), 'Fellow')
        self.assertEqual(self.util.search_name('james mwendia'), 'Staff')

        # search using a single word, add a person with the same name as a room, and repeat
        self.assertEqual(self.util.search_name('dennis njuguna'), "Fellow")
        self.util.add_person('Nairobi', 'Muriuki', 'fellow', 'y', '32320798')
        self.assertEqual(self.util.search_name('nairobi', category='person'), 'Fellow')

    def test_modify_room_name_function(self):
        """This function checks that the renamed room changes room name"""
        self.util.modify_room_name('mombasa', new_room_name="kutus", room_type='office')
        self.assertIn('kutus', self.util.office_dict.keys())
        self.assertNotIn('mombasa', self.util.office_dict.keys())

    def test_delete_room_function(self):
        """This function checks that a room ceases to exist after deletion and allocated users reduce"""
        # we create a room and delete it
        self.util.create_room('office', ['kerugoya'])
        self.assertIn('kerugoya', self.util.office_dict.keys())
        self.util.delete_room('kerugoya')
        self.assertNotIn('kerugoya', self.util.office_dict.keys())

    def test_search_id_for_function(self):
        """if two people share a common name, one name, both-names, returns alist of ids, retrun empty list if none """
        self.util.add_person('Peter', 'Muriuki', 'fellow', 'y', '89702313')
        self.util.add_person('Keneth', 'Muriuki', 'staff', 'n', '89702343')
        self.util.add_person('Peter', 'Muriuki', 'fellow', 'n', '89702393')
        self.assertTrue(type(self.util.search_id_for('peter')) is list)
        self.assertEqual(3, len(self.util.search_id_for('peter')))
        self.assertEqual(4, len(self.util.search_id_for('muriuki')))