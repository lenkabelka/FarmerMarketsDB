import json
import psycopg2


def load_config():
    with open('config.json', 'r') as config_file:
        return json.load(config_file)


def db_connect(config):
    return psycopg2.connect(**config)


def show_all_markets_GUI():

    rows = []
    try:
        config = load_config()
        conn = db_connect(config)
        cur = conn.cursor()

        cur.execute("SELECT y, x, market_name FROM markets.markets WHERE x IS NOT NULL AND y IS NOT NULL;")

        rows = cur.fetchall()
        print(type(rows))
        print(rows)

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

    return rows


def get_information_about_market_by_fmid(fmid):

    lat_lon_name_dict = []
    row_dict = {}
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

        cur.execute("SELECT x, y, market_name FROM markets.markets "
                    "WHERE x IS NOT NULL AND y IS NOT NULL AND fmid = %s;", (fmid,))

        lat_lon_name_dict = cur.fetchall()

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

    return row_dict, lat_lon_name_dict


def get_markets_fmids():

    fmids = []
    try:
        config = load_config()
        conn = db_connect(config)
        cur = conn.cursor()
        cur.execute("SELECT fmid FROM markets.markets")

        fmids = [' '.join(map(str, tpl)) for tpl in cur.fetchall()]

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error occurred: {e}")

    return fmids


def get_products():

    products = []
    try:
        config = load_config()
        conn = db_connect(config)
        cur = conn.cursor()
        cur.execute("SELECT product_name FROM markets.products")

        products = [' '.join(map(str, tpl)) for tpl in cur.fetchall()]

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error occurred: {e}")

    return products

def get_payment_methods():

    payment_methods = []
    try:
        config = load_config()
        conn = db_connect(config)
        cur = conn.cursor()
        cur.execute("SELECT payment_method FROM markets.payment_methods")

        payment_methods = [' '.join(map(str, tpl)) for tpl in cur.fetchall()]

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error occurred: {e}")

    return payment_methods

def get_cities():

    cities = []
    try:
        config = load_config()
        conn = db_connect(config)
        cur = conn.cursor()
        cur.execute("SELECT city_name FROM markets.cities")

        cities = [' '.join(map(str, tpl)) for tpl in cur.fetchall()]
        cities = sorted(cities)

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error occurred: {e}")

    return cities


def get_countries():

    countries = []
    try:
        config = load_config()
        conn = db_connect(config)
        cur = conn.cursor()
        cur.execute("SELECT country_name FROM markets.countries")

        countries = [' '.join(map(str, tpl)) for tpl in cur.fetchall()]
        countries = sorted(countries)

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error occurred: {e}")

    return countries


def get_states():

    states = []
    try:
        config = load_config()
        conn = db_connect(config)
        cur = conn.cursor()
        cur.execute("SELECT state_name FROM markets.states")

        states = [' '.join(map(str, tpl)) for tpl in cur.fetchall()]
        states = sorted(states)

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error occurred: {e}")

    return states


def get_markets_in_city(city_name):

    markets = []
    try:
        config = load_config()
        conn = db_connect(config)
        cur = conn.cursor()
        #cur.execute("SELECT market_name FROM markets.markets WHERE city = %s;", (city_name,))

        cur.execute("SELECT markets.market_name FROM markets.markets "
                    "JOIN markets.market_city ON markets.markets.fmid = markets.market_city.fmid "
                    "JOIN markets.cities ON markets.market_city.city_id = markets.cities.city_id "
                    "WHERE markets.cities.city_name = %s;", (city_name,))
        print(city_name)
        markets = [' '.join(map(str, tpl)) for tpl in cur.fetchall()]
        print(markets)

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error occurred: {e}")

    return markets


def get_lat_lon(market_name):

    lat_lon = []
    try:
        config = load_config()
        conn = db_connect(config)
        cur = conn.cursor()
        #cur.execute("SELECT x, y FROM markets.markets WHERE x IS NOT NULL AND y")

        cur.execute("SELECT markets.y, markets.x FROM markets.markets "
                    "JOIN markets.market_city ON markets.markets.fmid = markets.market_city.fmid "
                    "JOIN markets.cities ON markets.market_city.city_id = markets.cities.city_id "
                    "WHERE markets.x IS NOT NULL AND markets.y IS NOT NULL "
                    "AND markets.markets.market_name = %s;", (market_name,))

        lat_lon = [' '.join(map(str, tpl)) for tpl in cur.fetchall()]
        print(lat_lon)

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error occurred: {e}")

    return lat_lon