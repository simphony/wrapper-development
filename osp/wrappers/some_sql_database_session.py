# Copyright (c) 2014-2019, Adham Hashibon, Materials Informatics Team,
# Fraunhofer IWM.
# All rights reserved.
# Redistribution and use are limited to the scope agreed with the end user.
# No parts of this software may be used outside of this context.
# No redistribution is allowed without explicit written permission.

# TODO: Import the python connection to the DB

from osp.core.session import SqlWrapperSession


class SomeDatabaseSession(SqlWrapperSession):
    """
    Session class for some SQL DB.
    """

    def __init__(self, engine=None, **kwargs):
        # TODO instantiate or connect to the engine
        super().__init__(engine=engine, **kwargs)

    def __str__(self):
        # TODO define the output of str(SomeDatabaseSession)
        pass

    # OVERRIDE
    def close(self):
        # TODO close the connection to the database
        pass

    # OVERRIDE
    def _commit(self):
        # TODO commit the transaction
        pass

    # OVERRIDE
    def _init_transaction(self):
        # TODO initialise the transaction
        pass

    # OVERRIDE
    def _rollback_transaction(self):
        # TODO rollback the transaction
        pass

    # OVERRIDE
    def _db_select(self, table_name, columns, condition, datatypes):
        # TODO get data from the table by issuing a SELECT statement.
        pass

    # OVERRIDE
    def _db_create(self, table_name, columns, datatypes,
                   primary_key, foreign_key, index):
        # TODO create a table by issuing a CREATE TABLE statement.
        pass

    # OVERRIDE
    def _db_insert(self, table_name, columns, values, datatypes):
        # TODO insert data to the table by issuing an INSERT statement.
        pass

    # OVERRIDE
    def _db_update(self, table_name, columns, values, condition, datatypes):
        # TODO update data of the table by issuing an UPDATE statement.
        pass

    # OVERRIDE
    def _db_delete(self, table_name, condition):
        # TODO delete data from a table by issuing a DELETE statement.
        pass

    # OVERRIDE
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
