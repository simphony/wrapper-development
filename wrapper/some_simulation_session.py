# Maybe some copyright stuff goes here

# TODO: Import the python connection to the engine

import cuds.classes
from cuds.classes import CUBA
from cuds.session.sim_wrapper_session import SimWrapperSession


class SomeSimulationSession(SimWrapperSession):
    """
    Session class for some engine.
    """

    def __init__(self, engine=None, **kwargs):
        # TODO: Instantiate or connect the engine
        super().__init__(engine, **kwargs)

    def __str__(self):
        # TODO: Define the output of str(SomeSimulationSession())
        return "Some Wrapper Session"

    # OVERRIDE
    def _run(self, root_cuds_object):
        """Call the run command of the engine."""
        # TODO: call the run method in the engine

    # OVERRIDE
    def _update_cuds_objects_after_run(self, root_cuds_object):
        """Updates the cuds after the engine has been executed. """
        # TODO: sync the cuds with the engine

    # OVERRIDE
    def _apply_added(self):
        """Adds the added cuds to the engine."""
        # TODO: What should happen in the engine when the user adds a certain cuds?
        # Use self._added.values()

    # OVERRIDE
    def _apply_updated(self):
        """Updates the updated cuds in the engine."""
        # TODO: What should happen in the engine when the user updates a certain cuds?
        # Use self._updated.values()

    # OVERRIDE
    def _apply_deleted(self):
        """Deletes the deleted cuds from the engine."""
        # TODO: What should happen in the engine when the user removes a certain cuds?
        # Use self._deleted.values()
