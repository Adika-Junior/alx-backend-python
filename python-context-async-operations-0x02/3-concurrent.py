#!/usr/bin/env python3
"""Concurrent asynchronous SQLite queries using aiosqlite and asyncio.gather."""

import asyncio
import sqlite3

import aiosqlite

DB_NAME = "user_data.db"


async def async_fetch_users():
    """Fetch all users asynchronously."""
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            results = await cursor.fetchall()
            return "All Users", results


async def async_fetch_older_users():
    """Fetch users older than 40 asynchronously."""
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            results = await cursor.fetchall()
            return "Users Older Than 40", results


async def fetch_concurrently():
    """Run multiple asynchronous fetch functions concurrently."""
    print("Starting concurrent database fetches...")

    try:
        results = await asyncio.gather(
            async_fetch_users(),
            async_fetch_older_users(),
        )

        print("\n--- Concurrent Results ---")
        for title, data in results:
            print(f"**{title}:**")
            if data:
                for row in data:
                    print(f"  {row}")
            else:
                print("  No results found.")
    except sqlite3.OperationalError as error:
        print(f"An error occurred: {error}")
        print("Did you run the setup_db.py script to create the 'users' table?")

    print("\nConcurrent fetches completed.")


if __name__ == "__main__":
    print("Starting asyncio event loop...")
    asyncio.run(fetch_concurrently())
    print("Asyncio event loop finished.")

