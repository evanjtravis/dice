#!/usr/bin/env python
"""A simple Roll module to be used by dice.
"""
from goal import Goal

DEF_GOAL = Goal()
SUCCESS = 'Success'
CRIT_SUCCESS = 'Critical ' + SUCCESS
FAIL = 'Failure'
CRIT_FAIL = 'Critical ' + FAIL

class Roll():
    """This class encapsulates information about each roll of a certain die.
    """
    #TODO somehow indicate tha success/failure is achieved by going ABOVE goal or going BELOW goal. TRUE or FALSE
    # TODO goal is a class, 
#TODO all editable globals in config file
    def __init__(self, dice, value, goal=None)
        """
        """
        self.dice = dice
        self.value = value
        self.goal = goal
        self.above = above
        self.roll_number = self.value - self.dice.offset

        self.__check_vars()

        self.status = self.__set_status()

    def __set_status(self):
        """Get the status of the roll.
        Statuses:
            Success: value meets or exceeds the goal
            Fail: value fails to meet the goal
            Critical Fail: value = lowest possible roll
            Critical Success: value = highest possible roll
        """
        if self.__is_successful():
            if self.roll_number == self.dice.max_roll:
                return CRIT_SUCCESS
            else:
                return SUCCESS
        else:
            if self.roll_number == 1:
                return CRIT_FAIL
            else:
                return FAIL

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

    def __is_successful(self):
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

    def __is_failed(self):
        """Returns true if the value of the roll does NOT meet or exceed
        the goal.
        """
        if self.goal == None:
            return None
        return not self.__is_successful
