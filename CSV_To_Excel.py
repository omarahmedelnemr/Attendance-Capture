import pandas as pd

def csv_to_excel(csv_file_name, sheet_name='Sheet1'):
    csv_file = "./Records/"+csv_file_name
    excel_file = "./Sheets/"+csv_file_name.replace("csv",'xlsx')

    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Write the DataFrame to an Excel file
    df.to_excel(excel_file, index=False, sheet_name=sheet_name)

