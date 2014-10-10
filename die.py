#!/usr/bin/env python
"""A simple dice module.
"""
# from ConfigParser import ConfigParser
from random import randint, seed
from roll import Roll

seed()

############################################################################
# Globals
############################################################################
DICE = []
DEF_OFFSET = 0
DEF_NAME = 'NA'
DEF_MOD = 0
CRITICAL_FAIL = 1
DEF_MAX = CRITICAL_FAIL + 1
DEF_ROLLS_LENGTH = 20
############################################################################
# Exceptions
############################################################################



############################################################################
# Functions
############################################################################
# TODO given a set of dice, produce list of possible rolls and their
# probability.
# TODO initialize DICE from config
# TODO module level roll function to call one off basic rolls calling
# dice.roll('d6')
# TODO update roll method to take int argument for number of times to
# roll, and a string argument for a basic die roll counterpart.
# TODO Roll object to encapsulate status, current_roll, and previous_roll,
# created and stored in rolls list in Dice, not to exceed length of 20,
# also keeps track of base die roll.
def roll_set(dice_set):
    """Roll a given dice set and return the results in a dictionary.
    The Dice object is the key, the value is a tuple of the roll and
    dice modifier.
    """
    results = {}
    for dice in dice_set:
        results[dice] = dice.roll()
    return results


def roll_all():
    """Roll all of the dice that exist.
    """
    return roll_set(DICE)


def remove(dice_obj):
    """Remove a given dice from DICE.
    """
    DICE.remove(dice_obj)

############################################################################
# Classes
############################################################################

class Die(object):
    """This class specifies dice used in games.
    """
    def __init__(
            self,
            max_roll,
            name=DEF_NAME,
            offset=DEF_OFFSET,
            mod=DEF_MOD):
        """Dice have a max roll, an offset, and a name.
        """
        self.max_roll = max_roll
        self.offset = offset
        self.name = name
        self.mod = mod
        self.__rolls = []

        self.__check_vars()

        DICE.append(self)

    def __str__(self):
        """The print-out of a Dice object.
        """
        self.__check_vars()
        message = '%s: ' % self.name
        message += 'd%d' % self.max_roll
        if self.offset > 0:
            message += '+'
        if self.offset != 0:
            message += '%d, ' % self.offset
        if self.mod != 0:
            message += 'mod: %d, ' % self.mod
        return message

    ########################################################################
    # Public Methods
    ########################################################################
    def roll(self, count=1, goal=None):
        """Appends a roll to the dice's rolls list.
        """
        self.__check_vars()
        for i in range(count):
            value = randint(
                self.offset + 1,
                self.max_roll + self.offset
            )
            self.__rolls.insert(0, Roll(self, value, goal=goal))

    def get_rolls(self):
        """Returns the list of rolls for the dice.
        """
        return self.__rolls
    ########################################################################
    # Private Methods
    ########################################################################

    def __check_vars(self):
        """Maintain the validity of Dice variables.
        """
        self.__check_max_roll()
        self.__check_offset()
        self.__check_name()
        self.__check_modifier()
        self.__check_rolls()

    def __check_max_roll(self):
        """Make sure that any changes made to max_roll are valid.
        """
        try:
            self.max_roll = int(self.max_roll)
        except ValueError:
            self.max_roll = DEF_MAX
        if self.max_roll <= CRITICAL_FAIL:
            self.max_roll = DEF_MAX

    def __check_offset(self):
        """Make sure that when and if the offset is changed, that it
        is still positive and a number.
        """
        try:
            self.offset = int(self.offset)
        except ValueError:
            self.offset = DEF_OFFSET
        if self.offset <= -1:
            self.offset = DEF_OFFSET

    def __check_name(self):
        """If the name is None, then the name displayed on print should be
        NA.
        """
        if self.name == 'None':
            return
        if self.name == None:
            self.name = DEF_NAME
        try:
            self.name = str(self.name)
        except ValueError:
            self.name = DEF_NAME

    def __check_modifier(self):
        """Make sure that when and if the moddifier is changed, that it is
        still an integer.
        """
        try:
            self.mod = int(self.mod)
        except ValueError:
            self.mod = DEF_MOD

    def __check_rolls(self):
        """Dice's rolls list length shouldn't exceed DEF_ROLLS_LENGTH
        """
        self.__rolls = self.__rolls[:DEF_ROLLS_LENGTH]
