"""Database inspection script

Connects to Postgres (or other SQLAlchemy-supported DB) using the URL from
`env_load_util.env.get_database_url()` and prints tables, row counts, and sample rows.

Usage: python scripts/db_inspect.py
"""
from __future__ import annotations

import argparse
import sys
from typing import Optional

# Add repo root to sys.path when run as a script
from pathlib import Path
_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from sqlalchemy import create_engine, text, inspect

from scripts.env_load_util import env


def connect_engine(database_url: Optional[str]):
    if not database_url:
        raise ValueError("No database URL available; set POSTGRES_* or DATABASE_URL in .env")
    engine = create_engine(database_url, future=True)
    return engine


def list_tables(engine):
    insp = inspect(engine)
    return insp.get_table_names()


def get_row_count(engine, table):
    with engine.connect() as conn:
        res = conn.execute(text(f"SELECT count(*) FROM {table}"))
        return res.scalar()


def sample_rows(engine, table, limit=5):
    with engine.connect() as conn:
        res = conn.execute(text(f"SELECT * FROM {table} LIMIT :l"), {"l": limit})
        cols = res.keys()
        return cols, res.fetchall()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample", "-n", type=int, default=5, help="sample rows per table")
    args = parser.parse_args()

    env.load()
    db_url = env.get_database_url()
    if not db_url:
        print("Could not determine database URL from environment. Check .env and env_load_util." )
        sys.exit(1)

    engine = connect_engine(db_url)
    print("Connected to:", db_url)

    try:
        tables = list_tables(engine)
    except Exception as e:
        print("Failed to list tables:", e)
        sys.exit(1)

    if not tables:
        print("No tables found.")
        return

    print("Found tables:")
    for t in tables:
        try:
            cnt = get_row_count(engine, t)
        except Exception as e:
            cnt = f"error: {e}"
        print(f"- {t}: {cnt} rows")
        try:
            cols, rows = sample_rows(engine, t, args.sample)
            if rows:
                print("  sample row:")
                for r in rows[:3]:
                    print("   ", dict(zip(cols, r)))
        except Exception as e:
            print(f"  failed to sample rows: {e}")


if __name__ == "__main__":
    main()
