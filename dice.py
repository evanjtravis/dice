#!/usr/bin/env python
"""A simple dice module.
"""
from ConfigParser import ConfigParser
from random import randint, seed

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
############################################################################
# Exceptions
############################################################################



############################################################################
# Functions
############################################################################
#TODO given a set of dice, produce list of possible rolls and their probability.
#TODO initialize DICE from config
#TODO module level roll function to call one off basic rolls calling dice.roll('d6')
# TODO update roll method to take int argument for number of times to roll, and a string argument for a basic die roll counterpart.
# TODO Roll object to encapsulate status, current_roll, and previous_roll, created and stored in rolls list in Dice, not to exceed length of 20, also keeps track of base die roll.
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

class Dice():
    """This class specifies dice used in games.
    """
    
    def __init__(self,
            max_roll, name=DEF_NAME, offset=DEF_OFFSET, mod=DEF_MOD):
        """Dice have a max roll, an offset, and a name.
        """
        self.max_roll = max_roll
        self.offset = offset
        self.name = name
        self.mod = mod
        self.__current_roll = None
        self.__previous_roll = None
        self.__critical = None

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
        if self.__current_roll:
            message += 'Cur: %d, ' % self.__current_roll
        if self.__previous_roll:
            message += 'Prev: %d' % self.__previous_roll
        return message

    ########################################################################
    # Public Methods
    ########################################################################
# TODO CHANGE TO REFLECT USE OF GOAL AND ROLL CLASSES
    def get_current_roll(self):
        """Returns the value of the current roll.
        """
        return self.__current_roll

    def get_previous_roll(self):
        """Returns the value of the previous roll.
        """
        return self.__previous_roll

    def get_critical(self):
        """Returns the value of is_critical
        """
        return self.__critical
    
    def is_critical_fail(self):
        """Returns true if the die rolls a critical fail.
        """
        return self.__critical == False

    def is_critical_success(self):
        """Returns true if the die rolls a critical success.
        """
        return self.__critical == True

    def roll(self, count=1, co_roll=None):
        """Returns a random roll from the dice along with its modifier.
        Updates current and previous rolls.
        """
        self.__step()
        if count > 0:
            if count == 1:
                value = randint(
                    self.offset + 1,
                    self.max_roll + self.offset
                )
                self.__current_roll = value
        
                if value - self.offset <= CRITICAL_FAIL:
                    self.__set_critical_failure()
                    value = CRITICAL_FAIL
                elif value - self.offset == self.max_roll:
                    self.__set_critical_success()
                
                return [(value, self.mod)]
            else:
                results = []
                for i in range(count):
                    results.append(self.roll(additional=additional))
                return results
        else:
            return []

    ########################################################################
    # Private Methods
    ########################################################################

    def __step(self):
        """Perform actions associated with moving from one roll to the next.
        """
        self.__check_vars()
        self.__clear_critical_status()
        self.__previous_roll = self.__current_roll
 
    def __check_vars(self):
        """
        """
        self.__check_max_roll()
        self.__check_offset()
        self.__check_name()
        self.__check_modifier()

    def __check_max_roll(self):
        """Make sure that any changes made to max_roll are valid.
        """
        try:
            self.max_roll = int(self.max_roll)
        except Exception:
            self.max_roll = DEF_MAX
        if self.max_roll <= CRITICAL_FAIL:
            self.max_roll = DEF_MAX

    def __check_offset(self):
        """Make sure that when and if the offset is changed, that it
        is still positive and a number.
        """
        try:
            self.offset = int(self.offset)
        except Exception:
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
        except Exception:
            self.name = DEF_NAME

    def __check_modifier(self):
        """Make sure that when and if the moddifier is changed, that it is
        still an integer.
        """
        try:
            self.mod = int(self.mod)
        except Exception:
            self.mod = DEF_MOD
