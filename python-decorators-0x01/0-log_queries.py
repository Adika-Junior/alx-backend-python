#!/usr/bin/env python3
"""
Module that defines the `log_queries` decorator.
"""

import functools
from datetime import datetime
from typing import Any, Callable


def log_queries(func: Callable) -> Callable:
    """
    Decorator that logs the SQL query passed to `func` before execution.
    """

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        query = kwargs.get("query")

        if query is None:
            for arg in args:
                if isinstance(arg, str):
                    query = arg
                    break

        timestamp = datetime.utcnow().isoformat()

        if query is not None:
            print(f"[{timestamp}] [log_queries] Executing SQL query: {query}")
        else:
            print(f"[{timestamp}] [log_queries] Executing {func.__name__} without an explicit SQL query argument.")

        return func(*args, **kwargs)

    return wrapper


if __name__ == "__main__":
    import sqlite3

    @log_queries
    def fetch_all_users(query: str):
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        return results

    users = fetch_all_users(query="SELECT * FROM users")
    print(users)

