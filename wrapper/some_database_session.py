# Copyright (c) 2014-2019, Adham Hashibon, Materials Informatics Team,
# Fraunhofer IWM.
# All rights reserved.
# Redistribution and use are limited to the scope agreed with the end user.
# No parts of this software may be used outside of this context.
# No redistribution is allowed without explicit written permission.

# TODO: Import the python connection to the DB

import cuds.classes
from cuds.classes import CUBA
from cuds.session.db.sql_wrapper_session import SqlWrapperSession


class SomeDatabaseSession(SqlWrapperSession):
    """
    Session class for some SQL DB.
    """