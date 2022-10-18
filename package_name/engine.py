"""This file emulates communication with a simulation engine."""

from dataclasses import dataclass
from typing import List, Optional

from numpy import ndarray


@dataclass
class Atom:
    """Class holding information about an atom."""

    position: ndarray
    velocity: ndarray


class SimulationEngine:
    """Simple engine sample code."""

    atoms: List[Optional[Atom]]

    def __init__(self):
        """Initialize the simulation engine."""
        self.atoms = list()
        print("Engine instantiated!")

    def __str__(self) -> str:
        """String representation of the simulation engine."""
        return "Some Engine Connection"

    def run(self, time_steps: int = 1) -> None:
        """Call the run command of the engine."""
        print("Now the engine is running")
        for atom in self.atoms:
            atom.position = atom.position + atom.velocity * time_steps

    def add_atom(self, position: ndarray, velocity: ndarray) -> None:
        """Add an atom to the engine.

        Args:
            position: A 3D array for the position of the atom.
            velocity: A 3D array for the velocity of the atom.
        """
        print(
            "Add atom %s with position %s and velocity %s"
            % (len(self.atoms), position, velocity)
        )
        self.atoms.append(Atom(position, velocity))

    def delete_atom(self, index: int) -> None:
        """Remove an atom from the engine.

        Args:
            index: The index of the atom to remove.
        """
        self.atoms[index] = None

    def update_position(self, index: int, position: ndarray) -> None:
        """Update the position of the atom.

        Args:
            index: The index of the atom to update
            position: The new position.
        """
        print("Update atom %s. Setting position to %s" % (index, position))
        self.atoms[index].position = position

    def update_velocity(self, index: int, velocity: ndarray) -> None:
        """Update the velocity of an atom.

        Args:
            index: The index of the atom
            velocity: The new velocity.
        """
        print("Update atom %s. Setting velocity to %s" % (index, velocity))
        self.atoms[index].velocity = velocity

    def get_velocity(self, index: int) -> ndarray:
        """Get the velocity of an atom.

        Args:
            index: The index of the atom.

        Returns:
            The velocity of the atom.
        """
        return self.atoms[index].velocity

    def get_position(self, index) -> ndarray:
        """Get the position of the atom.

        Args:
            index: The index of the atom.

        Returns:
            The position of the atom.
        """
        return self.atoms[index].position
