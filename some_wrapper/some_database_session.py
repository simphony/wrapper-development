# Copyright (c) 2014-2019, Adham Hashibon, Materials Informatics Team,
# Fraunhofer IWM.
# All rights reserved.
# Redistribution and use are limited to the scope agreed with the end user.
# No parts of this software may be used outside of this context.
# No redistribution is allowed without explicit written permission.

# TODO: Import the python connection to the DB

from cuds.session.db.db_wrapper_session import DbWrapperSession


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
        # TODO initialize the transaction
        pass

    # OVERRIDE
    def _rollback_transaction(self):
        # TODO rollback the transaction
        pass

    # OVERRIDE
    def _initialize(self):
        # TODO load by cuba key
        pass

        # OVERRIDE
    def _apply_added(self):
        # TODO: What should happen in the engine when the user adds a certain cuds?
        # Use self._added.values()
        pass

    # OVERRIDE
    def _apply_updated(self):
        # TODO: What should happen in the engine when the user updates a certain cuds?
        # Use self._updated.values()
        pass

    # OVERRIDE
    def _apply_deleted(self):
        # TODO: What should happen in the engine when the user removes a certain cuds?
        # Use self._deleted.values()
        pass

    # OVERRIDE
    def _load_by_cuba(self, cuba, update_registry=False):
        # TODO load the cuds objects with the given cuba key
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
