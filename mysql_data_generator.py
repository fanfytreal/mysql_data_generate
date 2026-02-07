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

    insert_sql = f"""
    INSERT INTO `{ALL_TYPES_TABLE}` (
        tinyint_col,
        smallint_col,
        mediumint_col,
        int_col,
        bigint_col,
        decimal_col,
        float_col,
        double_col,
        bit_col,
        boolean_col,
        date_col,
        datetime_col,
        timestamp_col,
        time_col,
        year_col,
        char_col,
        varchar_col,
        tinytext_col,
        text_col,
        mediumtext_col,
        longtext_col,
        binary_col,
        varbinary_col,
        tinyblob_col,
        blob_col,
        mediumblob_col,
        longblob_col,
        enum_col,
        set_col,
        json_col,
        geometry_col,
        point_col,
        linestring_col,
        polygon_col,
        multipoint_col,
        multilinestring_col,
        multipolygon_col,
        geometrycollection_col
    ) VALUES (
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        b'10101010',
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        UNHEX(%s),
        UNHEX(%s),
        UNHEX(%s),
        UNHEX(%s),
        UNHEX(%s),
        UNHEX(%s),
        %s,
        %s,
        %s,
        ST_GeomFromText(%s),
        ST_GeomFromText(%s),
        ST_GeomFromText(%s),
        ST_GeomFromText(%s),
        ST_GeomFromText(%s),
        ST_GeomFromText(%s),
        ST_GeomFromText(%s)
    )
    """

    cursor.execute(
        insert_sql,
        (
            12,
            32000,
            64000,
            214748,
            922337203,
            "12345.67",
            3.14,
            2.7182818,
            True,
            now.date(),
            now,
            now,
            now.time(),
            2024,
            "char-data",
            "varchar-data",
            "tiny text",
            "text data",
            "medium text data",
            "long text data",
            "00FF00FF00FF00FF00FF00FF00FF00FF",
            "ABCD1234",
            "DEADBEEF",
            "BLOB00FF",
            "CAFEBABE",
            "FADEFADE",
            "red",
            "alpha,beta",
            json_payload,
            "POINT(0 0)",
            "POINT(1 1)",
            "LINESTRING(0 0, 1 1, 2 2)",
            "POLYGON((0 0, 0 1, 1 1, 1 0, 0 0))",
            "MULTIPOINT(0 0, 1 1)",
            "MULTILINESTRING((0 0, 1 1), (2 2, 3 3))",
            "MULTIPOLYGON(((0 0, 0 1, 1 1, 1 0, 0 0)))",
            "GEOMETRYCOLLECTION(POINT(1 1), LINESTRING(0 0, 2 2))",
        ),
    )


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
