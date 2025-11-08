#!/usr/bin/env python3
"""
Module providing decorators for database connection management and retry logic.
"""

import functools
import sqlite3
import time
from typing import Any, Callable, Optional, Type


def with_db_connection(func: Callable) -> Callable:
    """
    Decorator that opens a SQLite connection, passes it to the wrapped
    function, and ensures the connection is closed afterwards.
    """

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        conn = sqlite3.connect("users.db")
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()

    return wrapper


def retry_on_failure(retries: int = 3, delay: float = 2.0, exceptions: Optional[Type[Exception]] = None) -> Callable:
    """
    Decorator factory that retries the wrapped function when specific exceptions
    are raised. By default retries on any Exception.
    """

    exceptions = exceptions or Exception

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            attempt = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:
                    attempt += 1
                    if attempt > retries:
                        raise
                    time.sleep(delay)

        return wrapper

    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


if __name__ == "__main__":
    users = fetch_users_with_retry()
    print(users)

