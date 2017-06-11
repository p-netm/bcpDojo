import unittest
from ..program.housing import Office, LivingSpace, Fellow, Staff


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

