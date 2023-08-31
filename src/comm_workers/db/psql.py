from contextlib import closing
from typing import Any, Iterable, cast
from uuid import UUID

from core.config import settings
from core.loggers import LOGGER
from psycopg2 import connect as pg_connect
from psycopg2.extensions import connection as pg_connection
from psycopg2.extras import DictCursor, DictRow

from .abstract import DBTemplateABC
from .base import ConnectionManager, Connector


class PostgresConnector(Connector):
    def __init__(self, dsl: dict | None = None):
        super().__init__()
        if not dsl:
            self.dsl = {
                "dbname": settings.psql_db_name,
                "user": settings.psql_user,
                "password": settings.psql_password,
                "host": settings.psql_host,
                "port": settings.psql_port,
            }
        else:
            self.dsl = dsl

    def _ping(self):
        self.connection: pg_connection
        cursor = self.connection.cursor()
        cursor.execute("SELECT 1;")
        cursor.close()

    def _connect(self) -> pg_connection:
        return pg_connect(**self.dsl, cursor_factory=DictCursor)


class PostgresConnectionManager(ConnectionManager):
    def __init__(self, connector: PostgresConnector):
        self.cursor_name_prefix = 1
        super().__init__(connector)

    def get_connection(self) -> pg_connection:
        return cast(pg_connection, super().get_connection())

    def cursor(self, itersize: int = 10000) -> DictCursor:
        # prevent cursor name from bloating
        if self.cursor_name_prefix > 10000000:
            self.cursor_name_prefix = 1

        if itersize < 1:
            return self.back_connection()(self.get_connection().cursor)()

        # create server side cursor to limit memory use
        cursor = self.back_connection()(self.get_connection().cursor)(
            name=f"cursor_{self.cursor_name_prefix}"
        )

        self.cursor_name_prefix += 1

        LOGGER.debug(f"Created cursor {self.cursor_name_prefix}")
        cursor.itersize = itersize
        return cursor

    def _execute(
        self, cursor: DictCursor, sql: str, sql_vars: Any = None
    ) -> DictCursor:
        if not sql_vars:
            cursor.execute(sql)
        else:
            cursor.execute(sql, sql_vars)
        return cursor

    def _fetchall(self, sql: str, sql_vars: Any = None) -> Iterable[DictRow]:
        """
        cursor.fetchall() with reconnect
        """

        with closing(self.cursor()) as cursor:
            return self._execute(cursor, sql, sql_vars).fetchall()

    def _fetchone(self, sql, sql_vars: Any = None, itersize: int = 1) -> DictRow | None:
        with closing(self.cursor(itersize)) as cursor:
            return self._execute(cursor, sql, sql_vars).fetchone()

    def _fetchmany(
        self, sql: str, size: int, sql_vars: Any = None, itersize: int = 0
    ) -> Iterable[Iterable[DictRow]]:
        with closing(self.cursor(itersize)) as cursor:
            self._execute(cursor, sql, sql_vars)

            while True:
                rows = cursor.fetchmany(size)
                if len(rows) > 0:
                    yield rows
                else:
                    return

    def fetchall(
        self, sql: str, sql_vars: Any = None, itersize: int = 0
    ) -> Iterable[DictRow]:
        """
        cursor.fetchall() with reconnect
        """

        return self.back_connection()(self._fetchall)(sql, sql_vars, itersize)

    def fetchone(
        self, sql: str, sql_vars: Any = None, itersize: int = 0
    ) -> Iterable[DictRow]:
        """
        cursor.fetchone() with reconnect
        """

        return self.back_connection()(self._fetchone)(sql, sql_vars)

    def fetchmany(self, sql: str, size: int, sql_vars: Any = None, itersize: int = 0):
        """
        cursor.fetchmany with reconnect and batch control

        sql: str - SQL expression
        size: int - number of rows to read
        close: bool - close after first batch
        intersize: int - if > 0, creates server-side cursor with
            len(batch) == intersize

        """

        return self.back_connection()(self._fetchmany)(sql, size, sql_vars, itersize)


class DBTemplatePSQL(DBTemplateABC):
    def __init__(
        self, connection_manager=PostgresConnectionManager(PostgresConnector())
    ):
        self.connection_manager = connection_manager
        self.templates = settings.templates_collection
        self.templates_id_field = settings.templates_id_field

    async def get_one_template(self, template_id: UUID):
        raw_template = self.connection_manager.fetchone(
            f"SELECT body from {self.templates} WHERE {self.templates_id_field} = '{template_id}'"
        )
        return raw_template[0]
