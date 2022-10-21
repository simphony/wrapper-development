"""Tests the intended usage of your wrapper.

Modify this file to adapt it to your own wrapper. You can organize your tests
in any way you wish (e.g. distribute them among different files) and use any
testing framework, but do not omit this kind of testing in your package.

This example assumes that the typical usage is to pass a single atom to the
wrapper from an existing turtle file, compute its position after ten seconds,
and then export the results to a file again.

These tests must be written accessing only functionality that a user of
SimPhoNy could make use of themselves (e.g. no access to private attributes or
methods of the wrapper class). Such in-depth tests are covered in the files
"test_unit.py" and "test_integration.py".
"""

import unittest
from io import StringIO

from simphony_osp.tools.pico import install, packages

# install the required ontology for the test if not installed
if "ontology" not in packages():
    install("../package_name/ontology.yml")


class TestUsage(unittest.TestCase):
    """Tests the typical usage of the wrapper.

    Collects the typical use cases of the wrapper and tests them.
    """

    def test_usage_simulation(self):
        """Tests running a simple simulation with data from an RDF file.

        Imports an RDF file with a single atom and runs the simulation, then
        exports the results back to an RDF file again.
        """
        # prepare environment for typical usage
        import uuid

        from rdflib import RDF
        from simphony_osp.namespaces import ontology_namespace as namespace
        from simphony_osp.utils.datatypes import Vector

        atom_uuid = uuid.uuid4()
        position_uuid = uuid.uuid4()
        position_as_string = Vector([1, 5, 15]).to_b85()
        velocity_uuid = uuid.uuid4()
        velocity_as_string = Vector([3, 7, 4]).to_b85()

        input_file = f"""
        # Atom
        <http://example.org/entities#{atom_uuid}>
          <{RDF.type}> <{namespace.Atom.identifier}> ;
          <{namespace.hasPart.identifier}>
          <http://example.org/entities#{position_uuid}> ;
          <{namespace.hasPart.identifier}>
          <http://example.org/entities#{velocity_uuid}> .

        # Position
        <http://example.org/entities#{position_uuid}>
          <{RDF.type}> <{namespace.Position.identifier}> ;
          <{namespace.value.identifier}>
          "{position_as_string}"^^<{Vector.iri}> .

        # Velocity
        <http://example.org/entities#{velocity_uuid}>
          <{RDF.type}> <{namespace.Velocity.identifier}> ;
          <{namespace.value.identifier}>
          "{velocity_as_string}"^^<{Vector.iri}> .
        """

        input_file = StringIO(input_file)
        output_file = StringIO()

        # execute typical usage
        from simphony_osp.namespaces import ontology_namespace as namespace
        from simphony_osp.tools import export_file, import_file
        from simphony_osp.wrappers import SimulationWrapper

        with SimulationWrapper() as wrapper:
            import_file(file=input_file, format="ttl")
            wrapper.compute()
            export_file(file=output_file, format="ttl")

        # verify results
        from simphony_osp.session import Session

        output_file.seek(0)

        with Session() as session:
            import_file(output_file, format="ttl")
            position = session.get(oclass=namespace.Position).one()
            self.assertEqual(position.value, [4, 12, 19])


if __name__ == "__main__":
    unittest.main()
