## Python MySQL generators: seeding, streaming, batching, pagination, and aggregates

This folder contains scripts to seed a MySQL database and demonstrate Python generators for streaming rows, batching, lazy pagination, and computing an aggregate (average age) memory‑efficiently.

### Requirements

- Python 3.8+
- MySQL server
- Package: `mysql-connector-python`

Install dependency:

```bash
pip install mysql-connector-python
```

### Environment variables

- `MYSQL_HOST` (default: `localhost`)
- `MYSQL_PORT` (default: `3306`)
- `MYSQL_USER` (default: `root`)
- `MYSQL_PASSWORD` (default: empty)
- `USER_DATA_CSV` (optional path to `user_data.csv`; default: `./user_data.csv` in this directory)

### What the script does

`seed.py` will:
- Connect to MySQL server
- Create database `ALX_prodev` if it does not exist
- Connect to `ALX_prodev`
- Create table `user_data` if it does not exist with schema:
  - `user_id` CHAR(36) PRIMARY KEY (indexed)
  - `name` VARCHAR(255) NOT NULL
  - `email` VARCHAR(255) NOT NULL
  - `age` DECIMAL(5,2) NOT NULL
- Read `user_data.csv` and insert rows (duplicates by `user_id` ignored)
- Demonstrate the generator by streaming and printing up to 5 rows

If `user_data.csv` is missing, the script creates a tiny sample CSV so it can run out of the box.

### Usage

```bash
cd /home/j_view/Projects/alx-backend-python/python-generators-0x00
python3 seed.py
```

Example with custom connection:

```bash
export MYSQL_HOST=127.0.0.1
export MYSQL_PORT=3306
export MYSQL_USER=root
export MYSQL_PASSWORD=secret
export USER_DATA_CSV=/absolute/path/to/user_data.csv
python3 seed.py
```

### Scripts overview

- `seed.py`
  - Functions:
    - `connect_db()` — connect to server (no DB)
    - `create_database(connection)` — ensure `ALX_prodev`
    - `connect_to_prodev()` — connect to `ALX_prodev`
    - `create_table(connection)` — ensure `user_data`
    - `insert_data(connection, data)` — insert rows (ignore duplicates)
    - `stream_user_rows(connection, chunk_size=100)` — stream rows with server‑side cursor
  - Run directly to seed and preview a few streamed rows.

- `0-stream_users.py`
  - `stream_users()` — generator yielding rows one by one using an unbuffered cursor (single loop).
  - Example:
    ```python
    from 0-stream_users import stream_users
    for row in stream_users():
        print(row)
    ```

- `1-batch_processing.py`
  - `stream_users_in_batches(batch_size)` — yields lists of rows using `fetchmany`.
  - `batch_processing(batch_size)` — yields filtered batches where `age > 25`.
  - Example:
    ```python
    from 1-batch_processing import batch_processing
    for batch in batch_processing(100):
        print(batch)
    ```

- `2-lazy_paginate.py`
  - `paginate_users(page_size, offset)` — fetch one page.
  - `lazy_paginate(page_size)` — lazily yield pages starting at offset 0 (single loop).
  - Example:
    ```python
    from 2-lazy_paginate import lazy_paginate
    for page in lazy_paginate(50):
        for row in page:
            print(row)
    ```

- `4-stream_ages.py`
  - `stream_user_ages()` — yields ages one by one (streaming cursor).
  - `compute_average_age()` — computes memory‑efficient average (no SQL AVG).
  - CLI output when run directly:
    ```
    Average age of users: <value>
    ```

### Make scripts executable and run

```bash
chmod +x ./seed.py ./0-stream_users.py ./1-batch_processing.py ./2-lazy_paginate.py ./4-stream_ages.py
./seed.py
./4-stream_ages.py
```

### References

- asyncio — Asynchronous I/O: `https://docs.python.org/3/library/asyncio.html`
- Context Managers: `https://book.pythontips.com/en/latest/context_managers.html`
- Python Decorators: `https://realpython.com/primer-on-python-decorators/#simple-decorators-in-python`
- Python Generators: `https://realpython.com/introduction-to-python-generators/`
- Python Wiki — Generators: `https://wiki.python.org/moin/Generators`


