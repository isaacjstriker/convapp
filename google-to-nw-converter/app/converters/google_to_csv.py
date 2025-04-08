import pandas as pd
import csv
import requests
from io import BytesIO
import random

def convert_google_sheet_to_csv(input_file, output_file, territory_number):
    '''if "docs.google.com/spreadsheets" in google_sheet_url:
        google_sheet_url = google_sheet_url.replace('/edit', '/export?format=xlsx').replace('/view', '/export?format=xlsx')

    response = requests.get(google_sheet_url)
    response.raise_for_status()
    input_file = BytesIO(response.content)'''
    
    df = pd.read_excel(input_file)

    # Forward fill data in Columns A and B
    df[['Town/Zip Code', 'Street/House#']] = df[['Town/Zip Code', 'Street/House#']].fillna('ffill')

    # Handles splitting the town and zip code
    df[['Suburb', 'PostalCode']] = df['Town/Zip Code'].str.extract(r'(.+)\s+(\d{5})')

    processed_data = []

    territory_id = random.randint(1000000, 9999999)

    used_ids = set()

    row_count = 0
    for _, row in df.iterrows():
            row_count += 1
            
            while True:
                addr_id = random.randint(1000000, 9999999)
                if addr_id not in used_ids:
                    used_ids.add(addr_id)
                    break

            street_house = row.get("Street/House#", "")

            if pd.notna(street_house):  # Check if the value is not NaN
                street_house = str(street_house).strip()  # Convert to string and strip whitespace
                number = street_house.split()[0] if len(street_house.split()) > 0 else None
                street = " ".join(street_house.split()[1:]) if len(street_house.split()) > 1 else None
            else:
                number = None
                street = None

            mailbox_value = row.get("Mailbox Y/N", "")
            if pd.notna(mailbox_value):  # Check if the value is not NaN
                mailbox_value = str(mailbox_value).strip().upper()  # Convert to string, strip whitespace, and normalize
            else:
                mailbox_value = ""
            address_type = "House" if mailbox_value == "Y" else "Other"

            processed_row = {
            "TerritoryID": territory_id,
            "TerritoryNumber": territory_number,
            "CategoryCode": "D",
            "Category": "Door to Door",
            "TerritoryAddressID": addr_id,
            "ApartmentNumber": "",
            "Number": number,
            "Street": street,
            "Suburb": row.get("Suburb", None),
            "PostalCode": row.get("PostalCode", None),
            "State": "Vermont",
            "Name": row.get("Householder Name", None),
            "Phone": row.get("Phone#", None),
            "Type": address_type,
            "Status": "Available",
            "StatusDate": "0001/01/01",
            "Latitude": 0,
            "Longitude": 0,
            "Notes": row.get("Comments", None),
            "NotesFromPublisher": "",
        }
            processed_data.append(processed_row)
    
    processed_df = pd.DataFrame(processed_data)
    processed_df.to_csv(output_file, index=False, quoting=csv.QUOTE_MINIMAL)