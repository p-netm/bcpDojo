import unittest
from mock import mock
from ..program.housing import Office, LivingSpace, Fellow, Staff
from ..program.dojo import Dojo


class HousingTest(unittest.TestCase):
    def setUp(self):
        """create instances of housng.<> objects and check some of their methods and properties"""
        self.fellow = Fellow('James Kariuki', '3254986')
        self.staff = Staff('Dida Sob', '3265741')
        self.office1 = Office('Masaai')
        self.space1 = LivingSpace('23')

    def tearDown(self):
        """ Delete the setup objects"""

    def test_Instance(self):
        self.assertEqual(self.fellow.person_id, '3254986')
        self.assertEqual(self.office1.room_name, 'Masaai')
        self.assertEqual(self.fellow.get_type(), "Fellow")
        self.assertEqual(self.office1.occupants, 0)
        self.assertEqual(self.office1.max_space, 4)
        self.assertEqual(self.space1.max_space, 6)
        self.assertEqual(self.space1.occupants, 0)
        self.assertEqual(self.staff.office, None)
        self.assertEqual(self.fellow.space, None)
        with self.assertRaises(AttributeError) as exception:
            self.staff.space
            self.assertTrue(exception)


class DojoTests(unittest.TestCase):
    def setUp(self):
        self.dojo = Dojo()

    def tearDown(self):
        del(self.dojo)

    def test_create_room(self):
        self.assertTrue(type(self.dojo.create_room('office', ['Nairobi', 'Mombasa'])) is list)
        self.assertTrue(type(self.dojo.instant_room("living_space", ['room3', 'room4'], self.dojo.room_list))
                        is list)
        self.assertEqual(len(self.dojo.room_list), 4)
        self.assertEqual(self.dojo.room_list[0].get_type(), "office")
        self.assertTrue(type(self.dojo.instant_room("living_space", ['21', '22'], self.dojo.room_list)) is list)
        self.assertEqual(len(self.dojo.room_list), 6)
        self.dojo.compute_variables()
        self.assertEqual(len(self.dojo.room_name_set), 6)
        self.assertEqual(len(self.dojo.get_empty_rooms('office')), 2)
        self.assertEqual(len(self.dojo.get_empty_rooms('living_space')), 4)
        string = self.dojo.instant_room('office', ['Nairobi'], self.dojo.room_list)
        self.assertTrue(string, "Office Nairobi exists.")
        dojo_add_room = self.dojo.create_room("living_space", ['33', ['room1', 'room2'], {}])
        self.assertEqual(dojo_add_room, "Invalid room name",
                                        msg="Invalid name for room name argument")

    def test_set_person_identifier_function(self):
        self.assertEqual(self.dojo.set_person_id('12345678'), '12345678')
        input_id = self.dojo.set_person_id('select')
        self.assertTrue(input_id in range(0000000, 100000000))
        with mock.patch('builtins.input', side_effect=['123', 'dsf', '12365498']):
            self.assertEqual(self.dojo.set_person_id(None), '12365498')
        with mock.patch('builtins.input', return_value="q"):
            with self.assertRaises(TypeError) as typeerror:
                self.dojo.set_person_id()
                self.assertTrue(typeerror)

    def test_add_person_functionalities(self):
        self.dojo.add_person('Kevin', 'mac', 'fellow', 'n', id='1265437')
        self.dojo.add_person('Johnson', 'Stone', 'staff', 'n', id='32156487')
        ids_list = self.dojo.get_all_ids()
        self.assertListEqual(ids_list, ['1265437', '32156487'])
        self.assertTrue(self.dojo.id_is_present('1265437'))

    def test_assign_rooms_functions(self):
        """Create rooms and then manually assign offices and living_spaces """
        self.assertTrue(type(self.dojo.create_room('office', ['Nairobi', 'Mombasa'])) is list)
        self.assertTrue(type(self.dojo.instant_room("living_space", ['21', '22'], self.dojo.room_list))
                        is list)
        fellow = Fellow('James Kariuki', '3254986')
        staff = Staff('Dida Sob', '3265741')
        self.dojo.assign_office(staff, office_name="Nairobi")
        self.assertEqual(self.dojo.get_room_by_room_name('Nairobi').occupants, 1)
        self.dojo.assign_office(fellow)
        self.dojo.assign_living_space(fellow)
        self.assertTrue(fellow.office is not None)
        self.assertTrue(fellow.space is not None)
        self.assertEqual(staff.office.room_name, "Nairobi")
        # test room_modification functions
        self.dojo.compute_variables()
        print("the current state of the room_name_set", self.dojo.room_name_set)
        renamed_room = self.dojo.modify_room_name('Nairobi', 'Kutus')
        # self.assertEqual(renamed_room.room_name, 'Kutus')
        # self.assertEqual(staff.office.room_name, 'Kutus')
        self.assertTrue(not self.dojo.get_room_by_room_name('Nairobi'))

    def test_retrieve_person_functions(self):
        self.dojo.add_person('Kevin', 'mac', 'fellow', 'n', id='1265437')
        self.dojo.add_person('Johnson', 'Stone', 'staff', 'n', id='32156487')
        person = self.dojo.retrieve_person_by_id('1265437')
        self.assertEqual(person.person_name, 'Kevin Mac')
        self.assertTrue(not self.dojo.retrieve_person_by_id('32631546'))
        person = self.dojo.retrieve_person_by_name('Kevin Mac')
        self.assertEqual(person.get_type(), 'Fellow')
        self.assertEqual(person.person_id, '1265437')
        self.assertTrue(not self.dojo.retrieve_person_by_name('ajhdgajad hsaj'))
        self.assertEqual(self.dojo.retrieve_person_by_name('Johnson Stone').get_type(), 'Staff')