"""Tests all internal methods independently.

This module is meant to contain unit tests for all the internal functions and
methods used by your wrapper.

Modify this file to adapt it to your own wrapper. You can organize your tests
in any way you wish (e.g. distribute them among different files) and use any
testing framework, and you can omit this kind of testing in your package,
although it is recommended not to do so.
"""

import unittest
from typing import List

from numpy import array
from package_name.engine import Atom, SimulationEngine, AtomNotFoundException

# install the required ontology for the test if not installed
try:
    from simphony_osp.namespaces import ontology_namespace as namespace
except ImportError:
    from simphony_osp.tools.pico import install
    install('../package_name/ontology.yml')
    from simphony_osp.namespaces import ontology_namespace as namespace


class TestWrapperModuleSimulationWrapper(unittest.TestCase):
    """Tests methods of the `package_name.wrapper.SimulationWrapper` class.

    The tests for wrapper API methods are omitted, as they have been already
    thoroughly tested in `test_wrapper_api.py`.
    """

    @unittest.skip
    def test__consistency_check(self):
        """Tests the `_consistency_check` method.

        This test is only a placeholder and actually skipped because this
        method is sufficiently covered indirectly by
        `tests.test_wrapper_api.TestWrapperAPI.test_commit`.
        """
        pass


class TestEngineModuleAtom(unittest.TestCase):
    """Tests methods of the `package_name.engine.Atom` class.

    Note hat there is not much to test for this class because it is a simple
    dataclass, and for the most part can be trusted to work as documented in
    the Python standard library.
    """

    def test_Atom___init__(self):
        """Tests the `__init__` method.

        As this class is a Python dataclass, we trust dataclasses to have been
        sufficiently tested by the Python developers. Only the ordering of the
        attributes of the dataclass is tested.
        """
        position = array([5, 9, 14])
        velocity = array([3, 4, 6])

        # normal instantiation
        atom = Atom(position, velocity)
        self.assertTrue((position == atom.position).all())
        self.assertTrue((velocity == atom.velocity).all())

        # instantiation using keyword arguments
        atom = Atom(velocity=velocity, position=position)
        self.assertTrue((position == atom.position).all())
        self.assertTrue((velocity == atom.velocity).all())


