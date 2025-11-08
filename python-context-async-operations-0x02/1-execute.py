#!/usr/bin/env python3
"""Reusable context manager to execute parameterised SQLite queries."""

import sqlite3
from typing import Iterable, Sequence


class ExecuteQuery:
    """
    A reusable context manager to execute a specific SQL query with optional
    parameters, managing the connection lifecycle.
    """

    def __init__(
        self,
        query: str,
        params: Sequence | None = None,
        db_name: str = "user_data.db",
    ) -> None:
        self.db_name = db_name
        self.query = query
        self.params = list(params) if params is not None else []
        self.conn: sqlite3.Connection | None = None
        self.cursor: sqlite3.Cursor | None = None
        self.results: Iterable | None = None

    def __enter__(self) -> Iterable:
        """
        Connects to the database, executes the query, and stores results.
        Returns the stored results.
        """
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            self.cursor.execute(self.query, self.params)
            self.results = self.cursor.fetchall()
            self.conn.commit()
            return self.results
        except sqlite3.Error as error:
            print(f"Database error during query execution: {error}")
            self.results = []
            raise

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """Closes the database connection."""
        if self.conn:
            self.conn.close()
        return False


if __name__ == "__main__":
    QUERY = "SELECT * FROM users WHERE age > ?"
    AGE_THRESHOLD = 25

    print(f"--- Executing query: {QUERY} with age > {AGE_THRESHOLD} ---")

    try:
        with ExecuteQuery(QUERY, [AGE_THRESHOLD]) as users:
            print("Filtered Users:")
            if users:
                for user in users:
                    print(user)
            else:
                print("No users found matching the criteria.")
    except sqlite3.OperationalError as error:
        print(f"An error occurred: {error}")
        print("Did you run the setup_db.py script to create the 'users' table?")

    print("--- Connection automatically closed after query execution ---")

