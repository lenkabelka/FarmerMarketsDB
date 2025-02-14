import database_creator as creator
import database_from_csv_fill as fill

creator.create_database()
creator.create_tables_in_database()

fill.fill_database_from_csv()