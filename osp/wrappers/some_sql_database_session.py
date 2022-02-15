# TODO: Import the python connection to the DB

from osp.core.session import SqlWrapperSession


class SomeDatabaseSession(SqlWrapperSession):
    """
    Session class for some SQL DB.
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

    def _db_select(self, query):
        """Get data from the table of the given names.

        Args:
            query (SqlQuery): A object describing the SQL query.
        """
        # TODO get data from the table by issuing a SELECT statement.
        pass

    # OVERRIDE
    def _db_create(self, table_name, columns, datatypes,
                   primary_key, generate_pk, foreign_key, indexes):
        # TODO create a table by issuing a CREATE TABLE statement.
        pass

    def _db_insert(self, table_name, columns, values, datatypes):
        # TODO insert data to the table by issuing an INSERT statement.
        pass

    def _db_update(self, table_name, columns, values, condition, datatypes):
        # TODO update data of the table by issuing an UPDATE statement.
        pass

    def _db_delete(self, table_name):
        # TODO delete data from a table by issuing a DELETE statement.
        pass

    def _db_drop(self, table_name):
        # TODO drop an entire table.
        pass

    def _get_table_names(self, prefix):
        # TODO get all the table names with the given prefix.
        pass

    def _convert_condition(self, condition):
        # OPTIONAL TODO convert osp-core condition to conditions
        # usable for your database.
        pass

    def _to_sqlite_datatype(self, cuds_datatype):
        # OPTIONAL TODO convert osp-core datatype tp a datatype
        # usable for your database.
        pass
