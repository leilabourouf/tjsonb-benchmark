from pathlib import Path

from scripts.db.connect import connect


BASE_DIR = Path(__file__).resolve().parents[2]

SQL_FILES = [
    BASE_DIR / "sql/indexes/mobility.sql",
    BASE_DIR / "sql/indexes/timescale.sql",
]


def run_sql(cur, path):

    print(f"Running {path.name}")

    sql = path.read_text()

    cur.execute(sql)


def main():

    conn = connect()
    cur = conn.cursor()

    for path in SQL_FILES:

        run_sql(cur, path)

        conn.commit()

    cur.close()
    conn.close()

    print("\nIndex setup complete")


if __name__ == "__main__":
    main()