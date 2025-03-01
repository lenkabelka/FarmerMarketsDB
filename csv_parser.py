import csv
from pathlib import Path


def make_csvfile_for_loading_in_database(path_to_source_csvfile,
                                         path_to_new_csvfile,
                                         list_of_columns, is_header):

    """
    Creates a new CSV file from an existing one, including only the specified columns.

    Parameters:
    - path_to_source_csvfile (str): Path to the original CSV file.
    - path_to_new_csvfile (str): Path to save the new CSV file.
    - list_of_columns (list of int): List of column indices (0-based) to be included in the new CSV file.

    The function reads the source CSV file, extracts only the specified columns (by index),
    and writes the data to a new CSV file without a header.
    """

    if path_to_new_csvfile.exists():
        path_to_new_csvfile.unlink()

    ls = []
    with open(path_to_source_csvfile, mode='r', newline='') as source_file:
        reader = csv.reader(source_file)
        if is_header:
            next(reader)

        with open(path_to_new_csvfile, mode='a', newline='') as new_file:
            writer = csv.writer(new_file)
            for row in reader:
                row_for_new_csv = []
                counter = 0
                while counter < len(list_of_columns):
                    row_for_new_csv.append(row[list_of_columns[counter]])
                    counter += 1
                writer.writerow(row_for_new_csv)

    return ls


def remove_duplicates_in_csvfile(path_to_input_csvfile,
                                 path_to_output_csvfile,
                                 number_of_column_with_unique_data):

    """
    Removes duplicate rows based on a specific column in a CSV file.

    Parameters:
    - path_to_input_csvfile (str): Path to the input CSV file.
    - path_to_output_csvfile (str): Path to save the cleaned CSV file.
    - number_of_column_with_unique_data (int): Index of the column (0-based) that should contain unique values.

    The function reads the input CSV file, removes duplicate rows based on the specified column,
    and writes the cleaned data to a new CSV file while preserving the original order of appearance.
    """

    if path_to_output_csvfile.exists():
        path_to_output_csvfile.unlink()

    seen_rows = set()
    with open(path_to_input_csvfile, mode='r', newline='') as in_csvfile:
        reader = csv.reader(in_csvfile)

        with open(path_to_output_csvfile, mode='a', newline='') as out_csvfile:
            writer = csv.writer(out_csvfile)

            for row in reader:
                key = row[number_of_column_with_unique_data]
                if key not in seen_rows:
                    seen_rows.add(key)
                    writer.writerow(row)


def remove_empty_row_from_column(path_to_input_csvfile, path_to_output_csvfile, number_of_column):

    """
    Removes rows from a CSV file where the specified column is empty.

    Parameters:
    path_to_input_csvfile (str): Path to the input CSV file.
    path_to_output_csvfile (str): Path to save the output CSV file with non-empty rows.
    number_of_column (int): The index of the column to check for empty values (0-based index).

    The function reads the input CSV file, filters out rows where the specified column is empty,
    and writes the cleaned data to the output CSV file.
    """

    if path_to_output_csvfile.exists():
        path_to_output_csvfile.unlink()

    with open(path_to_input_csvfile, mode='r', newline='') as in_csvfile:
        reader = csv.reader(in_csvfile)

        with open(path_to_output_csvfile, mode='a', newline='') as out_csvfile:
            writer = csv.writer(out_csvfile)

            for row in reader:
                if not row[number_of_column] or all(not cell.strip() for cell in row[number_of_column]):
                    continue
                else:
                    writer.writerow(row)


