from osp.core.session import SimWrapperSession
from osp.wrappers.simple_simulation import SimulationEngine
from osp.core.namespaces import simple_ontology 


class SimpleSimulationSession(SimWrapperSession):
    """Session class for some engine."""

    def __init__(self, engine=None, **kwargs):
        super().__init__(engine or SimulationEngine(), **kwargs)
        self.mapper = dict()  # maps uid to index in the backend

    def __str__(self):
        return "Simple sample Wrapper Session"

    def _apply_added(self, root_obj, buffer):
        """Adds the added cuds to the engine."""
        for obj in buffer.values():
            if obj.is_a(simple_ontology.Atom):
                self.mapper[obj.uid] = len(self.mapper)
                pos = obj.get(oclass=simple_ontology.Position)[0].value
                vel = obj.get(oclass=simple_ontology.Velocity)[0].value
                self._engine.add_atom(pos, vel)

    def _apply_updated(self, root_obj, buffer):
        """Updates the updated cuds in the engine."""
        for obj in buffer.values():

            # case 1: we change the velocity
            if obj.is_a(simple_ontology.Velocity):
                atom = obj.get(rel=simple_ontology.isPartOf)[0]
                idx = self.mapper[atom.uid]
                self._engine.update_velocity(idx, obj.value)

            # case 2: we change the position
            elif obj.is_a(simple_ontology.Position):
                atom = obj.get(rel=simple_ontology.isPartOf)[0]
                idx = self.mapper[atom.uid]
                self._engine.update_position(idx, obj.value)

    def _apply_deleted(self, root_obj, buffer):
        """Deletes the deleted cuds from the engine."""

    def _load_from_backend(self, uids, expired=None):
        """Loads the cuds object from the simulation engine"""
        for uid in uids:
            if uid in self._registry:
                obj = self._registry.get(uid)

                # check whether user wants to load a position
                if obj.is_a(simple_ontology.Position):
                    atom = obj.get(rel=simple_ontology.isPartOf)[0]
                    idx = self.mapper[atom.uid]
                    pos = self._engine.get_position(idx)
                    obj.value = pos

                # check whether user wants to load a velocity
                elif obj.is_a(simple_ontology.Velocity):
                    atom = obj.get(rel=simple_ontology.isPartOf)[0]
                    idx = self.mapper[atom.uid]
                    vel = self._engine.get_velocity(idx)
                    obj.value = vel

                yield obj

    def _run(self, root_cuds_object):
        """Call the run command of the engine."""
        self._engine.run()
