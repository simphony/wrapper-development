"""Your SimPhoNy wrapper is implemented in this file."""

from typing import Optional

from package_name.engine import SimulationEngine
from simphony_osp.development import Wrapper
from simphony_osp.namespaces import ontology_namespace
from simphony_osp.utils.datatypes import Vector


class SimulationWrapper(Wrapper):
    """Wrapper implementation for some simulation engine.

    Note: This implementation only makes use of the mandatory wrapper methods,
    as well as the `compute` method. Visit the SimPhoNy documentation
    https://simphony.readthedocs.io/en/v4.0.0rc4/developers/wrappers.html
    to learn more about the additional possibilities and the meaning of each
    method.
    """

    _engine = Optional[SimulationEngine]
    _mapper: dict
    _mapped_atoms: int = 0

    # Interface
    # ↓ ----- ↓

    def open(
        self,
        configuration: str,
        create: bool = False,
    ) -> None:
        """Create an instance of the simulation engine.

        The arguments "configuration" and "create" are ignored, since this
        wrapper does not require any configuration nor reads any special
        resource.

        Args:
            configuration: No effect.
            create: No effect.
        """
        self._mapper = dict()
        self._mapped_atoms = 0
        # underlying assumption: the engine never reuses atom indices
        self._engine = SimulationEngine()

    def close(self) -> None:
        """Destroy the current instance of the simulation engine."""
        self._engine = None  # garbage-collects the engine

    def populate(self) -> None:
        """Populate the base session so that it represents the data source.

        This simulation engine cannot save its state to a file, nothing to do
        here.
        """
        pass

    def commit(self) -> None:
        """This method commits the changes made by the user.

        Raises:
            AssertionError: When the data provided by the user would produce
                an inconsistent or unpredictable state of the data structures.
        """
        # Perform a consistency check if the user changed something. Raises
        # an `AssertionError` if the consistency check fails. This prevents
        # to some extent the case in which the changes are only partially
        # committed.
        if self.added | self.updated | self.deleted:
            self._consistency_check()

        # Examine the differences between the graphs below and make a plan to
        # modify your data structures.
        for individual in self.added:
            if individual.is_a(ontology_namespace.Atom):
                self._mapper[individual.identifier] = self._mapped_atoms
                self._mapped_atoms += 1
                position = (
                    individual.get(oclass=ontology_namespace.Position)
                    .one()
                    .value.data
                )
                velocity = (
                    individual.get(oclass=ontology_namespace.Velocity)
                    .one()
                    .value.data
                )
                self._engine.add_atom(position, velocity)

        for individual in self.updated:
            if individual.is_a(ontology_namespace.Velocity) or individual.is_a(
                ontology_namespace.Position
            ):
                atom = individual.get(
                    rel=ontology_namespace.hasPart,
                    oclass=ontology_namespace.Atom,
                ).inverse.one()
                index = self._mapper[atom.identifier]
                value = individual.value.data
                if individual.is_a(ontology_namespace.Position):
                    self._engine.update_position(index, value)
                else:  # individual.is_a(ontology_namespace.Velocity):
                    self._engine.update_velocity(index, value)

        for individual in self.deleted:
            if individual.is_a(ontology_namespace.Atom):
                index = self._mapper[individual.identifier]
                self._engine.delete_atom(index)
                del self._mapper[individual.identifier]

        # Change your data structures below. As you change the data
        # structures, `old_graph` and `new_graph` will change, so do not
        # rely on them. Relying on them would be analogous to changing a
        # dictionary while looping over it.
        pass

    def compute(self, time_steps: int = 1) -> None:
        """Run the simulation.

        Args:
            time_steps: Number of time steps to run the simulation for.
        """
        self._engine.run(time_steps=time_steps)

        # Reflect the changes back on the base graph.
        for individual in set(
            self.session.get(oclass=ontology_namespace.Position)
        ) | set(self.session.get(oclass=ontology_namespace.Velocity)):
            atom = individual.get(
                rel=ontology_namespace.hasPart, oclass=ontology_namespace.Atom
            ).inverse.one()
            index = self._mapper[atom.identifier]
            if individual.is_a(ontology_namespace.Position):
                individual.value = Vector(self._engine.get_position(index))
            else:  # individual.is_a(ontology_namespace.Velocity):
                individual.value = Vector(self._engine.get_velocity(index))

    # Interface
    # ↑ ----- ↑

    def _consistency_check(self) -> None:
        """Consistency check.

        Before updating the data structures, check that the changes
        provided by the user can leave them in a consistent state.

        This recommended because SimPhoNy cannot revert the changes you
        make to your data structures.

        Raises:
            AssertionError: When the data provided by the user would leave
                your engine in an inconsistent or unpredictable state.
        """
        try:
            # Verify atoms
            # - all atoms have exactly one velocity and force which must be
            #   vectors of either floats or integers
            for atom in self.session.get(oclass=ontology_namespace.Atom):
                position = atom.get(oclass=ontology_namespace.Position).one()
                velocity = atom.get(oclass=ontology_namespace.Velocity).one()
                for entity in (position, velocity):
                    array = entity.value.data
                    assert array.dtype in ("int64", "float64")
                    assert array.shape == (3,)

            # Verify velocities
            #  - all velocities are attached to exactly one atom
            for velocity in self.session.get(
                oclass=ontology_namespace.Velocity
            ):
                assert (
                    len(
                        velocity.get(
                            rel=ontology_namespace.hasPart,
                            oclass=ontology_namespace.Atom,
                        ).inverse
                    )
                    == 1
                )

            # Verify positions
            #  - all positions are attached to exactly one atom
            for position in self.session.get(
                oclass=ontology_namespace.Position
            ):
                assert (
                    len(
                        position.get(
                            rel=ontology_namespace.hasPart,
                            oclass=ontology_namespace.Atom,
                        ).inverse
                    )
                    == 1
                )
        except Exception as e:
            raise AssertionError(
                "Your changes leave the engine in an inconsistent or "
                "unpredictable state, cannot commit. Scroll up to find out "
                "the detailed cause of the exception."
            ) from e
