# TODO: Import the python connection to the DB
from osp.core.session import DbWrapperSession


class SomeDatabaseSession(DbWrapperSession):
    """
    Session class for some database.
    """

    def __init__(self, engine=None):
        # TODO instantiate or connect to the engine
        super().__init__(engine=engine)

    def __str__(self):
        # TODO define the output of str(SomeDatabaseSession)
        pass

    def close(self):
        # TODO close the connection to the database
        pass

    def _commit(self):
        # TODO commit the transaction
        pass

    def _init_transaction(self):
        # TODO initialise the transaction
        pass

    def _rollback_transaction(self):
        # TODO rollback the transaction
        pass

    def _initialize(self):
        # TODO load by cuba key
        pass

    def _apply_added(self, root_obj, buffer):
        """Adds the added cuds to the engine."""
        # TODO: What should happen in the engine
        #  when the user adds a certain cuds?
        #  The given buffer contains all the added CUDS object in a dictionary

    def _apply_updated(self, root_obj, buffer):
        """Updates the updated cuds in the engine."""
        # TODO: What should happen in the engine
        #  when the user updates a certain cuds?
        #  The given buffer contains all the updated CUDS object in a
        #  dictionary

    def _apply_deleted(self, root_obj, buffer):
        """Deletes the deleted cuds from the engine."""
        # TODO: What should happen in the engine
        #  when the user removes a certain cuds?
        #  The given buffer contains all the deleted CUDS object in a
        #  dictionary

    def _load_by_oclass(self, oclass, update_registry=False):
        # TODO load the cuds objects with the given ontology class
        #  (inclusive sub-classes)
        pass

    def _load_first_level(self):
        # TODO Load the first level cuds objects
        #  These are the cuds objects,
        #  that are direct neighbors of the wrapper.
        pass

    # OVERRIDE
    def _load_from_backend(self, uids, expired=None):
        # TODO load cuds objects from the backend
        pass
