#!/usr/bin/env python3
"""
Generator that streams rows one by one from the MySQL table `user_data`.

Prototype: def stream_users()
Constraint: This file contains no more than one loop.
"""

from typing import Dict, Generator

from seed import connect_to_prodev


def stream_users() -> Generator[Dict[str, object], None, None]:
    """Yield user rows one-by-one from the `user_data` table.

    Uses an unbuffered server-side cursor so iteration streams results
    without loading all rows into memory.
    """
    connection = connect_to_prodev()
    cursor = connection.cursor(dictionary=True, buffered=False)
    try:
        cursor.execute("SELECT user_id, name, email, age FROM `user_data`")
        for row in cursor:  # single loop per requirements
            yield row
    finally:
        cursor.close()
        connection.close()


