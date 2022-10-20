"""Tests all the wrapper API methods defined on your wrapper.

Modify this file to adapt it to your own wrapper. You can organize your tests
in any way you wish (e.g. distribute them among different files) and use any
testing framework, but do not omit this kind of testing in your package.

These tests must be written accessing only functionality that a user of
SimPhoNy could make use of themselves (e.g. no access to private attributes or
methods of the wrapper class). Such in-depth tests are covered in the files
"test_unit.py" and "test_integration.py".
"""

import unittest

from simphony_osp.namespaces import owl
from simphony_osp.session import Session
from simphony_osp.utils.datatypes import Vector
from simphony_osp.wrappers import SimulationWrapper

# install the required ontology for the test if not installed
try:
    from simphony_osp.namespaces import ontology_namespace as namespace
except ImportError:
    from simphony_osp.tools.pico import install
    install('../package_name/ontology.yml')
    from simphony_osp.namespaces import ontology_namespace as namespace


class TestWrapperAPI(unittest.TestCase):
    """Tests all the wrapper API method defined on your wrapper.

    The methods are tested indirectly. Normal usage is simulated so that
    wrapper methods are called.
    """

    def test_open(self) -> None:
        """Tests the `open` method, invoked opening a new session.

        Of course, the code below also invokes `populate` and `close`, but this
        test should be focusing on testing the behavior of `open`: for example
        passing different configuration strings together with different
        combinations of the "create" argument if it was applicable.
        """
        # enough to cover all use cases
        with SimulationWrapper():
            pass

    def test_populate(self) -> None:
        """Tests the `populate` method, invoked opening a new session."""
        # enough to cover all use cases, since for this wrapper populate does
        # nothing
        with SimulationWrapper():
            pass

    def test_close(self):
        """Tests the `close` method."""
        session = SimulationWrapper()
        session.close()

    def test_commit(self) -> None:
        """Tests the `commit` method.

        For this example wrapper, there is just one aspect to test:
        - When incoherent data is provided, an `AssertionError` is raised,
          whereas when coherent data is provided, no exception is raised.

        For that, one may trigger failures of the consistency check. The
        consistency check in the wrapper verifies constraints for each ontology
        class separately. Therefore, this test follows the following logical
        structure:
        - prepare a situation (or several) which are consistent
        - for each relevant type of ontology class:
          - for each kind of possible inconsistency:
            - start with the situation that is considered correct
            - introduce a single inconsistency/change and verify that it makes
              the consistency check raise assertion errors (or not raise them
              if you introduced a valid change)
            - if desired, return to a consistent state and repeat with a new
              inconsistency of the same type
        """

        def consistent() -> Session:
            """Create a consistent situation in a new session."""
            session = SimulationWrapper()
            session.locked = True
            with session:
                atm = namespace.Atom()
                pos = namespace.Position(value=[8, 5, 3], unit="m")
                vel = namespace.Velocity(value=[1, 2, 3], unit="m/s")
                atm[namespace.hasPart] = pos, vel
            session.locked = False
            return session

        def consistent_two_atoms() -> Session:
            """Create a consistent situation (two atoms) in a new session.

            This function reuses the code from the previous function
            `consistent`.
            """
            session = consistent()
            session.locked = True
            with session:
                atm2 = namespace.Atom()
                pos2 = namespace.Position(value=[1, 5.3, 7.1], unit="m")
                vel2 = namespace.Velocity(value=[4, 2.1, 5], unit="m/s")
                atm2[namespace.hasPart] = pos2, vel2
            session.locked = False
            return session

        with consistent() as wrapper:
            # verify that the situation assumed to be consistent is indeed
            # consistent
            wrapper.commit()

        with consistent_two_atoms() as wrapper:
            # verify that the situation assumed to be consistent is indeed
            # consistent
            wrapper.commit()

        # --------- Atoms --------- #
        with consistent() as wrapper:
            # delete the position
            position = wrapper.get(oclass=namespace.Position).one()
            wrapper.delete(position)
            self.assertRaises(AssertionError, wrapper.commit)

        with consistent() as wrapper:
            # delete the velocity
            velocity = wrapper.get(oclass=namespace.Velocity).one()
            wrapper.delete(velocity)
            self.assertRaises(AssertionError, wrapper.commit)

        with consistent() as wrapper:
            # detach the position
            atom = wrapper.get(oclass=namespace.Atom).one()
            position = wrapper.get(oclass=namespace.Position).one()
            atom[owl.topObjectProperty] -= position
            self.assertRaises(AssertionError, wrapper.commit)
            # reattach it
            atom[namespace.hasPart] += position
            wrapper.commit()

            # detach and reattach with wrong relationship
            atom[namespace.hasPart] -= position
            atom[owl.topObjectProperty] += position
            self.assertRaises(AssertionError, wrapper.commit)
            # fix the relationship
            atom[namespace.hasPart] += position
            wrapper.commit()

        with consistent() as wrapper:
            # detach the velocity
            atom = wrapper.get(oclass=namespace.Atom).one()
            velocity = wrapper.get(oclass=namespace.Velocity).one()
            atom[owl.topObjectProperty] -= velocity
            self.assertRaises(AssertionError, wrapper.commit)
            # reattach it
            atom[namespace.hasPart] += velocity
            wrapper.commit()

            # detach and reattach with wrong relationship
            atom[namespace.hasPart] -= velocity
            atom[owl.topObjectProperty] += velocity
            self.assertRaises(AssertionError, wrapper.commit)
            # fix the relationship
            atom[namespace.hasPart] += velocity
            wrapper.commit()

        with consistent() as wrapper:
            # position and velocity values of an atom
            velocity = wrapper.get(oclass=namespace.Velocity).one()
            position = wrapper.get(oclass=namespace.Position).one()

            for individual in (velocity, position):
                # remove value
                value = individual["value"].one()
                del individual["value"]
                self.assertRaises(AssertionError, wrapper.commit)
                # restore original value
                individual["value"] = value
                wrapper.commit()

                # set an array of strings as value
                individual["value"] = Vector(["a", "b", "c"])
                self.assertRaises(AssertionError, wrapper.commit)
                # restore original value
                individual["value"] = value
                wrapper.commit()

                # set an array of floats as value
                individual["value"] = Vector([1.3, 4.8, 9.2])
                wrapper.commit()
                # restore original value
                individual["value"] = value
                wrapper.commit()

                # use a 4D array of integers
                individual["value"] = Vector([9, 18, 43, 7])
                self.assertRaises(AssertionError, wrapper.commit)
                # restore original value
                individual["value"] = value
                wrapper.commit()

        # --------- Velocities and positions --------- #
        for class_ in (namespace.Position, namespace.Velocity):
            with consistent() as wrapper:
                # add a velocity/position that is not attached to an atom
                class_(
                    value=[8, 5, 3],
                    unit="m" if class_ == namespace.Position else "m/s"
                )
                self.assertRaises(AssertionError, wrapper.commit)

            with consistent_two_atoms() as wrapper:
                # attach one of the existing velocity/position to the two atoms
                individual = wrapper.get(oclass=class_).any()
                atoms = wrapper.get(oclass=namespace.Atom)
                for atom in atoms:
                    atom["hasPart"] += individual
                self.assertRaises(AssertionError, wrapper.commit)

    def test_compute(self) -> None:
        """Tests the `compute` method."""
        with SimulationWrapper() as wrapper:
            atom = namespace.Atom()
            position = namespace.Position(value=[1, 1, 1], unit="m")
            velocity = namespace.Velocity(value=[1, 2, 3], unit="m/s")
            atom[namespace.hasPart] = position, velocity

            self.assertEqual(position.value, [1, 1, 1])
            wrapper.compute()  # default number of time steps should be one
            self.assertEqual(position.value, [2, 3, 4])
            wrapper.compute(time_steps=2)
            self.assertEqual(position.value, [4, 7, 10])


if __name__ == "__main__":
    unittest.main()
