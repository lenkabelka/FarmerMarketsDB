import json
import psycopg2
import bcrypt


def load_config():
    with open('config.json', 'r') as config_file:
        return json.load(config_file)


def db_connect(config):
    return psycopg2.connect(**config)

def get_markets_names(*, product_name = None,
                      payment_method=None,
                      state_name=None,
                      country_name=None,
                      city_name=None, fmid=None,
                      all_markets_names=None):
    markets_name = []
    try:
        config = load_config()
        conn = db_connect(config)
        cur = conn.cursor()

        if state_name:
            cur.execute("SELECT markets.fmid, markets.market_name FROM markets.markets "
                        "JOIN markets.market_state ON markets.markets.fmid = markets.market_state.fmid "
                        "JOIN markets.states ON markets.market_state.state_id = markets.states.state_id "
                        "WHERE markets.states.state_name = %s;", (state_name,))
        elif country_name:
            cur.execute("SELECT markets.fmid, markets.market_name FROM markets.markets "
                        "JOIN markets.market_country ON markets.markets.fmid = markets.market_country.fmid "
                        "JOIN markets.countries ON markets.market_country.country_id = markets.countries.country_id "
                        "WHERE markets.countries.country_name = %s;", (country_name,))
        elif city_name:
            cur.execute("SELECT markets.fmid, markets.market_name FROM markets.markets "
                        "JOIN markets.market_city ON markets.markets.fmid = markets.market_city.fmid "
                        "JOIN markets.cities ON markets.market_city.city_id = markets.cities.city_id "
                        "WHERE markets.cities.city_name = %s;", (city_name,))
        elif fmid:
            cur.execute("SELECT markets.fmid, market_name FROM markets.markets WHERE fmid = %s;", (fmid,))
        elif product_name:
            cur.execute("SELECT markets.fmid, markets.market_name FROM markets.markets "
                        "JOIN markets.markets_products ON markets.markets.fmid = markets.markets_products.fmid "
                        "JOIN markets.products ON markets.markets_products.product_id = markets.products.product_id "
                        "WHERE markets.products.product_name = %s;", (product_name,))
        elif payment_method:
            cur.execute("SELECT markets.fmid, markets.market_name FROM markets.markets "
                        "JOIN markets.markets_payment_methods ON markets.markets.fmid = markets.markets_payment_methods.fmid "
                        "JOIN markets.payment_methods ON markets.markets_payment_methods.payment_method_id = markets.payment_methods.payment_method_id "
                        "WHERE markets.payment_methods.payment_method = %s;", (payment_method,))
        elif all_markets_names == "all_markets_names":
            cur.execute("SELECT fmid, market_name FROM markets.markets;")
        else:
            raise ValueError("Error: Specify one of the parameters - state_name, country_name, city_name or fmid")

        for i in cur.fetchall():
            markets_name.append(f"{i[1]}  __fmid: {i[0]}")

        markets_name.sort()

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error occurred: {e}")

    return markets_name


