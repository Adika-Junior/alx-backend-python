#!/usr/bin/env python3
"""
Seed script for MySQL and a generator that streams rows one by one.

Functions:
- connect_db()
- create_database(connection)
- connect_to_prodev()
- create_table(connection)
- insert_data(connection, data)
- stream_user_rows(connection, chunk_size=100)

Environment variables used for MySQL connection:
- MYSQL_HOST (default: localhost)
- MYSQL_PORT (default: 3306)
- MYSQL_USER (default: root)
- MYSQL_PASSWORD (default: empty)

CSV path can be provided via USER_DATA_CSV (default: ./user_data.csv)
"""

import csv
import os
import sys
import uuid
from decimal import Decimal
from typing import Dict, Generator, Iterable, Optional

import mysql.connector
from mysql.connector import MySQLConnection


DB_NAME = "ALX_prodev"
TABLE_NAME = "user_data"


def _get_mysql_config(include_database: bool = False) -> Dict[str, object]:
    config = {
        "host": os.getenv("MYSQL_HOST", "localhost"),
        "port": int(os.getenv("MYSQL_PORT", "3306")),
        "user": os.getenv("MYSQL_USER", "root"),
        "password": os.getenv("MYSQL_PASSWORD", ""),
    }
    if include_database:
        config["database"] = DB_NAME
    return config


def connect_db() -> MySQLConnection:
    """Connects to the MySQL server (no default database)."""
    return mysql.connector.connect(**_get_mysql_config(include_database=False))


def create_database(connection: MySQLConnection) -> None:
    """Creates the database ALX_prodev if it does not exist."""
    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}`")
    finally:
        cursor.close()


def connect_to_prodev() -> MySQLConnection:
    """Connects to the ALX_prodev database in MySQL."""
    return mysql.connector.connect(**_get_mysql_config(include_database=True))


def create_table(connection: MySQLConnection) -> None:
    """Creates table user_data if it does not exist with required fields."""
    cursor = connection.cursor()
    try:
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS `{TABLE_NAME}` (
                `user_id` CHAR(36) NOT NULL,
                `name` VARCHAR(255) NOT NULL,
                `email` VARCHAR(255) NOT NULL,
                `age` DECIMAL(5,2) NOT NULL,
                PRIMARY KEY (`user_id`),
                INDEX `idx_user_id` (`user_id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """
        )
    finally:
        cursor.close()


def _coerce_age(value: str) -> Decimal:
    value = (value or "").strip()
    if not value:
        raise ValueError("age is required")
    return Decimal(value)


def _row_to_tuple(row: Dict[str, str]) -> Dict[str, object]:
    user_id = row.get("user_id")
    if user_id:
        user_id = str(user_id).strip()
    if not user_id:
        user_id = str(uuid.uuid4())
    name = (row.get("name") or "").strip()
    email = (row.get("email") or "").strip()
    age = _coerce_age(str(row.get("age")))
    return {
        "user_id": user_id,
        "name": name,
        "email": email,
        "age": age,
    }


def insert_data(connection: MySQLConnection, data: Iterable[Dict[str, object]]) -> int:
    """
    Inserts data into the database.
    - If a row with the same user_id exists, it will be ignored (no-op).
    Returns number of attempted inserts (not necessarily affected rows).
    """
    cursor = connection.cursor()
    attempted = 0
    try:
        sql = (
            f"INSERT INTO `{TABLE_NAME}` (user_id, name, email, age) "
            "VALUES (%s, %s, %s, %s) "
            "ON DUPLICATE KEY UPDATE user_id = user_id"
        )
        for item in data:
            attempted += 1
            cursor.execute(
                sql,
                (
                    item["user_id"],
                    item["name"],
                    item["email"],
                    str(item["age"]),
                ),
            )
        connection.commit()
        return attempted
    finally:
        cursor.close()


def stream_user_rows(connection: MySQLConnection, chunk_size: int = 100) -> Generator[Dict[str, object], None, None]:
    """
    Generator that streams rows one by one from the database.
    Uses an unbuffered server-side cursor and fetchmany to limit memory use.
    """
    # dictionary=True yields dict rows; buffered=False enables streaming
    cursor = connection.cursor(dictionary=True, buffered=False)
    try:
        cursor.execute(f"SELECT user_id, name, email, age FROM `{TABLE_NAME}`")
        while True:
            rows = cursor.fetchmany(size=chunk_size)
            if not rows:
                break
            for row in rows:
                yield row
    finally:
        cursor.close()


def _ensure_sample_csv(csv_path: str) -> None:
    """
    If user_data.csv is missing, create a small sample file as a fallback.
    This allows the script to be runnable out-of-the-box.
    """
    if os.path.exists(csv_path):
        return
    rows = [
        {"name": "Alice Smith", "email": "alice@example.com", "age": "30"},
        {"name": "Bob Jones", "email": "bob@example.com", "age": "41.5"},
        {"name": "Charlie Ray", "email": "charlie@example.com", "age": "22"},
    ]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["user_id", "name", "email", "age"])
        writer.writeheader()
        for r in rows:
            writer.writerow({"user_id": "", **r})


def _read_csv_rows(csv_path: str) -> Iterable[Dict[str, object]]:
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield _row_to_tuple(row)


def main(argv: Optional[Iterable[str]] = None) -> int:
    csv_path = os.getenv("USER_DATA_CSV", os.path.join(os.path.dirname(__file__), "user_data.csv"))

    # Ensure CSV exists (fallback sample if missing)
    _ensure_sample_csv(csv_path)

    # 1) Connect to server and create database
    server_conn = connect_db()
    try:
        create_database(server_conn)
    finally:
        server_conn.close()

    # 2) Connect to ALX_prodev and create table
    db_conn = connect_to_prodev()
    try:
        create_table(db_conn)

        # 3) Insert CSV data
        inserted = insert_data(db_conn, _read_csv_rows(csv_path))
        print(f"Processed {inserted} CSV rows (duplicates ignored).")

        # 4) Demonstrate streaming generator (prints the first few rows)
        print("Streaming rows:")
        count = 0
        for row in stream_user_rows(db_conn, chunk_size=50):
            print(row)
            count += 1
            if count >= 5:
                break
    finally:
        db_conn.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))


