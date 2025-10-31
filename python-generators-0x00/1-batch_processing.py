#!/usr/bin/env python3
"""
Batch streaming and processing using Python generators.

Prototypes:
- def stream_users_in_batches(batch_size)
- def batch_processing(batch_size)

Constraints:
- Use yield-based generators
- No more than 3 loops in this file (we use 2 total)
"""

from typing import Dict, Generator, List

from seed import connect_to_prodev


def stream_users_in_batches(batch_size: int) -> Generator[List[Dict[str, object]], None, None]:
    """Fetch rows from `user_data` in batches and yield lists of row dicts.

    Uses an unbuffered server-side cursor with fetchmany to limit memory usage.
    Single loop by design.
    """
    if batch_size <= 0:
        raise ValueError("batch_size must be > 0")

    connection = connect_to_prodev()
    cursor = connection.cursor(dictionary=True, buffered=False)
    try:
        cursor.execute("SELECT user_id, name, email, age FROM user_data")
        while True:  # loop 1
            batch = cursor.fetchmany(size=batch_size)
            if not batch:
                break
            yield batch
    finally:
        cursor.close()
        connection.close()


def batch_processing(batch_size: int) -> int:
    """Process each batch to filter users over age > 25 and print them.

    Designed to work even if the caller does not iterate over any generator.
    """
    printed = 0
    for batch in stream_users_in_batches(batch_size):  # loop 2
        filtered = [row for row in batch if float(row.get("age", 0)) > 25]
        if filtered:
            for row in filtered:  # loop 3
                print(row)
                printed += 1
    return printed


