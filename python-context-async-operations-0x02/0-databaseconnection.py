#!/usr/bin/env python3
"""Custom class-based context manager for SQLite connections."""

import sqlite3


class DatabaseConnection:
    """Context manager that opens a database connection and ensures cleanup."""

    def __init__(self, db_name: str = "user_data.db") -> None:
        self.db_name = db_name
        self.conn: sqlite3.Connection | None = None
        self.cursor: sqlite3.Cursor | None = None

    def __enter__(self) -> sqlite3.Cursor:
        """Connect to the database and return a cursor."""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """Commit pending transactions and close the connection."""
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()

        # Propagate exceptions
        return False


if __name__ == "__main__":
    print("--- Executing query with DatabaseConnection Context Manager ---")

    try:
        with DatabaseConnection() as cursor:
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

