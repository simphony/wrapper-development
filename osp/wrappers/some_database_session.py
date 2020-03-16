# Copyright (c) 2014-2019, Adham Hashibon, Materials Informatics Team,
# Fraunhofer IWM.
# All rights reserved.
# Redistribution and use are limited to the scope agreed with the end user.
# No parts of this software may be used outside of this context.
# No redistribution is allowed without explicit written permission.

# TODO: Import the python connection to the DB

from osp.core.session import DbWrapperSession


class SomeDatabaseSession(DbWrapperSession):
    """
    Session class for some DB.
    """

    def __init__(self, engine=None, **kwargs):
        # TODO instantiate or connect to the engine
        super().__init__(engine=engine, **kwargs)

    def __str__(self):
        # TODO define the output of str(SomeDatabaseSession)
        pass

    # OVERRIDE
    def close(self):
        # TODO close the connection to the database
        pass

    # OVERRIDE
    def _commit(self):
        # TODO commit the transaction
        pass

    # OVERRIDE
    def _init_transaction(self):
        # TODO initialise the transaction
        pass

    # OVERRIDE
    def _rollback_transaction(self):
        # TODO rollback the transaction
        pass

    # OVERRIDE
    def _initialise(self):
        # TODO load by cuba key
        pass

        # OVERRIDE
    def _apply_added(self, root_obj, buffer):
        """Adds the added cuds to the engine."""
        # TODO: What should happen in the engine
        # when the user adds a certain cuds?
        # The given buffer contains all the added CUDS object in a dictionary

    # OVERRIDE
    def _apply_updated(self, root_obj, buffer):
        """Updates the updated cuds in the engine."""
        # TODO: What should happen in the engine
        # when the user updates a certain cuds?
        # The given buffer contains all the updated CUDS object in a dictionary

    # OVERRIDE
    def _apply_deleted(self, root_obj, buffer):
        """Deletes the deleted cuds from the engine."""
        # TODO: What should happen in the engine
        # when the user removes a certain cuds?
        # The given buffer contains all the deleted CUDS object in a dictionary

    # OVERRIDE
    def _load_by_oclass(self, oclass, update_registry=False):
        # TODO load the cuds objects with the given ontology class
        # (inclusive sub-classes)
        pass

    def _load_first_level(self):
        # TODO Load the first level cuds objects.
        # These are the cuds objects, 
        # that are direct neighbors of the wrapper
        pass

    def _load_from_backend(self, uids, expired=None):
        # TODO load cuds objects from the backend
        pass
