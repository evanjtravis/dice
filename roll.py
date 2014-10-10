#!/usr/bin/env python
"""A simple Roll module to be used by dice.
"""
from goal import Goal

DEF_GOAL = Goal()

class Roll(object):
    """This class encapsulates information about each roll of a certain die.
    """
    def __init__(self, dice, value, goal=None):
        """A Roll has an associated dice, a value, and a possible goal.
        """
        self.dice = dice
        self.value = value
        self.goal = goal
        self.roll_number = self.value - self.dice.offset

        self.__check_vars()

        self.status = self.is_successful()

    def is_successful(self):
        """Returns true if the value of the roll meets or exceeds the goal.
        """
        self.__check_vars()
        successful = False

        if self.goal == None:
            return None
        else:
            if self.goal.above == True:
                if self.roll_number >= self.goal.value:
                    successful = True
            else:
                if self.roll_number <= self.goal.value:
                    successful = True
        return successful

    def __check_vars(self):
        """Make sure that object variables are valid, otherwise, they are
        set to default values.
        """
        self.__check_goal()

    def __check_goal(self):
        """A goal should either be a Goal object or an integer that is then
        used to create a Goal object.
        """
        if isinstance(self.goal, Goal):
            return
        else:
            try:
                self.goal = int(self.goal)
            except ValueError:
                self.goal = DEF_GOAL
            self.goal = Goal(value=self.goal)
