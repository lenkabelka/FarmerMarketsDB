import csv
import argparse
import json
import psycopg2


def load_config():
    with open('config.json', 'r') as config_file:
        return json.load(config_file)


def db_connect(config):
    return psycopg2.connect(**config)


def fill_dbtable_from_csvfile(path_to_csvfile, table_name, columns):
    """
    Function to insert data from a CSV into a PostgreSQL table.

    Args:
        path_to_csvfile: Path to the CSV file
        table_name: Name of the table where data will be inserted
        columns: List of column names that match the order in CSV
    """

    config = load_config()
    conn = db_connect(config)
    try:
        cur = conn.cursor()

        with open(path_to_csvfile, mode='r') as csvfile:
            reader = csv.reader(csvfile)
            columns_str = ', '.join(columns)
            values_placeholder = ', '.join(['%s'] * len(columns))

            for row in reader:
                row = [value if value != '' else None for value in row]
                insert_query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({values_placeholder})"
                cur.execute(insert_query, tuple(row))

        conn.commit()
        cur.close()
        conn.close()
        print("Data inserted successfully!")
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()


def show_all_markets():

    try:
        config = load_config()
        conn = db_connect(config)
        cur = conn.cursor()

        cur.execute("SELECT fmid, market_name FROM markets.markets;")

        for row in cur:
            print(f"Name of market: {row[1]} ______ FMID: {row[0]}")

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")


def get_information_about_market_by_fmid(fmid):

    try:
        config = load_config()
        conn = db_connect(config)
        cur = conn.cursor()

        cur.execute("SELECT * FROM markets.markets WHERE fmid = %s;", (fmid,))
        name_of_columns = [column[0] for column in cur.description]  # column[0], 0 - name of column

        for row in cur:
            row_dict = {name_of_columns[i]: row[i] for i in range(len(row)) if row[i] is not None}
            for key, value in row_dict.items():
                print(f"{key}:___ {value}")

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")


def get_markets_in_city(city_name):

    try:
        config = load_config()
        conn = db_connect(config)
        cur = conn.cursor()
        cur.execute("SELECT market_name FROM markets.markets WHERE city = %s;", (city_name,))

        for row in cur:
            print(', '.join(row))

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error occurred: {e}")


def get_markets_by_product(product_name):

    try:
        config = load_config()
        conn = db_connect(config)
        cur = conn.cursor()
        cur.execute("SELECT markets.market_name FROM markets.markets "
                    "JOIN markets.markets_products ON markets.markets.fmid = markets.markets_products.fmid "
                    "JOIN markets.products ON markets.markets_products.product_id = markets.products.product_id "
                    "WHERE markets.products.product_name = %s;", (product_name,))

        for row in cur:
            print(', '.join(row))

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error occurred: {e}")


def get_markets_by_payment_method(payment_method):

    try:
        config = load_config()
        conn = db_connect(config)
        cur = conn.cursor()

        cur.execute("SELECT markets.market_name FROM markets.markets "
                    "JOIN markets.markets_payment_methods ON markets.markets.fmid = markets.markets_payment_methods.fmid "
                    "JOIN markets.payment_methods ON markets.markets_payment_methods.payment_method_id = markets.payment_methods.payment_method_id "
                    "WHERE markets.payment_methods.payment_method = %s;", (payment_method,))

        for row in cur:
            print(', '.join(row))

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error occurred: {e}")


def get_information_about_markets():

    # Dictionary of possible commands for command line:
    possible_args_for_command_line = {
        "show_all_markets": show_all_markets,
        "get_information_about_market_by_fmid": get_information_about_market_by_fmid,
        "get_markets_in_city": get_markets_in_city,
        "get_markets_by_product": get_markets_by_product,
        "get_markets_by_payment_method": get_markets_by_payment_method
    }

    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices = possible_args_for_command_line.keys(), help="Choose a command to execute.")

    parser.add_argument("--fmid", nargs="?", help="FMID to get information about market")
    parser.add_argument("--city", help="markets in a city")
    parser.add_argument("--product", help="markets by product")
    parser.add_argument("--payment_method", help="markets by payment method")
    args = parser.parse_args()


    if args.command == "show_all_markets":
        possible_args_for_command_line[args.command]()
    elif args.command == "get_information_about_market_by_fmid" and args.fmid:
        get_information_about_market_by_fmid(args.fmid)
    elif args.command == "get_markets_in_city" and args.city:
        get_markets_in_city(args.city)
    elif args.command == "get_markets_by_product" and args.product:
        get_markets_by_product(args.product)
    elif args.command == "get_markets_by_payment_method" and args.payment_method:
        get_markets_by_payment_method(args.payment_method)



if __name__ == "__main__":
    get_information_about_markets()