class TestEngineModuleSimulationEngine(unittest.TestCase):
    """Tests methods of the `package_name.engine.SimulationEngine` class.

    Remember that the simulation engine associates atoms with an integer index.
    Indexing starts at zero, and each time an atom is added, `last_index + 1`
    is associated with it. Indexes of deleted atoms are never reused for new
    atoms.
    """

    engine: SimulationEngine

    def setUp(self) -> None:
        """Instantiates a new simulation engine for each test."""
        self.engine = SimulationEngine()

    def test___init__(self):
        """Tests the instantiation of new simulation engines."""
        # nothing to do here, `setUpClass` already instantiates a new engine
        # before running this test
        pass

    def test_run(self):
        """Tests the `run` method."""
        atoms = [
            {"position": array([5, 9, 14]),
             "velocity": array([3, 4, 6])},
            {"position": array([4, 15, 13]),
             "velocity": array([18, -1, 2])},
        ]

        for attributes in atoms:
            self.engine.add_atom(**attributes)

        def validate_atoms(expected_positions: List[List[int]]):
            """Validates the atoms after a simulation.

            As the velocities of the atoms do not change, only the expected
            positions are required as arguments.
            """
            for i, position in enumerate(expected_positions):
                self.assertTrue(
                    (position == self.engine.get_position(i)).all()
                )
                self.assertTrue(
                    (atoms[i]["velocity"] == self.engine.get_velocity(i)).all()
                )

        self.engine.run()
        validate_atoms([
            [8, 13, 20],
            [22, 14, 15]
        ])

        self.engine.run(time_steps=3)
        validate_atoms([
            [17, 25, 38],
            [76, 11, 21]
        ])

        self.engine.run(time_steps=0)
        validate_atoms([
            [17, 25, 38],
            [76, 11, 21]
        ])

        self.engine.run(time_steps=-1)
        validate_atoms([
            [14, 21, 32],
            [58, 12, 19]
        ])

    def test_add_atom(self):
        """Tests the `add_atom` method."""
        atom = {"position": [5, 9, 14],
                "velocity": [3, 4, 6]}
        self.engine.add_atom(**atom)

        self.assertEqual(self.engine.get_position(0), atom["position"])
        self.assertEqual(self.engine.get_velocity(0), atom["velocity"])

    def test_delete_atom(self):
        """Tests the `delete_atom` method."""
        atom1 = {"position": array([5, 9, 14]),
                 "velocity": array([3, 4, 6])}
        self.engine.add_atom(**atom1)
        atom2 = {"position": array([0, 1, -5]),
                 "velocity": array([2, 0, 4])}
        self.engine.add_atom(**atom2)

        self.engine.delete_atom(0)

        self.assertRaises(AtomNotFoundException, self.engine.get_position, 0)
        self.assertTrue(
            (atom2["position"] == self.engine.get_position(1)).all()
        )
        self.assertRaises(AtomNotFoundException, self.engine.delete_atom, 0)
        self.assertRaises(AtomNotFoundException, self.engine.delete_atom, 2)

    def test_update_position(self):
        """Tests the `update_position` method."""
        atom1 = {"position": array([5, 9, 14]),
                 "velocity": array([3, 4, 6])}
        self.engine.add_atom(**atom1)
        atom2 = {"position": array([0, 1, -5]),
                 "velocity": array([2, 0, 4])}
        self.engine.add_atom(**atom2)

        self.engine.update_position(0, array([1, 2, 3]))

        self.assertTrue(
            (self.engine.get_position(0) == array([1, 2, 3])).all()
        )
        self.assertTrue(
            (atom2["position"] == self.engine.get_position(1)).all()
        )
        self.assertRaises(
            AtomNotFoundException,
            self.engine.update_position,
            2,
            array([1, 2, 3])
        )

    def test_update_velocity(self):
        """Tests the `update_velocity` method."""
        atom1 = {"position": array([5, 9, 14]),
                 "velocity": array([3, 4, 6])}
        self.engine.add_atom(**atom1)
        atom2 = {"position": array([0, 1, -5]),
                 "velocity": array([2, 0, 4])}
        self.engine.add_atom(**atom2)

        self.engine.update_velocity(0, array([1, 2, 3]))

        self.assertTrue(
            (array([1, 2, 3]) == self.engine.get_velocity(0)).all())
        self.assertTrue(
            (atom2["velocity"] == self.engine.get_velocity(1)).all()
        )
        self.assertRaises(
            AtomNotFoundException,
            self.engine.update_velocity,
            2,
            array([1, 2, 3])
        )

    def test_get_position(self):
        """Tests the `get_position` method."""
        atom1 = {"position": array([5, 9, 14]),
                 "velocity": array([3, 4, 6])}
        self.engine.add_atom(**atom1)
        atom2 = {"position": array([0, 1, -5]),
                 "velocity": array([2, 0, 4])}
        self.engine.add_atom(**atom2)

        self.assertTrue(
            (atom1["position"] == self.engine.get_position(0)).all()
        )
        self.assertTrue(
            (atom2["position"] == self.engine.get_position(1)).all()
        )
        self.assertRaises(AtomNotFoundException, self.engine.get_position, 2)

    def test_get_velocity(self):
        """Tests the `get_velocity` method."""
        atom1 = {"position": array([5, 9, 14]),
                 "velocity": array([3, 4, 6])}
        self.engine.add_atom(**atom1)
        atom2 = {"position": array([0, 1, -5]),
                 "velocity": array([2, 0, 4])}
        self.engine.add_atom(**atom2)

        self.assertTrue(
            (atom1["velocity"] == self.engine.get_velocity(0)).all()
        )
        self.assertTrue(
            (atom2["velocity"] == self.engine.get_velocity(1)).all()
        )
        self.assertRaises(AtomNotFoundException, self.engine.get_velocity, 2)
