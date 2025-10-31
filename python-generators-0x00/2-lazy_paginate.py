#!/usr/bin/env python3
"""
Lazy pagination over the `user_data` table using a generator.

Includes:
- paginate_users(page_size, offset)
- lazy_paginate(page_size)

Constraints:
- Only one loop in this file (in lazy_paginate)
- Must use yield
"""

from typing import Dict, Generator, List

from seed import connect_to_prodev


def paginate_users(page_size: int, offset: int) -> List[Dict[str, object]]:
    """Fetch one page of users starting at the given offset.

    Returns a list of row dicts with length up to page_size.
    """
    if page_size <= 0:
        raise ValueError("page_size must be > 0")
    if offset < 0:
        raise ValueError("offset must be >= 0")

    connection = connect_to_prodev()
    # regular buffered cursor is fine for a single page
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT * FROM user_data LIMIT %s OFFSET %s",
            (int(page_size), int(offset)),
        )
        rows = cursor.fetchall()
        return rows
    finally:
        cursor.close()
        connection.close()


def lazy_paginate(page_size: int) -> Generator[List[Dict[str, object]], None, None]:
    """Yield successive pages lazily, fetching the next page only when needed.

    Starts at offset 0 and advances by the number of rows returned each time.
    Contains the only loop in this file as required.
    """
    offset = 0
    while True:  # single loop
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += len(page)


# Compatibility alias expected by some test harnesses
lazy_pagination = lazy_paginate


