from pathlib import Path
import csv_parser as parser


#0. FMID, 1. MarketName, 2. Website, 3. Facebook, 4. Twitter, 5. Youtube, 6. OtherMedia, 7. street, 8. city, 9. County, 10. State, 11. zip,
# 12. Season1Date, 13. Season1Time, 14. Season2Date, 15. Season2Time, 16. Season3Date, 17. Season3Time, 18. Season4Date, 19. Season4Time,
# 20. x, 21. y, 22. Location, 23. Credit, 24. WIC, 25. WICcash, 26. SFMNP, 27. SNAP, 28. Organic, 29. Bakedgoods, 30. Cheese, 31. Crafts,
# 32. Flowers, 33. Eggs, 34. Seafood, 35. Herbs, 36. Vegetables, 37. Honey, 38. Jams, 39. Maple, 40. Meat, 41. Nursery, 42. Nuts, 43. Plants,
# 44. Poultry, 45. Prepared, 46. Soap, 47. Trees, 48. Wine, 49. Coffee, 50. Beans, 51. Fruits, 52. Grains, 53. Juices, 54. Mushrooms,
# 55. PetFood, 56. Tofu, 57. WildHarvested, 58. updateTime

path = Path("DB_Farmer_Markets")
if path.is_dir():
    pass
else:
    Path("DB_Farmer_Markets").mkdir()

relative_path_to_source_csvfile = Path("Export.csv")
absolute_path_to_source_csvfile = relative_path_to_source_csvfile.resolve()
source_directory = Path("DB_Farmer_Markets")
#source_directory = relative_path_to_source_csvfile.parent
path_to_temp_new_csvfile = source_directory / "markets_table_with_duplicates.csv"

list_of_columns = [0, 1, 2, 3, 4, 5, 6, 11, 7, 20, 21]
parser.make_csvfile_for_loading_in_database(absolute_path_to_source_csvfile,
                                            path_to_temp_new_csvfile,
                                            list_of_columns, True)

relative_path_to_csvfile_with_duplicates = Path("DB_Farmer_Markets/markets_table_with_duplicates.csv")
absolute_path_to_csvfile_with_duplicates = relative_path_to_csvfile_with_duplicates.resolve()
path_to_new_csvfile = source_directory / "markets_table.csv"
parser.remove_duplicates_in_csvfile(absolute_path_to_csvfile_with_duplicates, path_to_new_csvfile, 0)

path_to_new_csvfile = source_directory / "products_table.csv"
list_of_columns = [28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57]
parser.make_new_csvfile_from_header_source_scv(absolute_path_to_source_csvfile,
                                               path_to_new_csvfile,
                                               list_of_columns)

path_to_new_csvfile = source_directory / "payment_methods_table.csv"
list_of_columns = [23, 24, 25, 26, 27]
parser.make_new_csvfile_from_header_source_scv(absolute_path_to_source_csvfile,
                                               path_to_new_csvfile,
                                               list_of_columns)


list_of_columns = [0, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57]
path_to_temp_new_csvfile = source_directory / "temp_products.csv"
parser.make_csvfile_for_loading_in_database(absolute_path_to_source_csvfile,
                                            path_to_temp_new_csvfile,
                                            list_of_columns, True)


relative_path_to_source_csvfile = Path("DB_Farmer_Markets/temp_products.csv")
absolute_path_to_source_csvfile = relative_path_to_source_csvfile.resolve()
path_to_new_csvfile = source_directory / "markets_products_table.csv"
parser.make_csv_file_for_many_to_many_table(absolute_path_to_source_csvfile, path_to_new_csvfile)


list_of_columns = [0, 23, 24, 25, 26, 27]
path_to_temp_new_csvfile = source_directory / "temp_payment_methods.csv"
parser.make_csvfile_for_loading_in_database(absolute_path_to_source_csvfile,
                                            path_to_temp_new_csvfile,
                                            list_of_columns, True)

relative_path_to_source_csvfile = Path("DB_Farmer_Markets/temp_payment_methods.csv")
absolute_path_to_source_csvfile = relative_path_to_source_csvfile.resolve()
path_to_new_csvfile = source_directory / "markets_payment_methods_table.csv"
parser.make_csv_file_for_many_to_many_table(absolute_path_to_source_csvfile, path_to_new_csvfile)



#######################################################################################################

relative_path_to_source_csvfile = Path("Export.csv")

fmid_cities_with_duplicates_with_none_with_multiple_values = source_directory / "fmid_cities_with_duplicates_with_none_with_multiple_values.csv"
list_of_columns = [0, 8]
parser.make_csvfile_for_loading_in_database(relative_path_to_source_csvfile,
                                            fmid_cities_with_duplicates_with_none_with_multiple_values,
                                            list_of_columns, True)

