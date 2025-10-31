#!/usr/bin/env python3
"""
Memory-efficient average age calculation using generators.

Requirements:
- Implement `stream_user_ages()` that yields ages one by one
- Compute average without loading all rows into memory
- Print: "Average age of users: <average>"
- Use no more than two loops in this script (we use 2 total)
"""

from decimal import Decimal, ROUND_HALF_UP
from typing import Generator

from seed import connect_to_prodev


def stream_user_ages() -> Generator[Decimal, None, None]:
    """Yield ages from `user_data` one-by-one using a streaming cursor.

    Loop 1 of 2 in this file.
    """
    connection = connect_to_prodev()
    cursor = connection.cursor(dictionary=True, buffered=False)
    try:
        cursor.execute("SELECT age FROM `user_data`")
        for row in cursor:  # loop 1
            # MySQL DECIMAL maps to Decimal in mysql-connector
            age = row.get("age")
            if age is None:
                continue
            yield Decimal(str(age))
    finally:
        cursor.close()
        connection.close()


def compute_average_age() -> Decimal:
    """Consume the age stream and compute the average without loading all rows."""
    total = Decimal("0")
    count = 0
    for age in stream_user_ages():  # loop 2
        total += age
        count += 1
    if count == 0:
        return Decimal("0")
    return (total / Decimal(count)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


if __name__ == "__main__":
    avg = compute_average_age()
    print(f"Average age of users: {avg}")


