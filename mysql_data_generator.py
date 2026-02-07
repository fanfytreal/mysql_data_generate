#!/usr/bin/env python3
"""Generate a MySQL sample database/table covering all common data types."""

import argparse
from datetime import datetime
import json
import os

import pymysql


ALL_TYPES_TABLE = "all_mysql_types"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a MySQL sample database with a table covering MySQL data types."
    )
    parser.add_argument("--host", default=os.getenv("MYSQL_HOST", "127.0.0.1"))
    parser.add_argument("--port", type=int, default=int(os.getenv("MYSQL_PORT", "3306")))
    parser.add_argument("--user", default=os.getenv("MYSQL_USER", "root"))
    parser.add_argument("--password", default=os.getenv("MYSQL_PASSWORD", ""))
    parser.add_argument(
        "--database",
        default=os.getenv("MYSQL_DATABASE", "sample_all_types"),
        help="Database to create/use for sample data.",
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Drop and recreate the database and table before inserting sample data.",
    )
    return parser.parse_args()


def connect_mysql(args: argparse.Namespace, database: str | None = None) -> pymysql.connections.Connection:
    return pymysql.connect(
        host=args.host,
        port=args.port,
        user=args.user,
        password=args.password,
        database=database,
        autocommit=True,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.Cursor,
    )


def create_database(cursor: pymysql.cursors.Cursor, database: str) -> None:
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{database}` CHARACTER SET utf8mb4")


def drop_database(cursor: pymysql.cursors.Cursor, database: str) -> None:
    cursor.execute(f"DROP DATABASE IF EXISTS `{database}`")


def create_table(cursor: pymysql.cursors.Cursor) -> None:
    ddl = f"""
    CREATE TABLE IF NOT EXISTS `{ALL_TYPES_TABLE}` (
        id BIGINT PRIMARY KEY AUTO_INCREMENT,
        tinyint_col TINYINT,
        smallint_col SMALLINT,
        mediumint_col MEDIUMINT,
        int_col INT,
        bigint_col BIGINT,
        decimal_col DECIMAL(10,2),
        float_col FLOAT,
        double_col DOUBLE,
        bit_col BIT(8),
        boolean_col BOOLEAN,
        date_col DATE,
        datetime_col DATETIME,
        timestamp_col TIMESTAMP NULL,
        time_col TIME,
        year_col YEAR,
        char_col CHAR(10),
        varchar_col VARCHAR(255),
        tinytext_col TINYTEXT,
        text_col TEXT,
        mediumtext_col MEDIUMTEXT,
        longtext_col LONGTEXT,
        binary_col BINARY(16),
        varbinary_col VARBINARY(255),
        tinyblob_col TINYBLOB,
        blob_col BLOB,
        mediumblob_col MEDIUMBLOB,
        longblob_col LONGBLOB,
        enum_col ENUM('red', 'green', 'blue'),
        set_col SET('alpha', 'beta', 'gamma'),
        json_col JSON,
        geometry_col GEOMETRY,
        point_col POINT,
        linestring_col LINESTRING,
        polygon_col POLYGON,
        multipoint_col MULTIPOINT,
        multilinestring_col MULTILINESTRING,
        multipolygon_col MULTIPOLYGON,
        geometrycollection_col GEOMETRYCOLLECTION
    ) ENGINE=InnoDB
    """
    cursor.execute(ddl)


def insert_sample(cursor: pymysql.cursors.Cursor) -> None:
    now = datetime.utcnow()
    json_payload = json.dumps({"name": "sample", "count": 1, "tags": ["mysql", "types"]})

    rows = [
        ("tinyint_col", "%s", 12),
        ("smallint_col", "%s", 32000),
        ("mediumint_col", "%s", 64000),
        ("int_col", "%s", 214748),
        ("bigint_col", "%s", 922337203),
        ("decimal_col", "%s", "12345.67"),
        ("float_col", "%s", 3.14),
        ("double_col", "%s", 2.7182818),
        ("bit_col", "b'10101010'", None),
        ("boolean_col", "%s", True),
        ("date_col", "%s", now.date()),
        ("datetime_col", "%s", now),
        ("timestamp_col", "%s", now),
        ("time_col", "%s", now.time()),
        ("year_col", "%s", 2024),
        ("char_col", "%s", "char-data"),
        ("varchar_col", "%s", "varchar-data"),
        ("tinytext_col", "%s", "tiny text"),
        ("text_col", "%s", "text data"),
        ("mediumtext_col", "%s", "medium text data"),
        ("longtext_col", "%s", "long text data"),
        ("binary_col", "UNHEX(%s)", "00FF00FF00FF00FF00FF00FF00FF00FF"),
        ("varbinary_col", "UNHEX(%s)", "ABCD1234"),
        ("tinyblob_col", "UNHEX(%s)", "DEADBEEF"),
        ("blob_col", "UNHEX(%s)", "BLOB00FF"),
        ("mediumblob_col", "UNHEX(%s)", "CAFEBABE"),
        ("longblob_col", "UNHEX(%s)", "FADEFADE"),
        ("enum_col", "%s", "red"),
        ("set_col", "%s", "alpha,beta"),
        ("json_col", "%s", json_payload),
        ("geometry_col", "ST_GeomFromText(%s)", "POINT(0 0)"),
        ("point_col", "ST_GeomFromText(%s)", "POINT(1 1)"),
        ("linestring_col", "ST_GeomFromText(%s)", "LINESTRING(0 0, 1 1, 2 2)"),
        ("polygon_col", "ST_GeomFromText(%s)", "POLYGON((0 0, 0 1, 1 1, 1 0, 0 0))"),
        ("multipoint_col", "ST_GeomFromText(%s)", "MULTIPOINT(0 0, 1 1)"),
        (
            "multilinestring_col",
            "ST_GeomFromText(%s)",
            "MULTILINESTRING((0 0, 1 1), (2 2, 3 3))",
        ),
        (
            "multipolygon_col",
            "ST_GeomFromText(%s)",
            "MULTIPOLYGON(((0 0, 0 1, 1 1, 1 0, 0 0)))",
        ),
        (
            "geometrycollection_col",
            "ST_GeomFromText(%s)",
            "GEOMETRYCOLLECTION(POINT(1 1), LINESTRING(0 0, 2 2))",
        ),
    ]

    columns = ", ".join(f"`{column}`" for column, _, _ in rows)
    expressions = ", ".join(expression for _, expression, _ in rows)
    values = [value for _, expression, value in rows if "%s" in expression]

    insert_sql = f"INSERT INTO `{ALL_TYPES_TABLE}` ({columns}) VALUES ({expressions})"
    cursor.execute(insert_sql, values)


def main() -> None:
    args = parse_args()
    with connect_mysql(args) as conn:
        with conn.cursor() as cursor:
            if args.reset:
                drop_database(cursor, args.database)
            create_database(cursor, args.database)

    with connect_mysql(args, args.database) as conn:
        with conn.cursor() as cursor:
            if args.reset:
                cursor.execute(f"DROP TABLE IF EXISTS `{ALL_TYPES_TABLE}`")
            create_table(cursor)
            cursor.execute(f"TRUNCATE TABLE `{ALL_TYPES_TABLE}`")
            insert_sample(cursor)

    print(
        f"Sample database '{args.database}' and table '{ALL_TYPES_TABLE}' are ready with 1 row of data."
    )


if __name__ == "__main__":
    main()
