#!/usr/bin/env python3
"""
Module providing decorators for database connection and transaction management.
"""

import functools
import sqlite3
from typing import Any, Callable


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


def transactional(func: Callable) -> Callable:
    """
    Decorator that wraps the execution of `func` in a database transaction.
    Commits if the wrapped function succeeds; rolls back on exception.
    """

    @functools.wraps(func)
    def wrapper(conn: sqlite3.Connection, *args: Any, **kwargs: Any) -> Any:
        try:
            result = func(conn, *args, **kwargs)
        except Exception:
            conn.rollback()
            raise
        else:
            conn.commit()
            return result

    return wrapper


@with_db_connection
@transactional
def update_user_email(conn: sqlite3.Connection, user_id: int, new_email: str) -> None:
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))


if __name__ == "__main__":
    update_user_email(user_id=1, new_email="Crawford_Cartwright@hotmail.com")

