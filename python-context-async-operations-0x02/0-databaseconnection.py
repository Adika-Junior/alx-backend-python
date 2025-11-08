#!/usr/bin/env python3
"""Custom class-based context manager for SQLite connections."""

import sqlite3
from typing import Optional


class DatabaseConnection:
    """Context manager that opens a database connection and ensures cleanup."""

    def __init__(self, db_name: str = "user_data.db", verbose: bool = False) -> None:
        self.db_name = db_name
        self.verbose = verbose
        self.conn: Optional[sqlite3.Connection] = None
        self.cursor: Optional[sqlite3.Cursor] = None

    def __enter__(self) -> sqlite3.Cursor:
        """Connect to the database and return a cursor."""
        self.conn = sqlite3.connect(self.db_name)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

        if self.verbose:
            print(f"[MANAGER] Opened connection to {self.db_name}")

        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """Commit pending transactions and close the connection."""
        if self.cursor is not None:
            self.cursor.close()
            self.cursor = None

        if self.conn is not None:
            if exc_type is None:
                self.conn.commit()
                if self.verbose:
                    print("[MANAGER] Transaction committed.")
            else:
                self.conn.rollback()
                if self.verbose:
                    print(f"[MANAGER] Transaction rolled back: {exc_val}")

            self.conn.close()
            if self.verbose:
                print("[MANAGER] Connection closed.")
            self.conn = None

        # Propagate exceptions
        return False


if __name__ == "__main__":
    print("--- Executing query with DatabaseConnection Context Manager ---")

    try:
        with DatabaseConnection(verbose=True) as cursor:
            cursor.execute("SELECT * FROM users")
            results = cursor.fetchall()

            print("Query: SELECT * FROM users")
            print("Results:")
            for row in results:
                print(row)
    except sqlite3.OperationalError as error:
        print(f"An error occurred: {error}")
        print("Did you run the setup_db.py script to create the 'users' table?")

    print("--- Connection is automatically closed ---")

