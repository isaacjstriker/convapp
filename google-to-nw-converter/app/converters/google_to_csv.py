import pandas as pd
import csv

def convert_google_sheet_to_csv(input_file, output_file):
    # Read the .xlsx file
    df = pd.read_excel(input_file)

    # Process the DataFrame to match NW Scheduler format
    # This is a placeholder for any specific processing needed
    # For example, renaming columns, filtering rows, etc.

    # Save the DataFrame to a CSV file
    df.to_csv(output_file, index=False, quoting=csv.QUOTE_MINIMAL)