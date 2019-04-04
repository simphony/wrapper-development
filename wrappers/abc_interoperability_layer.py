# Copyright (c) 2018, Adham Hashibon and Materials Informatics Team
# at Fraunhofer IWM.
# All rights reserved.
# Redistribution and use are limited to the scope agreed with the end user.
# No parts of this software may be used outside of this context.
# No redistribution is allowed without explicit written permission.

from abc import ABCMeta, abstractmethod
from copy import deepcopy

# from wrappers.abc_cuds_checker import ABCCudsChecker


class ABCInteroperabilityLayer(object, metaclass=ABCMeta):
    """
    ABC for the interoperability between the semantic and syntactic layer.
    Here will be stored the internal copy of cuds
    """
    def __init__(self):
        # self._cuds_checker = ABCCudsChecker()
        self._cuds_checker = None
        self._cuds = None
        self._ran = False

    def run(self):
        self._check_cuds()
        if not self._ran:
            self._add_whole_cuds()
            self._ran = True
        self._run_engine()
        self._update_cuds_after_run()

    def _check_cuds(self):
        self._cuds_checker.check_all(self._cuds)

    @abstractmethod
    def _run_engine(self):
        pass

    @abstractmethod
    def _update_cuds_after_run(self):
        pass

    def get(self, path):
        """
        Get a certain subelement given the path to it

        :param path: list of uids until the subelement
        :return: internal cuds on that path
        """
        new_cuds = self._cuds
        for uid in path:
            new_cuds = new_cuds.get(uid)[0]
        return new_cuds

    def add(self, path, entity):
        """
        Adds an entity
        :param path:
        :param entity:
        :return:
        """
        current = self.get(path)
        current.add(deepcopy(entity))
        if self._ran:
            self._add_by_type(entity)

    @abstractmethod
    def _add_by_type(self, entity):
        pass

    @abstractmethod
    def _add_whole_cuds(self):
        pass

    def remove(self, path):
        entity = self.get(path)
        self._remove_by_type(entity)
        # Remove from internal cuds
        self.get(path[:-1]).remove(path[-1])

    @abstractmethod
    def _remove_by_type(self, entity):
        pass

    def update(self, path, entity):
        # Update internal cuds
        self.get(path).update(entity)
        self._update_by_type(entity)

    @abstractmethod
    def _update_by_type(self, entity):
        pass

    def update_attribute(self, path, name, value):
        cuds_object = self.get(path)
        setattr(cuds_object, name, value)
        if self._ran:
            self._update_in_engine(cuds_object, path)

    @abstractmethod
    def _update_in_engine(self, entity, path):
        pass
