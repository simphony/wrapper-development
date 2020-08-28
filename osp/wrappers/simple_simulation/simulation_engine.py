# This file contains simple code to emulate communication with an engine.
# It acts like a dummy syntactic layer.

class Atom():

    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity


class SimulationEngine:
    """
    Simple engine sample code.
    """

    def __init__(self):
        self.atoms = list()
        print("Engine instantiated!")

    def __str__(self):
        return "Some Engine Connection"

    def run(self, timesteps=1):
        """Call the run command of the engine."""
        print("Now the engine is running")
        for atom in self.atoms:
            atom.position += atom.velocity * timesteps

    def add_atom(self, position, velocity):
        """Add an atom to the engine.

        Args:
            position (array): A 3D array for the position of the atom.
            velocity (array): A 3D array for the velocity of the atom.
        """
        print("Add atom %s with position %s and velocity %s"
              % (len(self.atoms), position, velocity))
        self.atoms.append(Atom(position, velocity))

    def update_position(self, idx, position):
        """Update the position of the atom

        Args:
            idx (int): The index of the atom to update
            position (array): The new position.
        """
        print("Update atom %s. Setting position to %s"
              % (idx, position))
        self.atoms[idx].position = position

    def update_velocity(self, idx, velocity):
        """Update the velocity of an atom.

        Args:
            idx (int): The index of the atom
            velocity (array): The new velocity.
        """
        print("Update atom %s. Setting velocity to %s"
              % (idx, velocity))
        self.atoms[idx].velocity = velocity

    def get_velocity(self, idx):
        """Get the velocity of an atom.

        Args:
            idx (int): The index of the atom.

        Returns:
            array: The velocity of the atom.
        """
        return self.atoms[idx].velocity

    def get_position(self, idx):
        """Get the position of the atom.

        Args:
            idx (int): The index of the atom.

        Returns:
            array: The position of the atom.
        """
        return self.atoms[idx].position
