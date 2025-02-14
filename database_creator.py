from pathlib import Path
import json
import psycopg2

def load_config():
    relative_path_to_config = Path("config.json")
    absolute_path_to_config = relative_path_to_config.resolve()
    with open(absolute_path_to_config, 'r') as config_file:
        return json.load(config_file)


def db_connect(config):
    return psycopg2.connect(
        dbname="postgres",
        user=config["user"],
        password=config["password"],
        host=config["host"],
        port=config["port"]
    )


def create_database():
    try:
        config = load_config()
        db_name = config["database"]

        conn = db_connect(config)
        conn.autocommit = True

        cur = conn.cursor()
        cur.execute(f"CREATE DATABASE {db_name};")

        cur.close()
        conn.close()

        print(f"Database '{db_name}' created successfully")
    except Exception as e:
        print(f"Error: {e}")


def create_tables_in_database():
    config = load_config()
    conn = psycopg2.connect(
        dbname=config["database"],
        user=config["user"],
        password=config["password"],
        host=config["host"],
        port=config["port"]
    )

    try:
        relative_path_to_sql = Path("create_farmer_markets_db.sql")
        absolute_path_to_sql = relative_path_to_sql.resolve()

        with open(absolute_path_to_sql, 'r') as sql_file:
            sql_script = sql_file.read()

        with conn.cursor() as cur:
            cur.execute(sql_script)

            conn.commit()
            cur.close()
            conn.close()
            print("Tables created successfully!")
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()