# Copyright (c) 2018, Adham Hashibon and Materials Informatics Team
# at Fraunhofer IWM.
# All rights reserved.
# Redistribution and use are limited to the scope agreed with the end user.
# No parts of this software may be used outside of this context.
# No redistribution is allowed without explicit written permission.

from abc import ABCMeta, abstractmethod
from copy import deepcopy
from uuid import UUID

import cuds.classes
from cuds.utils import check_arguments
# from wrappers.abc_interoperability_layer \
#    import ABCInteroperabilityLayer


class ABCSemanticLayer(object, metaclass=ABCMeta):
    """
    ABC for the semantic layer of a wrapper to CUDS
    """

    @abstractmethod
    def __init__(self, path_to_subelement=None,
                 interoperability_layer=None):
        """
        Constructor.

        :param path_to_subelement: path from the root to the referenced element
        :param interoperability_layer: shared instance of the intOp layer
        """
        if interoperability_layer is None:
            # self._intop = ABCInteroperabilityLayer()
            self._intop = None
            self._path = []
        else:
            self._intop = interoperability_layer
            self._path = path_to_subelement

    def __getattr__(self, item):
        """
        Redefines the dot notation access to access the attributes
        that belong to a cuds entity.

        :param item: attribute to get
        :return: value of that attribute if it belongs to an entity or None
        :raises AttributeError: the accessed attribute does not exist
        """
        if item in cuds.classes.cuds_attributes:
            return getattr(self._intop.get(self._path), item)

    def __setattr__(self, name, value):
        """
        Overwrites the dot notation to set the properties,
        also setting the ones belonging to a cuds entity.

        :param name: name of the property
        :param value: value of the property
        """
        if name in cuds.classes.cuds_attributes:
            self._intop.update_attribute(self._path, name, value)
        else:
            self.__dict__[name] = value

    def __bool__(self):
        """
        Overwrites the bool() method to match osp-core behaviour

        :return: true if the element contains subelements, false otherwise
        """
        return bool(self._intop.get(self._path))

    @abstractmethod
    def __str__(self):
        return self.string("wrapper")

    def string(self, name):
        """
        Builds the string returned in the __str__ method.

        :param name: name of the wrapper
        :return: string with the uid of the referenced object
        """
        string = "<" + name + " instance to object " + \
                 str(self._intop.get(self._path).uid) + ">"
        return string

    def add(self, *args):
        """
        Adds (a) cuds object(s) to their respective cuds.CUBA key entries using
        a specific function.
        Before adding, check for invalid keys to aviod inconsistencies later.

        :param args: object(s) to add
        :raises ValueError: adding an element already there
        """
        check_arguments('all_simphony_wrappers', *args)
        for cuds_object in args:
            self._intop.add(self._path, cuds_object)
        return self

    def get(self, *keys):
        """
        Returns the contained elements of a certain uid.

        :param keys: UIDs of the elements
        :return: list of objects of that type
        """
        check_arguments(UUID, *keys)
        output = []

        for key in keys:
            child = self._intop.get(self._path + [key])
            # Wrap to new instances of Semantic Layer
            child_semantic = self._wrap(child)
            output.append(child_semantic)
        return output

    def remove(self, *args):
        """
        Removes an element from the DataContainer and thus
        also its contained elements.

        :param args: object or UID of the object to remove
        """
        check_arguments((UUID, cuds.classes.DataContainer), *args)
        for arg in args:
            if isinstance(arg, cuds.classes.DataContainer):
                arg = arg.uid
            self._intop.remove(self._path + [arg])

    def update(self, *args):
        """
        Updates the object with the newer versions of the subelements.

        :param args: element(s) to update
        """
        check_arguments('all_simphony_wrappers', *args)
        for cuds_object in args:
            self._intop.update(self._path, cuds_object)

    def iter(self, cuba_key=None):
        """
        Iterates over all the objects contained or over a specific type.

        :param cuba_key: type of the objects to iterate through
        """
        if cuba_key is None:
            yield from self._iter_all()
        else:
            check_arguments(cuds.classes.CUBA, cuba_key)
            yield from self._iter_by_key(cuba_key)

    def _iter_all(self):
        """
        Iterates over all the first level children
        """
        for cuds_object in self._intop.get(self._path).iter_all():
            yield self._wrap(cuds_object)

    def _iter_by_key(self, cuba_key):
        """
        Iterates over the first level children of a specific type

        :param cuba_key: type of the children to filter
        """
        for cuds_object in self._intop.get(self._path).iter_by_key(cuba_key):
            yield self._wrap(cuds_object)

    def run(self):
        self._intop.run()

    def get_cuds(self, *uids):
        """
        Returns native osp-core copies of the internal CUDS

        :param uids:
        :return:
        """
        check_arguments(UUID, *uids)
        objects = []
        for uid in uids:
            objects.append(
                deepcopy(self._intop.get(self._path + [uid])))
        return objects

    def _wrap(self, cuds_object):
        """
        Creates a proxy to a subelement of the current cuds

        :param cuds_object: new virtual root for the wrapper
        :return: instance of the semantic layer with a subelement
        """
        if cuds_object is None:
            return None
        else:
            new_path = self._path + [cuds_object.uid]
            # __class__ will point to the concrete implementation
            return self.__class__(new_path, self._intop)
