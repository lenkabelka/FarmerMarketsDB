import csv


def make_csvfile_for_loading_in_database(path_to_source_csvfile,
                                         path_to_new_csvfile,
                                         list_of_columns):

    """
    Creates a new CSV file from an existing one, including only the specified columns.

    Parameters:
    - path_to_source_csvfile (str): Path to the original CSV file.
    - path_to_new_csvfile (str): Path to save the new CSV file.
    - list_of_columns (list of int): List of column indices (0-based) to be included in the new CSV file.

    The function reads the source CSV file, extracts only the specified columns (by index),
    and writes the data to a new CSV file without a header.
    """

    ls = []
    with open(path_to_source_csvfile, mode='r', newline='') as source_file:
        reader = csv.reader(source_file)
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