# TODO: Import the Python connection to the triplestore
from osp.core.session.db.triplestore_wrapper_session \
    import TripleStoreWrapperSession
from osp.core.session.sparql_backend import SparqlResult, SparqlBindingSet


class SomeTriplestoreSession(TripleStoreWrapperSession):
    """
    Session class for some database.
    """

    def __init__(self, engine=None):
        # TODO instantiate or connect to the engine
        super().__init__(engine=engine)

    def __str__(self):
        # TODO define the output of str(SomeDatabaseSession)
        pass

    def close(self):
        # TODO close the connection to the database
        pass

    def _commit(self):
        # TODO commit the transaction
        pass

    def _init_transaction(self):
        # TODO initialise the transaction
        pass

    def _rollback_transaction(self):
        # TODO rollback the transaction
        pass

    def _initialize(self):
        # TODO load by cuba key
        pass

    def _add(self, *triples):
        # TODO add the given triples to the triplestore
        pass

    def _remove(self, pattern):
        # TODO remove all triples that match the given pattern
        pass

    def _triples(self, pattern):
        # TODO yield all triples that match the given pattern
        pass

    def _sparql(self, query_string):
        # TODO execute the given SPARQL query
        pass

    @staticmethod
    def _o_to_rdflib(o):
        # TODO: transform an object (Literal or IRI) from the engine format to
        #  an rdflib node.
        pass

    class SomeTriplestoreSparqlResult(SparqlResult):
        """The result of a SPARQL query on the triplestore."""

        def __init__(self, tuple_query_result, session):
            """Initialize the result."""
            self.result = tuple_query_result
            super().__init__(session)

        def close(self):
            """Close the connection."""
            self.result.close()

        def __iter__(self):
            """Iterate the result."""
            for binding_set in self.result:
                yield SomeTriplestoreSession\
                    .SomeTriplestoreSessionSparqlBindingSet(binding_set,
                                                            self.session)

        def __len__(self):
            """Compute the number of elements in the result."""
            return len(self.result)

    class SomeTriplestoreSessionSparqlBindingSet(SparqlBindingSet):
        """A row in the result. Mapping from variable to value."""

        def __init__(self, engine_binding_set, session):
            """Initialize the row."""
            self.binding_set = engine_binding_set
            super().__init__(session)

        def _get(self, variable_name):
            o = self.binding_set.getValue(variable_name)
            return SomeTriplestoreSession._o_to_rdflib(o)

