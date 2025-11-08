#!/usr/bin/env python3
"""
Module providing decorators for database connection management and query caching.
"""

import functools
import sqlite3
import time
from typing import Any, Callable, Dict, Tuple


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


query_cache: Dict[Tuple[str, Tuple[Any, ...], Tuple[Tuple[str, Any], ...]], Any] = {}


def cache_query(func: Callable) -> Callable:
    """
    Decorator that caches database query results based on the SQL query string
    and supplied arguments.
    """

    @functools.wraps(func)
    def wrapper(conn: sqlite3.Connection, *args: Any, **kwargs: Any) -> Any:
        query = kwargs.get("query")
        if query is None:
            if args:
                query = args[0]

        cache_key = (
            query,
            args,
            tuple(sorted(kwargs.items())),
        )

        if query is not None and cache_key in query_cache:
            return query_cache[cache_key]

        result = func(conn, *args, **kwargs)

        if query is not None:
            query_cache[cache_key] = result

        return result

    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn: sqlite3.Connection, query: str):
    cursor = conn.cursor()
    cursor.execute(query)
    # Simulate a delay to highlight caching benefits
    time.sleep(0.5)
    return cursor.fetchall()


if __name__ == "__main__":
    users = fetch_users_with_cache(query="SELECT * FROM users")
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    print(users)
    print(users_again)

