"""This code exemplifies how to use the wrapper."""

import numpy as np
from simphony_osp.namespaces import ontology_namespace
from simphony_osp.tools import pretty_print
from simphony_osp.tools.search import find
from simphony_osp.utils.datatypes import Vector
from simphony_osp.wrappers import SimulationWrapper

material = ontology_namespace.Material()
for i in range(3):
    atom = ontology_namespace.Atom()
    atom[ontology_namespace.hasPart] = {
        ontology_namespace.Position(value=[i, i, i], unit="m"),
        ontology_namespace.Velocity(value=np.random.random(3), unit="m/s"),
    }
    material[ontology_namespace.hasPart] += atom

# Run a simulation
with SimulationWrapper() as wrapper:
    wrapper.add(find(material))
    material = wrapper.get(material.identifier)
    pretty_print(material)

    wrapper.compute()
    pretty_print(material)

    for atom in material.get(
        rel=ontology_namespace.hasPart, oclass=ontology_namespace.Atom
    ):
        atom.get(oclass=ontology_namespace.Velocity).one().value = Vector(
            [0, 0, 0]
        )

    wrapper.compute()

    pretty_print(material)
