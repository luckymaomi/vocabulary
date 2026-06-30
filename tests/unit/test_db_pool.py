import sqlite3

from core.db_pool import DatabasePool


def test_database_pool_reuses_connection(tmp_path):
    db_path = tmp_path / "test.sqlite"
    pool = DatabasePool(str(db_path), pool_size=1)
    pool.initialize()

    with pool.get_db() as conn:
        conn.execute("CREATE TABLE sample (id INTEGER PRIMARY KEY, name TEXT)")
        conn.execute("INSERT INTO sample (name) VALUES ('alpha')")
        conn.commit()

    with pool.get_db() as conn:
        row = conn.execute("SELECT name FROM sample WHERE id = 1").fetchone()

    assert row[0] == "alpha"
    pool.close_all()


def test_database_pool_timeout_returns_none(tmp_path):
    db_path = tmp_path / "test.sqlite"
    pool = DatabasePool(str(db_path), pool_size=1)
    pool.initialize()
    conn = pool.get_connection()

    try:
        assert isinstance(conn, sqlite3.Connection)
        assert pool.get_connection(timeout=0.01) is None
    finally:
        pool.return_connection(conn)
        pool.close_all()
