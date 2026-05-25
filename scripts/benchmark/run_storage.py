import pandas as pd

from pathlib import Path

from scripts.db.connect import connect


BASE_DIR = Path(__file__).resolve().parents[2]

OUTPUT_FILE = (
    BASE_DIR
    / "results/storage/storage_results.csv"
)


MOBILITY_TABLES = [
    ("readings_mobility_small", "small"),
    ("readings_mobility_medium", "medium"),
    ("readings_mobility_large", "large"),
]


TIMESCALE_TABLES = [
    ("readings_timescale_small", "small"),
    ("readings_timescale_medium", "medium"),
    ("readings_timescale_large", "large"),
]


# MobilityDB table size
MOBILITY_QUERY = """
SELECT
    %s AS relname,
    pg_total_relation_size(%s) AS total_bytes,
    pg_relation_size(%s) AS table_bytes,
    pg_indexes_size(%s) AS index_bytes,
    pg_total_relation_size(%s)
      - pg_relation_size(%s)
      - pg_indexes_size(%s) AS toast_bytes;
"""


# TimescaleDB hypertable chunk size
TIMESCALE_QUERY = """
SELECT
    %s AS relname,

    SUM(
        pg_total_relation_size(
            format('%%I.%%I', chunk_schema, chunk_name)::regclass
        )
    ) AS total_bytes,

    SUM(
        pg_relation_size(
            format('%%I.%%I', chunk_schema, chunk_name)::regclass
        )
    ) AS table_bytes,

    SUM(
        pg_indexes_size(
            format('%%I.%%I', chunk_schema, chunk_name)::regclass
        )
    ) AS index_bytes,

    SUM(
        pg_total_relation_size(
            format('%%I.%%I', chunk_schema, chunk_name)::regclass
        )
    )
    -
    SUM(
        pg_relation_size(
            format('%%I.%%I', chunk_schema, chunk_name)::regclass
        )
    )
    -
    SUM(
        pg_indexes_size(
            format('%%I.%%I', chunk_schema, chunk_name)::regclass
        )
    ) AS toast_bytes

FROM timescaledb_information.chunks

WHERE hypertable_name = %s;
"""
def to_mb(value):

    return round(
        value / (1024 * 1024),
        2
    )


def measure_mobility(cur, table):

    cur.execute(
        MOBILITY_QUERY,
        (table, table, table, table, table, table, table)
    )

    return cur.fetchone()


def measure_timescale(cur, table):

    cur.execute(
        TIMESCALE_QUERY,
        (table, table)
    )

    return cur.fetchone()


def main():

    conn = connect()
    cur = conn.cursor()

    results = []

    print("\n=== STORAGE BENCHMARK ===\n")

    # MobilityDB
    for table, dataset in MOBILITY_TABLES:

        print(f"[MOBILITY] {table}")

        row = measure_mobility(cur, table)

        results.append({
            "system": "mobility",
            "dataset": dataset,
            "table": row[0],

            "total_bytes": row[1],
            "table_bytes": row[2],
            "index_bytes": row[3],
            "toast_bytes": row[4],

            "total_mb": to_mb(row[1]),
            "table_mb": to_mb(row[2]),
            "index_mb": to_mb(row[3]),
            "toast_mb": to_mb(row[4]),
        })

    # TimescaleDB
    for table, dataset in TIMESCALE_TABLES:

        print(f"[TIMESCALE] {table}")

        row = measure_timescale(cur, table)

        results.append({
            "system": "timescale",
            "dataset": dataset,
            "table": row[0],

            "total_bytes": row[1],
            "table_bytes": row[2],
            "index_bytes": row[3],
            "toast_bytes": row[4],

            "total_mb": to_mb(row[1]),
            "table_mb": to_mb(row[2]),
            "index_mb": to_mb(row[3]),
            "toast_mb": to_mb(row[4]),
        })

    cur.close()
    conn.close()

    df = pd.DataFrame(results)

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(f"\nResults saved to: {OUTPUT_FILE}\n")

    print(df[
        [
            "system",
            "dataset",
            "total_mb",
            "table_mb",
            "index_mb",
            "toast_mb"
        ]
    ])


if __name__ == "__main__":
    main()