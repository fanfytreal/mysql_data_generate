# MySQL Data Generator

This repository provides a Python script that connects to a MySQL instance and generates a sample database/table that covers common MySQL data types. The generated table includes numeric, date/time, string, binary, JSON, and spatial types, helping you avoid missing field types in test data.

## Requirements

- Python 3.10+
- MySQL 5.7+ (for JSON support; MySQL 8+ recommended)

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

```bash
python mysql_data_generator.py --host 127.0.0.1 --port 3306 --user root --password yourpass --database sample_all_types
```

To reset (drop/recreate) the database and table:

```bash
python mysql_data_generator.py --host 127.0.0.1 --port 3306 --user root --password yourpass --database sample_all_types --reset
```

Environment variables are also supported:

- `MYSQL_HOST`
- `MYSQL_PORT`
- `MYSQL_USER`
- `MYSQL_PASSWORD`
- `MYSQL_DATABASE`

## Output

The script creates a database (default: `sample_all_types`), a table named `all_mysql_types`, and inserts one row with sample values covering MySQL data types.
