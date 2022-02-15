"""This code runs on the wrapper under `../osp/wrappers/simple_simulation`"""

import numpy as np

from osp.core.namespaces import simple_ontology
from osp.core.utils import pretty_print
from osp.wrappers.simple_simulation import SimpleSimulationSession

m = simple_ontology.Material()
for i in range(3):
    a = m.add(simple_ontology.Atom())
    a.add(
        simple_ontology.Position(value=[i, i, i], unit="m"),
        simple_ontology.Velocity(value=np.random.random(3), unit="m/s")
    )

# Run a simulation
with SimpleSimulationSession() as session:
    w = simple_ontology.Wrapper(session=session)
    m = w.add(m)
    w.session.run()

    pretty_print(m)

    for atom in m.get(rel=simple_ontology.hasPart):
        atom.get(oclass=simple_ontology.Velocity)[0].value = [0, 0, 0]
    w.session.run()

    pretty_print(m)
