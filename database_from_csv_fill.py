import queries_to_database as query
from pathlib import Path


def fill_database_from_csv():

    relative_path = Path("DB_Farmer_Markets/markets_table.csv")
    absolute_path = relative_path.resolve()
    table_name = "markets.markets"
    columns = ['fmid', 'market_name', 'website', 'facebook', 'twitter', 'youtube',
               'other_media', 'zip', 'state', 'country', 'city', 'street', 'x', 'y',
               'Season1Date', 'Season1Time', 'Season2Date', 'Season2Time',
               'Season3Date', 'Season3Time', 'Season4Date', 'Season4Time']
    query.fill_dbtable_from_csvfile(absolute_path, table_name, columns)

    relative_path = Path("DB_Farmer_Markets/products_table.csv")
    absolute_path = relative_path.resolve()
    table_name = "markets.products"
    columns = ['product_name']
    query.fill_dbtable_from_csvfile(absolute_path, table_name, columns)

    relative_path = Path("DB_Farmer_Markets/payment_methods_table.csv")
    absolute_path = relative_path.resolve()
    table_name = "markets.payment_methods"
    columns = ['payment_method']
    query.fill_dbtable_from_csvfile(absolute_path, table_name, columns)

    relative_path = Path("DB_Farmer_Markets/markets_payment_methods_table.csv")
    absolute_path = relative_path.resolve()
    table_name = "markets.markets_payment_methods"
    columns = ['fmid', 'payment_method_id']
    query.fill_dbtable_from_csvfile(absolute_path, table_name, columns)

    relative_path = Path("DB_Farmer_Markets/markets_products_table.csv")
    absolute_path = relative_path.resolve()
    table_name = "markets.markets_products"
    columns = ['fmid', 'product_id']
    query.fill_dbtable_from_csvfile(absolute_path, table_name, columns)