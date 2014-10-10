#!/usr/bin/env python
"""A simple Goal module to work with die and roll.
"""
DEF_VALUE = 1
DEF_ABOVE = True

class Goal(object):
    """This class encapsulates information about the goal associated with
    a die roll.
    """
    def __init__(self, value=DEF_VALUE, above=DEF_ABOVE):
        """A goal has an associated value and an above boolean, indicating
        whether or not a successful roll value has to be above or below
        the goal's value.
        """
        self.value = value
        self.above = above

        self.__check_vars()

    def __check_vars(self):
        """Make sure that object variables are valid, otherwise, they are
        reset to default values.
        """
        self.__check_value()
        self.__check_above()

    def __check_value(self):
        """The value of the Goal object should always be a positive number.
        """
        try:
            self.value = int(self.value)
        except ValueError:
            self.value = DEF_VALUE

        if self.value <= 0:
            self.value = DEF_VALUE

    def __check_above(self):
        """Above should be either True or False.
        """
        possible = [True, False]
        if self.above not in possible:
            self.above = True