fmid_cities_with_duplicates_with_none = source_directory / "fmid_cities_with_duplicates_with_none.csv"
parser.find_rows_with_multiple_values(fmid_cities_with_duplicates_with_none_with_multiple_values, fmid_cities_with_duplicates_with_none)

fmid_cities_with_duplicates_without_none = source_directory / "fmid_cities_with_duplicates_without_none.csv"
parser.remove_empty_row_from_column(fmid_cities_with_duplicates_with_none, fmid_cities_with_duplicates_without_none, 1)

fmid_city_without_duplicates = source_directory / "fmid_city_without_duplicates.csv"
parser.remove_duplicates_in_csvfile(fmid_cities_with_duplicates_with_none, fmid_city_without_duplicates, 1)

fmid_city = source_directory / "fmid_city.csv" #without_none
parser.remove_empty_row_from_column(fmid_city_without_duplicates, fmid_city, 1)


list_of_columns = [1]
cities = source_directory / "cities.csv"
parser.make_csvfile_for_loading_in_database(fmid_city,
                                       cities,
                                       list_of_columns, False)

#make cities with id
cities_with_id = source_directory / "cities_with_id.csv"
parser.add_id_from_1(cities, cities_with_id)

#make many-to-many fmid-city_id
a = source_directory / "fmid_cities_with_duplicates_without_none.csv"
b = source_directory / "cities_with_id.csv"
c = source_directory / "fmid_city_id.csv"
parser.make_many_to_many_table_from_two_csvfiles(a,
                                            1,
                                            0,
                                            b,
                                            1,
                                            0,
                                            c)

#make fmid_country, countries
list_of_columns = [0, 9]
fmid_countries_with_duplicates_with_none = source_directory / "fmid_country_with_duplicates_with_none.csv"
parser.make_csvfile_for_loading_in_database(relative_path_to_source_csvfile,
                                            fmid_countries_with_duplicates_with_none,
                                            list_of_columns, True)

fmid_countries_with_duplicates_without_none = source_directory / "fmid_countries_with_duplicates_without_none.csv"
parser.remove_empty_row_from_column(fmid_countries_with_duplicates_with_none, fmid_countries_with_duplicates_without_none, 1)

fmid_country_without_duplicates = source_directory / "fmid_country_without_duplicates.csv"
parser.remove_duplicates_in_csvfile(fmid_countries_with_duplicates_with_none, fmid_country_without_duplicates, 1)

fmid_country = source_directory / "fmid_country.csv" #without none
parser.remove_empty_row_from_column(fmid_country_without_duplicates, fmid_country, 1)

list_of_columns = [1]
countries = source_directory / "countries.csv"
parser.make_csvfile_for_loading_in_database(fmid_country,
                                            countries,
                                            list_of_columns, False)

#make countries with id
countries_with_id = source_directory / "countries_with_id.csv"
parser.add_id_from_1(countries, countries_with_id)

#make many-to-many fmid-country_id
a = source_directory / "fmid_countries_with_duplicates_without_none.csv"
b = source_directory / "countries_with_id.csv"
c = source_directory / "fmid_country_id.csv"
parser.make_many_to_many_table_from_two_csvfiles(a,
                                            1,
                                            0,
                                            b,
                                            1,
                                            0,
                                            c)


#make fmid-state, states
list_of_columns = [0, 10]
fmid_state_with_duplicates_with_none = source_directory / "fmid_state_with_duplicates_with_none.csv"
parser.make_csvfile_for_loading_in_database(relative_path_to_source_csvfile,
                                            fmid_state_with_duplicates_with_none,
                                            list_of_columns, True)

fmid_states_with_duplicates_without_none = source_directory / "fmid_states_with_duplicates_without_none.csv"
parser.remove_empty_row_from_column(fmid_state_with_duplicates_with_none, fmid_states_with_duplicates_without_none, 1)

fmid_state_without_duplicates = source_directory / "fmid_state_without_duplicates.csv"
parser.remove_duplicates_in_csvfile(fmid_state_with_duplicates_with_none, fmid_state_without_duplicates, 1)

fmid_state = source_directory / "fmid_state.csv" #without none
parser.remove_empty_row_from_column(fmid_state_without_duplicates, fmid_state, 1)

list_of_columns = [1]
states = source_directory / "states.csv"
parser.make_csvfile_for_loading_in_database(fmid_state,
                                            states,
                                            list_of_columns, False)

states_with_id = source_directory / "states_with_id.csv"
parser.add_id_from_1(states, states_with_id)


#make many-to-many fmid-state_id
a = source_directory / "fmid_states_with_duplicates_without_none.csv"
b = source_directory / "states_with_id.csv"
c = source_directory / "fmid_state_id.csv"
parser.make_many_to_many_table_from_two_csvfiles(a,
                                            1,
                                            0,
                                            b,
                                            1,
                                            0,
                                            c)