# Copyright (c) 2018, Adham Hashibon and Materials Informatics Team
# at Fraunhofer IWM.
# All rights reserved.
# Redistribution and use are limited to the scope agreed with the end user.
# No parts of this software may be used outside of this context.
# No redistribution is allowed without explicit written permission.

from abc import ABCMeta, abstractmethod


class ABCCudsChecker(object, metaclass=ABCMeta):
    """
    This class defines the checking functions that will be used
    by the different cuds_checkers.
    """

    @abstractmethod
    def check_all(self, cuds_object):
        """
        Calls the different functions to check for the correct entities.

        :param cuds_object: the cuds object to be checked
        """

    @staticmethod
    def _check_equal_amount(cuds_object, cuba_key, expected_amount):
        """
        Checks that a given collection contains the given amount
        and raises ValueError if not.

        :param cuds_object:
        :param cuba_key:
        :param expected_amount: Amount of elements the collection should have
        :raises ValueError: if the amounts are not equal
        """
        collection = cuds_object.get(cuba_key)
        # Ignore the None entries
        actual_amount = sum(element is not None for element in collection)
        if actual_amount != expected_amount:
            message = 'Expected {} element(s) of type {}, but got {} instead.'
            raise ValueError(message.format(expected_amount, cuba_key, actual_amount))

    @staticmethod
    def _check_children(cuds_object, cuba_key, child_value_pairs):
        """
        Checks that the contained elements in a given collection
        contain the given amount of a type and raises ValueError if not.

        :param cuds_object:
        :param cuba_key:
        :param child_value_pairs: list with tuples containing the cuba key
        and its expected value for the children
        :raises ValueError: if the amounts are not equal
        """
        collection = cuds_object.get(cuba_key)
        try:
            for child in collection:
                for pair in child_value_pairs:
                    cuba_key_child = pair[0]
                    expected_amount_child = pair[1]
                    ABCCudsChecker._check_equal_amount(
                        child, cuba_key_child, expected_amount_child)
        except AttributeError:
            message = 'Simlammps needs at least one {}'
            raise ValueError(message.format(cuba_key))
