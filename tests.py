#!/usr/bin/env python
"""Test cases for the die module.
"""

from unittest import TestCase
import die

class TestDiceClass(TestCase):
    """Test Class for Dice object.
    """
    def tearDown(self):
        """
        """
        die.DICE = []

    def test_remove_die(self):
        """
        """
        size = len(die.DICE)
        d = die.Die(21, name='Test')
        self.assertEqual(len(die.DICE), size + 1)
        
        die.remove(d)
        self.assertEqual(len(die.DICE), size)

    def test_invalid_max_roll(self):
        """A Dice created with an invalid max_roll will set max_roll to the
        default value.
        """
        d = die.Die(-1)
        self.assertEqual(d.max_roll, die.DEF_MAX)
        
        d = die.Die('sdfsd')
        self.assertEqual(d.max_roll, die.DEF_MAX)
        
        d = die.Die(True)
        self.assertEqual(d.max_roll, die.DEF_MAX)

        d = die.Die(0.7)
        self.assertEqual(d.max_roll, die.DEF_MAX)

    def test_invalid_offset(self):
        """A Dice created with an invalid offset will set offset to the
        default value.
        """
        d = die.Die(2, offset=-1)
        self.assertEqual(d.offset, die.DEF_OFFSET)

        d = die.Die(2, offset='sdfsdf')
        self.assertEqual(d.offset, die.DEF_OFFSET)

        d = die.Die(2, offset='False')
        self.assertEqual(d.offset, die.DEF_OFFSET)
        
        d = die.Die(2)
        self.assertEqual(d.offset, die.DEF_OFFSET)
        
    def test_set_name(self):
        """A Dice created with an empty name will set name to the default
        value.
        """
        d = die.Die(2, name=None)
        self.assertEqual(d.name, die.DEF_NAME)

if __name__ == '__main__':
    unittest.main()
