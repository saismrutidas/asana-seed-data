import sqlite3
from typing import Iterable, Tuple


def execute_many(
    conn: sqlite3.Connection,
    query: str,
    rows: Iterable[Tuple]
):
    """
    Execute a parameterized INSERT query with multiple rows.
    """
    cursor = conn.cursor()
    cursor.executemany(query, rows)
    conn.commit()


def execute_one(
    conn: sqlite3.Connection,
    query: str,
    params: Tuple
):
    """
    Execute a single parameterized query.
    """
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()


def fetch_all(
    conn: sqlite3.Connection,
    query: str,
    params: Tuple = ()
):
    """
    Fetch all rows from a SELECT query.
    """
    cursor = conn.cursor()
    cursor.execute(query, params)
    return cursor.fetchall()
