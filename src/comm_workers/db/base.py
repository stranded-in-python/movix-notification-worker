import functools
import time
from abc import ABC, abstractmethod
from typing import Callable

from core.config import settings
from core.loggers import LOGGER
from psycopg2 import OperationalError
from psycopg2.extensions import connection as pg_connection


class Connector(ABC):
    def __init__(self):
        self.connection: pg_connection | None = None

    @abstractmethod
    def _connect(self) -> pg_connection:
        ...

    @abstractmethod
    def _ping(self):
        ...

    def connect(self) -> pg_connection:
        if not self.connection:
            self.connection = self._connect()
        return self.connection

    def reconnect(self):
        self.connection = self._connect()
        self._ping()


def backing_connect(connector: Connector) -> Callable:
    def decorator(func: Callable):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            wait = settings.first_nap
            time_passed = 0
            is_connected = True
            while time_passed < settings.wait_up_to:
                try:
                    # trying to reconnect
                    if not is_connected:
                        connector.reconnect()  # type: ignore

                    return func(*args, **kwargs)
                except (OperationalError or ConnectionError) as e:
                    LOGGER.error(e)
                    is_connected = False
                    time_passed += wait
                    wait = (
                        wait * settings.waiting_factor
                        if wait < settings.waiting_interval
                        else settings.waiting_interval
                    )
                    LOGGER.debug(f"Sleeping for {wait} seconds")
                    time.sleep(wait)
            raise Exception("Waiting for connection exceeded limit")

        return inner

    return decorator


class ConnectionManager:
    def __init__(self, connector: Connector):
        self.connector = connector
        self._connection = None

    def back_connection(self) -> Callable:
        return backing_connect(self.connector)

    def get_connection(self) -> pg_connection:
        if self._connection:
            return self._connection

        self._connection = self.back_connection()(self.connector.connect)()
        return self._connection

    @property
    def connection(self) -> pg_connection | None:
        return self.get_connection()

    @connection.setter
    def connection(self, connection: pg_connection | None):
        self._connection = connection

    def __exit__(self, *args):
        if not self._connection:
            return

        self._connection.close()
        self._connection = None  # type: ignore
        LOGGER.debug("Closed connection")

    def __enter__(self):
        return self
