#!/usr/bin/env python
"""Test cases for the dice module.
"""

from unittest import TestCase
import dice

class TestDiceClass(TestCase):
    """Test Class for Dice object.
    """
    def setUp(self):
        """
        """
        for i in range(2, 20):
            die = dice.Dice(i, name='Name %d' % i)

    def tearDown(self):
        """
        """
        dice.DICE = []
    
    def test_dice_print(self):
        """Tests if a dice prints correctly.
        """
        die = dice.DICE[0]
        self.assertEqual(die.__str__(), 'd%d, %s' %(die.max_roll, die.name))

    def test_remove_dice(self):
        """
        """
        size = len(dice.DICE)
        die = dice.Dice(21, name='Test')
        self.assertEqual(len(dice.DICE), size + 1)
        
        dice.remove(die)
        self.assertEqual(len(dice.DICE), size)

    def test_invalid_max_roll(self):
        """A Dice created with an invalid max_roll will set max_roll to the
        default value.
        """
        die = dice.Dice(-1)
        self.assertEqual(die.max_roll, dice.DEF_MAX)
        
        die = dice.Dice('sdfsd')
        self.assertEqual(die.max_roll, dice.DEF_MAX)
        
        die = dice.Dice(True)
        self.assertEqual(die.max_roll, dice.DEF_MAX)

        die = dice.Dice(0.7)
        self.assertEqual(die.max_roll, dice.DEF_MAX)

    def test_invalid_offset(self):
        """A Dice created with an invalid offset will set offset to the
        default value.
        """
        die = dice.Dice(2, offset=-1)
        self.assertEqual(die.offset, dice.DEF_OFFSET)

        die = dice.Dice(2, offset='sdfsdf')
        self.assertEqual(die.offset, dice.DEF_OFFSET)

        die = dice.Dice(2, offset='False')
        self.assertEqual(die.offset, dice.DEF_OFFSET)
        
        die = dice.Dice(2)
        self.assertEqual(die.offset, dice.DEF_OFFSET)
        
    def test_set_name(self):
        """A Dice created with an empty name will set name to the default
        value.
        """
        die = dice.Dice(2, name=None)
        self.assertEqual(die.name, dice.DEF_NAME)

if __name__ == '__main__':
    unittest.main()
