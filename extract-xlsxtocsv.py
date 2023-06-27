import pandas as pd


def convert_xlsx_to_csv(xlsx_file, csv_file):
    # Read the XLSX file into a pandas DataFrame
    df = pd.read_excel(xlsx_file)

    # Write the DataFrame to a CSV file
    df.to_csv(csv_file, index=False)


# Example usage
# Replace with your XLSX file path
xlsx_file = '/Users/gerryasrillinsandy/Downloads/dump_homepass_20230530.xlsx'
# Replace with the desired CSV file name
csv_file = '/Users/gerryasrillinsandy/Downloads/dump_homepass_20230530.csv'

convert_xlsx_to_csv(xlsx_file, csv_file)