def add_id_from_1(path_to_input_csvfile, path_to_output_csvfile):

    """
    Adds a unique ID to each row in a CSV file, starting from 1.

    Parameters:
    path_to_input_csvfile (str): Path to the input CSV file.
    path_to_output_csvfile (str): Path to save the output CSV file with added IDs.

    The function reads the input CSV file, adds an incremental ID as the first column
    (starting from 1), and writes the modified data to the output CSV file.
    """

    if path_to_output_csvfile.exists():
        path_to_output_csvfile.unlink()

    with open(path_to_input_csvfile, mode='r', newline='') as in_csvfile:
        reader = csv.reader(in_csvfile)

        with open(path_to_output_csvfile, mode='a', newline='') as out_csvfile:
            writer = csv.writer(out_csvfile)

            counter = 1
            new_row = []
            for row in reader:
                new_row.append(counter)
                temp_row = ",".join(row)
                new_row.append(temp_row)
                #print(new_row)
                writer.writerow(new_row)
                counter += 1
                new_row = []


def make_many_to_many_table_from_two_csvfiles(csvfile_one,
                                              column_to_compare_one,
                                              column_with_id_one,
                                              csvfile_two,
                                              column_to_compare_two,
                                              column_with_id_two,
                                              many_to_many_csvfile):

    """
    Creates a many-to-many relationship table from two CSV files based on matching values in specified columns.

    This function reads two CSV files, each containing:
    - A unique ID column.
    - A column with values to compare.

    It finds matching values between the specified comparison columns from both files and generates a new CSV file
    that establishes relationships between the corresponding unique IDs.

    Parameters:
    csvfile_one (str): Path to the first input CSV file.
    column_to_compare_one (str): Column name in the first CSV file used for comparison.
    column_with_id_one (str): Column name in the first CSV file that contains unique IDs.
    csvfile_two (str): Path to the second input CSV file.
    column_to_compare_two (str): Column name in the second CSV file used for comparison.
    column_with_id_two (str): Column name in the second CSV file that contains unique IDs.
    many_to_many_csvfile (str): Path to save the resulting many-to-many relationship table.

    Output:
    - A CSV file with two columns:
      - Column 1: Unique ID from the first CSV file.
      - Column 2: Unique ID from the second CSV file.
    - Each row in the output file represents a relationship between a matching value in the two input files.

    Note:
    - The function assumes that comparison values are formatted consistently in both files.
    - Rows with no matching values in the comparison columns are ignored.
    """

    if many_to_many_csvfile.exists():
        many_to_many_csvfile.unlink()

    with open(csvfile_one, mode='r', newline='') as csvfile_one:
        reader_one = csv.reader(csvfile_one)

        with open(csvfile_two, mode='r', newline='') as csvfile_two:
            reader_two = list(csv.reader(csvfile_two))

            with open(many_to_many_csvfile, mode='a', newline='') as new_csvfile:
                writer = csv.writer(new_csvfile)

                for reader_1 in reader_one:
                    for reader_2 in reader_two:
                        if reader_1[column_to_compare_one] == reader_2[column_to_compare_two]:
                            new_row = [ reader_1[column_with_id_one], reader_2[column_with_id_two] ]
                            writer.writerow(new_row)


def make_csv_file_for_many_to_many_table(path_to_csvfile, path_to_new_csvfile):

    """
    Transforms a CSV file into a format suitable for a many-to-many relationship table.

    Parameters:
    - path_to_csvfile (str): Path to the input CSV file.
    - path_to_new_csvfile (str): Path to save the transformed CSV file.

    The input CSV file format:
    - The first column (index 0) contains unique IDs (foreign keys) for the many-to-many table.
    - Other columns contain 'Y' or 'N', indicating whether an object is associated with the unique ID.

    Transformation process:
    - For each row, if a column contains 'Y', a new entry is created in the output CSV file.
    - The output CSV file consists of two columns:
      1. The unique ID from the first column of the input file.
      2. The column index where 'Y' is present (acting as a foreign key to another table).
    - Each row in the new CSV file represents a valid foreign key pair for the many-to-many relationship.
    - The primary key (PK) in the resulting table is the combination of both columns.

    Example:
    Input CSV:
        unique_id, A, B, C
        1,         Y, N, Y
        2,         N, Y, Y

    Output CSV:
        1, 1  # (unique_id=1, fk=1) because 'Y' is in column 1 (A)
        1, 3  # (unique_id=1, fk=3) because 'Y' is in column 3 (C)
        2, 2  # (unique_id=2, fk=2) because 'Y' is in column 2 (B)
        2, 3  # (unique_id=2, fk=3) because 'Y' is in column 3 (C)
    """

    with open(path_to_csvfile, mode='r', newline='') as csvfile:
        reader = csv.reader(csvfile)

        with open(path_to_new_csvfile, mode='a', newline='') as new_csvfile:
            writer = csv.writer(new_csvfile)

            for row in reader:
                for index, value in enumerate(row):
                    if value == 'Y':
                        row_to_write = [row[0], index]
                        writer.writerow(row_to_write)


