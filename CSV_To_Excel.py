import pandas as pd

def csv_to_excel(csv_file_name, sheet_name='Sheet1'):
    """
   Converts a CSV file to an Excel file.

   Parameters:
   csv_file_name (str): The name of the CSV file to convert. This file should be located in the './Records/' directory.
   sheet_name (str, optional): The name of the sheet in the Excel file. Defaults to 'Sheet1'.

   Returns:
   The file {file path} has been converted successfully!

   Example:
   >>> csv_to_excel('example.csv', 'Example Sheet')
   This will convert the 'example.csv' file in the './Records/' directory to an Excel file named 'example.xlsx' in the './Sheets/' directory. The Excel file will have a single sheet named 'Example Sheet'.
   """
    csv_file = "./Records/"+csv_file_name
    excel_file = "./Sheets/"+csv_file_name.replace("csv",'xlsx')

    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Write the DataFrame to an Excel file
    df.to_excel(excel_file, index=False, sheet_name=sheet_name)

