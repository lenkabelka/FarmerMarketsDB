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

list_of_columns = [0, 1, 2, 3, 4, 5, 6, 11, 10, 9, 8, 7, 20, 21, 12, 13, 14, 15, 16, 17, 18, 19]
parser.make_csvfile_for_loading_in_database(absolute_path_to_source_csvfile,
                                            path_to_temp_new_csvfile,
                                            list_of_columns)

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
                                            list_of_columns)

relative_path_to_source_csvfile = Path("DB_Farmer_Markets/temp_products.csv")
absolute_path_to_source_csvfile = relative_path_to_source_csvfile.resolve()
path_to_new_csvfile = source_directory / "markets_products_table.csv"
parser.make_csv_file_for_many_to_many_table(absolute_path_to_source_csvfile, path_to_new_csvfile)


list_of_columns = [0, 23, 24, 25, 26, 27]
path_to_temp_new_csvfile = source_directory / "temp_payment_methods.csv"
parser.make_csvfile_for_loading_in_database(absolute_path_to_source_csvfile,
                                            path_to_temp_new_csvfile,
                                            list_of_columns)

relative_path_to_source_csvfile = Path("DB_Farmer_Markets/temp_payment_methods.csv")
absolute_path_to_source_csvfile = relative_path_to_source_csvfile.resolve()
path_to_new_csvfile = source_directory / "markets_payment_methods_table.csv"
parser.make_csv_file_for_many_to_many_table(absolute_path_to_source_csvfile, path_to_new_csvfile)