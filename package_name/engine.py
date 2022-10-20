"""This file emulates communication with a simulation engine."""

from functools import wraps
from dataclasses import dataclass
from typing import List, Optional

from numpy import ndarray


@dataclass
class Atom:
    """Class holding information about an atom."""

    position: ndarray
    velocity: ndarray


class AtomNotFoundException(KeyError):
    """Exception to be raised when a non-existent atom is requested.

    Exception raised by `SimulationEngine` when an index that is not associated
    with an atom in the engine is looked up.
    """
    def __init__(self, *args):
        default_msg = f"No atom with given index registered in the engine"
        if not args:
            args = (default_msg, )
        super().__init__(*args)


def raise_atom_not_found_exception(func):
    """A decorator to automatically raise AtomNotFoundException.

    Raises AtomNotFoundException when the first positional argument of the
    decorated method of `SimulationEngine` does not correspond to an atom that
    is registered in the engine.
    """
    @wraps(func)
    def decorated(self, index: int, *args, **kwargs):
        exception = AtomNotFoundException()
        try:
            atom = self._atoms[index]
        except IndexError as e:
            raise exception from e
        if atom is None:
            raise exception
        return func(self, index, *args, **kwargs)

    return decorated


class SimulationEngine:
    """Simple engine sample code.

    This simulation engine associates atoms with an integer index. Indexing
    starts at zero, and each time an atom is added, `last_index + 1` is
    associated with it. Indexes of deleted atoms are never reused for new
    atoms.
    """

    _atoms: List[Optional[Atom]]

    def __init__(self):
        """Initializes the simulation engine."""
        self._atoms = list()
        print("Engine instantiated!")

    def __str__(self) -> str:
        """String representation of the simulation engine."""
        return "Some Engine Connection"

    def run(self, time_steps: int = 1) -> None:
        """Calls the run command of the engine."""
        print("Now the engine is running")
        for atom in self._atoms:
            atom.position = atom.position + atom.velocity * time_steps

    def add_atom(self, position: ndarray, velocity: ndarray) -> None:
        """Adds an atom to the engine.

        Args:
            position: A 3D array for the position of the atom.
            velocity: A 3D array for the velocity of the atom.
        """
        print(
            "Add atom %s with position %s and velocity %s"
            % (len(self._atoms), position, velocity)
        )
        self._atoms.append(Atom(position, velocity))

    @raise_atom_not_found_exception
    def delete_atom(self, index: int) -> None:
        """Removes an atom from the engine.

        Args:
            index: The index of the atom to remove.

        Raises:
            AtomNotFoundException: No atom with given index registered in the
                engine.
        """
        exception = AtomNotFoundException()
        try:
            atom = self._atoms[index]
        except KeyError as e:
            raise exception from e
        if atom is None:
            raise exception

        self._atoms[index] = None

    @raise_atom_not_found_exception
    def update_position(self, index: int, position: ndarray) -> None:
        """Update the position of the atom.

        Args:
            index: The index of the atom to update
            position: The new position.

        Raises:
            AtomNotFoundException: No atom with given index registered in the
                engine.
        """
        print("Update atom %s. Setting position to %s" % (index, position))
        self._atoms[index].position = position

    @raise_atom_not_found_exception
    def update_velocity(self, index: int, velocity: ndarray) -> None:
        """Update the velocity of an atom.

        Args:
            index: The index of the atom
            velocity: The new velocity.

        Raises:
            AtomNotFoundException: No atom with given index registered in the
                engine.
        """
        print("Update atom %s. Setting velocity to %s" % (index, velocity))
        self._atoms[index].velocity = velocity

    @raise_atom_not_found_exception
    def get_velocity(self, index: int) -> ndarray:
        """Get the velocity of an atom.

        Args:
            index: The index of the atom.

        Returns:
            The velocity of the atom.

        Raises:
            AtomNotFoundException: No atom with given index registered in the
                engine.
        """
        return self._atoms[index].velocity

    @raise_atom_not_found_exception
    def get_position(self, index) -> ndarray:
        """Get the position of the atom.

        Args:
            index: The index of the atom.

        Returns:
            The position of the atom.

        Raises:
            AtomNotFoundException: No atom with given index registered in the
                engine.
        """
        return self._atoms[index].position