def get_lat_lon(*, product_name = None,
                payment_method=None,market_name=None,
                state_name=None, country_name=None,
                city_name=None, fmid=None,
                all_markets_names=None):

    lat_lon = []
    try:
        config = load_config()
        conn = db_connect(config)
        cur = conn.cursor()

        if market_name:
            cur.execute("SELECT markets.y, markets.x FROM markets.markets "
                        "JOIN markets.market_city ON markets.markets.fmid = markets.market_city.fmid "
                        "JOIN markets.cities ON markets.market_city.city_id = markets.cities.city_id "
                        "WHERE markets.x IS NOT NULL AND markets.y IS NOT NULL "
                        "AND markets.markets.market_name = %s;", (market_name,))
        elif city_name:
            cur.execute("SELECT markets.y, markets.x FROM markets.markets "
                        "JOIN markets.market_city ON markets.markets.fmid = markets.market_city.fmid "
                        "JOIN markets.cities ON markets.market_city.city_id = markets.cities.city_id "
                        "WHERE markets.x IS NOT NULL AND markets.y IS NOT NULL "
                        "AND markets.cities.city_name = %s;", (city_name,))
        elif state_name:
            cur.execute("SELECT markets.y, markets.x FROM markets.markets "
                        "JOIN markets.market_state ON markets.markets.fmid = markets.market_state.fmid "
                        "JOIN markets.states ON markets.market_state.state_id = markets.states.state_id "
                        "WHERE markets.x IS NOT NULL AND markets.y IS NOT NULL "
                        "AND markets.states.state_name = %s;", (state_name,))
        elif country_name:
            cur.execute("SELECT markets.y, markets.x FROM markets.markets "
                        "JOIN markets.market_country ON markets.markets.fmid = markets.market_country.fmid "
                        "JOIN markets.countries ON markets.market_country.country_id = markets.countries.country_id "
                        "WHERE markets.x IS NOT NULL AND markets.y IS NOT NULL "
                        "AND markets.countries.country_name = %s;", (country_name,))
        elif fmid:
            cur.execute("SELECT y, x FROM markets.markets "
                        "WHERE x IS NOT NULL AND y IS NOT NULL AND fmid = %s;", (fmid,))
        elif product_name:
            cur.execute("SELECT markets.y, markets.x FROM markets.markets "
                        "JOIN markets.markets_products ON markets.markets.fmid = markets.markets_products.fmid "
                        "JOIN markets.products ON markets.markets_products.product_id = markets.products.product_id "
                        "WHERE markets.x IS NOT NULL AND markets.y IS NOT NULL "
                        "AND markets.products.product_name = %s;", (product_name,))
        elif payment_method:
            cur.execute("SELECT markets.y, markets.x FROM markets.markets "
                        "JOIN markets.markets_payment_methods ON markets.markets.fmid = markets.markets_payment_methods.fmid "
                        "JOIN markets.payment_methods ON markets.markets_payment_methods.payment_method_id = markets.payment_methods.payment_method_id "
                        "WHERE markets.x IS NOT NULL AND markets.y IS NOT NULL "
                        "AND markets.payment_methods.payment_method = %s;", (payment_method,))
        elif all_markets_names == "all_markets":
            cur.execute("SELECT y, x FROM markets.markets WHERE x IS NOT NULL AND y IS NOT NULL;")
        else:
            raise ValueError("Error: Specify one of the parameters - market_name, state_name, country_name, city_name or fmid")

        lat_lon = cur.fetchall()

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error occurred: {e}")

    return lat_lon


def get_information_about_market_by_fmid(fmid):

    info_about_market = []
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
                info_about_market.append(f"{key}:___ {value}")
                print(f"{key}:___ {value}")

        cur.execute("SELECT x, y, market_name FROM markets.markets "
                    "WHERE x IS NOT NULL AND y IS NOT NULL AND fmid = %s;", (fmid,))

        lat_lon_name_dict = cur.fetchall()

        print(info_about_market)

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

    return info_about_market


def get_fmids():

    fmids = []
    try:
        config = load_config()
        conn = db_connect(config)
        cur = conn.cursor()
        cur.execute("SELECT fmid FROM markets.markets")

        fmids = [' '.join(map(str, tpl)) for tpl in cur.fetchall()]
        fmids.sort()

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
        products.sort()

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
        payment_methods.sort()

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
        cities.sort()

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
        countries.sort()

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
        states.sort()

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error occurred: {e}")

    return states


def save_user(login, password):

    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password.encode(), salt).decode()

    config = load_config()
    conn = db_connect(config)
    try:
        cur = conn.cursor()

        cur.execute("SELECT 1 FROM markets.users WHERE user_nickname = %s", (login,))
        exists = cur.fetchone()

        if exists:
            print("This login is busy")
        else:
            cur.execute("INSERT INTO markets.users (user_nickname, password_hash) VALUES (%s, %s)", (login, password_hash))
            conn.commit()
            print("User saved successfully!")

        cur.close()
        conn.close()

    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()


def is_user_in_DB(user_name, password):

    try:
        config = load_config()
        with db_connect(config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM markets.users "
                            "WHERE user_nickname = %s", (user_name,))

                user = cur.fetchone()

                if user is None:
                    return False

                return bcrypt.checkpw(password.encode(), user[2].encode())

    except Exception as e:
        print(f"Error: {e}")
        return False


def get_info_about_market_by_market_name(market_name): #market_name is QListItem
    try:
        market_name = market_name.text()
        config = load_config()
        with db_connect(config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM markets.markets "
                            "WHERE market_name = %s", (market_name,))
                market = cur.fetchone()

    except Exception as e:
        print(f"Error: {e}")