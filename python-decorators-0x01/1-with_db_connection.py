#!/usr/bin/env python3
"""
Module that defines the `with_db_connection` decorator.
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


@with_db_connection
def get_user_by_id(conn: sqlite3.Connection, user_id: int):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()


if __name__ == "__main__":
    user = get_user_by_id(user_id=1)
    print(user)