def make_new_csvfile_from_header_source_scv(path_to_csvfile,
                                            path_to_new_csvfile,
                                            number_of_columns):
    """
        Creates a new CSV file containing a single column with header names from the source CSV file.

        Parameters:
        - path_to_csvfile (str): Path to the source CSV file.
        - path_to_new_csvfile (str): Path to save the new CSV file.
        - number_of_columns (int): The total number of columns in the source CSV file.

        The function reads the header of the input CSV file and creates a new CSV file with a single column.
        The rows of the new CSV file will contain the names of the columns from the header of the source CSV.
        Only the column names are written to the new file, with no data rows included.

        Example:
        Input CSV (source):
            column1, column2, column3
            data1, data2, data3

        Output CSV (new):
            column1
            column2
            column3
        """

    if path_to_new_csvfile.exists():
        path_to_new_csvfile.unlink()

    data_for_new_csvfile = []
    with open(path_to_csvfile, mode='r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)

        for item in number_of_columns:
            data_for_new_csvfile.append(header[item])

    with open(path_to_new_csvfile, mode='a', newline='') as new_csvfile:
        writer = csv.writer(new_csvfile)
        for i in data_for_new_csvfile:
            writer.writerow([i])


def find_rows_with_multiple_values(path_to_csvfile,
                                   path_to_new_csvfile):
    """
        Processes a CSV file containing two columns and modifies the second column according to specific rules.

        This function is designed for a specific CSV format where:
        - The first column contains an identifier.
        - The second column contains city names, sometimes with multiple cities in one row.

        The function performs the following transformations:
        1. Splits rows with multiple city names (separated by commas or ' and ') into separate rows.
        2. Removes state abbreviations.
        3. Removes rows where the second column has no data.
        4. Trims long city names, keeping only the first word.

        Parameters:
        path_to_csvfile (str): Path to the input CSV file.
        path_to_new_csvfile (str): Path to save the processed CSV file.

        Example transformations:
        - "Phoenixville, Pottstown, Coatesville, Parkesburg, West Chester, Kennett Square and Oxford"
          → Multiple rows, each containing a single city.
        - "Bloomington, IN" → "Bloomington" (removes state abbreviation).
        - "Louisville/Jefferson County metro government (balance)" → "Louisville/Jefferson" (shortens long names).

        Note: This function is not general-purpose and is intended for a specific CSV structure.
        """

    if path_to_new_csvfile.exists():
        path_to_new_csvfile.unlink()

    with open(path_to_csvfile, mode='r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        with open(path_to_new_csvfile, mode='a', newline='') as new_csvfile:
            writer = csv.writer(new_csvfile)

            for row in reader:
                if ',' in row[1]:
                    row_list = row[1].split(',')
                    for item in row_list:
                        item = item.strip()
                        if item in ['IA', 'IN', 'KY', 'Mi', 'IN',
                                    'IN', 'NY', 'ID', 'AR', 'MO', 'TX',
                                    'AK', 'RI', 'AR', 'WI', '']:
                            continue
                        if ' and ' in item:
                            temp_items = item.split(' and ')
                            for i in temp_items:
                                writer.writerow([row[0], i])
                            continue
                        new_row = [row[0], item]
                        writer.writerow(new_row)
                elif len( list(row[1]) ) > 24:
                    row_list = row[1].split(' ')
                    writer.writerow([ row[0], row_list[0] ])
                else:
                    writer.writerow(row)