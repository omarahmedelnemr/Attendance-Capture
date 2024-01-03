import os
import shutil
import pandas as pd
from datetime import date

def save_to_csv(name, provided_names):
    """
   Saves a record to a CSV file.

   If the file already exists, it adds a new column with today's date and marks the provided names.
   If the file doesn't exist, it creates a copy from 'all.csv' and then adds a new column with today's date and marks the provided names.

   Parameters:
   name (str): The name of the CSV file to save to. This file should be located in the './Records/' directory.
   provided_names (list): A list of names to mark in the new column.

   Returns:
   print(f'- - The file {file_path} has been saved successfully! - -')


   Example:
   >>> save_to_csv('Crypto', ['Nady', 'Darwish'])
   This will save a record to the 'Crypto.csv' file in the './Records/' directory.
   """
    records_dir = "./Records"
    all_records_file = os.path.join(records_dir, "all.csv")

    # Check if the file with the given name exists
    file_path = os.path.join(records_dir, f"{name}.csv")
    provided_names = [i.split("_")[0] for i in provided_names]
    if os.path.exists(file_path):
        # If the file exists, open it and add a new column with today's date
        df = pd.read_csv(file_path)
        today_date = date.today().strftime("%Y-%m-%d")
        df[today_date] = 0  # Add a new column with zeros initially

        # Set the values to 1 for provided names in the new column
        df.loc[df['Names'].isin(provided_names), today_date] = 1

        # Save the updated DataFrame back to the file
        df.to_csv(file_path, index=False)
    else:
        # If the file doesn't exist, create a copy from 'all.csv'
        shutil.copy(all_records_file, file_path)

        # Open the new file and add a new column with today's date
        df = pd.read_csv(file_path)
        today_date = date.today().strftime("%Y-%m-%d")
        df[today_date] = 0  # Add a new column with zeros initially

        # Set the values to 1 for provided names in the new column
        df.loc[df['Names'].isin(provided_names), today_date] = 1

        # Save the updated DataFrame back to the file
        df.to_csv(file_path, index=False)

