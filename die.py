#!/usr/bin/env python
"""A simple dice module.
"""
# from ConfigParser import ConfigParser
from goal import Goal
from random import randint, seed
from roll import Roll
import itertools
import types

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
# TODO initialize DICE from config
# TODO remove from DICE based on class variables
# TODO limit list size of get_probability, limit size of dice
# TODO set_function(func) for die, calling function with roll value as
# argument for function
# TODO get_probability variant where fraction is given instead of percent
# for probability of value occurence
# TODO dice_utils module
# TODO store func result in Roll object???
# TODO dice_set object? Expand list functionality?

def get_most_likely_roll(dice_set=DICE):
    """Given a set of dice, returns the value(s) that have the highest
    chance of occuring.
    """
    highest = 0
    highest_list = [0]
    probs = get_probability(dice_set=dice_set)
    for prob in probs:
        if probs[prob] > highest:
            highest_list = [prob]
            highest = probs[prob]
        elif probs[prob] == highest:
            highest_list.append(prob)
    return highest_list

def get_probability(dice_set=DICE):
    """Given a set of dice, returns a dictionary of possible roll values and
    their probability of coming up in percent.
    """
    results = {}
    possible_rolls = []
    count = 0
    for die in dice_set:
        possible_rolls.append(die.possible_rolls())

    possible_rolls = itertools.product(*possible_rolls)

    for result in possible_rolls:
        total = sum(result)
        if total in results:
            results[total] += 1
        else:
            results[total] = 1
        count += 1

    for key in results:
        results[key] = float(results[key])/float(count) * 100
    return results

def get_minimum_roll(dice_set=DICE):
    """Return the smallest roll possible given a set of dice.
    """
    minimum_roll = 0
    for die in dice_set:
        offset = die.offset
        minimum_roll += (offset + 1)
    return minimum_roll

def get_maximum_roll(dice_set=DICE):
    """Return the largest roll possible given a set of dice.
    """
    maximum_roll = 0
    for die in dice_set:
        maximum_roll += die.max_roll + die.offset
    return maximum_roll

def roll_set(dice_set=DICE, count=1, goal=None):
    """Roll a given dice set and return the list of dice. The results are
    stored in each dice's __rolls variable.

    The optional argument count determines the number of times to roll
    the dice set.

    The optional agrument goal determines the goal against which the dice
    rolls will be checked.
    """
    for dice in dice_set:
        dice.roll(count=count, goal=goal)
    return dice_set


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
        self.__goal = None
        self.__func = None
        self.__rolls = []

        self.check_vars()

        DICE.append(self)

    def __str__(self):
        """The print-out of a Dice object.
        """
        self.check_vars()
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
        self.check_vars()
        result = None
        if goal == None and self.__goal != None:
            goal = self.__goal

        for i in range(count):
            value = randint(
                self.offset + 1,
                self.max_roll + self.offset + 1
            )
            if self.__func != None:
                result = self.__func(value)
            self.__rolls.insert(
                0,
                Roll(self, value, goal=goal, result=result)
            )

    def rolls(self):
        """Returns the list of rolls for the dice.
        """
        return self.__rolls

    def set_goal(self, goal):
        """Sets the goal of the dice to be used as a default for rolls.
        """
        if isinstance(goal, Goal):
            self.__goal = goal
        else:
            self.__goal = Goal(value=goal)

    def set_function(self, func, clear_rolls=True):
        """This method assigns a function to a dice, which is executed
        with each roll, and recieves a the Roll object as an argument.

        Optional argument clear_rolls sets __rolls to an empty list if
        True.
        """
        if isinstance(func, types.FunctionType):
            if func == self.__func:
                return
            self.__func = func
            if clear_rolls == True:
                self.__rolls = []
            self.__check_func()
        else:
            self.__func = None

    def possible_rolls(self):
        """Returns a list of possible roll values, not including Mod.
        """
        possible_rolls = []
        for num in range(self.offset + 1, self.offset + self.max_roll + 1):
            possible_rolls.append(num)
        return possible_rolls

    def check_vars(self):
        """Maintain the validity of Dice variables.
        """
        self.__check_max_roll()
        self.__check_offset()
        self.__check_name()
        self.__check_modifier()
        self.__check_rolls()
        self.__check_goal()
        self.__check_func()

    ########################################################################
    # Private Methods
    ########################################################################


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

    def __check_goal(self):
        """Dice's goal should be checked by Goal class verification.
        """
        if isinstance(self.__goal, Goal):
            self.__goal.check_vars()
        elif self.__goal != None:
            self.__goal = Goal(self.__goal)

    def __check_func(self):
        """Dice's function should be a FunctionType and be able to take an
        integer argument.
        """
        message = "Function %s() does not accept integer arguments."
        if isinstance(self.__func, types.FunctionType):
            try:
                temp = self.__func(1)
            except ValueError:
                raise Exception(message % self.__func)
        else:
            self.__func = None
