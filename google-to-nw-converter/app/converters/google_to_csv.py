import pandas as pd
import random
import csv
import re
from datetime import datetime

def extract_date_from_row(row):
    date_pattern = r'(\d{1,2}/\d{1,2}/\d{2,4})'
    for val in row:
        if isinstance(val, str):
            match = re.search(date_pattern, val)
            if match:
                date_str = match.group(1)
                # Try parsing with 4-digit year first, then 2-digit year
                for fmt in ("%m/%d/%Y", "%m/%d/%y"):
                    try:
                        dt = datetime.strptime(date_str, fmt)
                        return dt.strftime("%Y/%m/%d")
                    except ValueError:
                        continue
    return "0001/01/01"

def convert_map_to_nw_format(input_file, output_file, territory_number):
    df = pd.read_excel(input_file)
    df['Town/Zip Code'] = df['Town/Zip Code'].fillna(method='ffill')
    df['Street/House#'] = df['Street/House#'].fillna(method='ffill')
    df[['Suburb', 'PostalCode']] = df['Town/Zip Code'].str.extract(r'(.+)\s+(\d{5})')
    processed_data = []
    territory_id = random.randint(1000000, 9999999)
    used_ids = set()
    current_street = None

    # Merge Phone# and Householder Name for easier logic
    df['MergedNamePhone'] = df[['Phone#', 'Householder Name']].fillna('').agg(' '.join, axis=1).str.strip()

    # Group apartments by base number and street
    apartment_groups = {}
    for idx, row in df.iterrows():
        street_house = str(row.get("Street/House#", "")).strip()
        apt_match = re.match(r"(\d+)\s*Apt\s*(\w+)", street_house, re.IGNORECASE)
        if apt_match:
            base_number = apt_match.group(1)
            street = current_street if current_street else ""
            key = (base_number, row.get('Suburb', ''), row.get('PostalCode', ''), street)
            if key not in apartment_groups:
                apartment_groups[key] = []
            apartment_groups[key].append((idx, apt_match.group(2), street_house))

    # Find single-apartment indices
    single_apartment_indices = set()
    for group in apartment_groups.values():
        if len(group) == 1:
            idx, _, _ = group[0]
            single_apartment_indices.add(idx)

    for idx, row in df.iterrows():
        street_house = str(row.get("Street/House#", "")).strip()
        householder = str(row.get("Householder Name", "")).strip()

        # If this row is a street name (not starting with a digit), update current_street and skip
        if street_house and not re.match(r"^\d", street_house):
            current_street = street_house
            continue

        # If this row is missing a house number or current_street, skip it
        number_match = re.match(r"^(\d+)", street_house)
        has_number = bool(number_match)
        if not (has_number and current_street):
            continue

        # Generate unique TerritoryAddressID
        while True:
            addr_id = random.randint(1000000, 9999999)
            if addr_id not in used_ids:
                used_ids.add(addr_id)
                break

        street_house = str(row.get("Street/House#", "")).strip()
        number = None
        street = current_street
        apt_match = re.match(r"(\d+)\s*Apt\s*(\w+)", street_house, re.IGNORECASE)
        if apt_match:
            number = apt_match.group(1)
            # Street stays as current_street
        elif re.match(r"^\d+", street_house):
            number = street_house.split()[0]
        else:
            current_street = street_house
            street = current_street

        # Apartment logic
        apartment_number = ""
        type_field = "House"
        is_apartment = False
        for key, group in apartment_groups.items():
            for group_idx, apt_num, _ in group:
                if group_idx == idx:
                    if len(group) == 1:
                        apartment_number = ""
                        type_field = "House"
                    else:
                        apartment_number = apt_num
                        type_field = "Apartment"
                        is_apartment = True
                        number = key[0]
                        street = key[3] if key[3] else street
                    break

        # "___ Family" logic
        householder = str(row.get("Householder Name", ""))
        if "Family" in householder:
            type_field = "House"

        # Business logic
        merged = row.get("MergedNamePhone", "")
        if "Unknown Resident" not in merged and type_field not in ["Apartment", "House"]:
            type_field = "Business"

        # Ensure Name is set correctly
        name = str(row.get("Householder Name", "")).strip()
        if not name:
            if "Unknown Resident" in merged or "Family" in merged:
                name = merged

        # Phone number extraction and validation
        phone = str(row.get("Phone#", "")).strip()

        # Define a simple phone number pattern (adjust as needed)
        phone_pattern = r"^\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$"

        # If Phone# is not a phone number and not empty, move it to Name
        if phone and (not re.match(phone_pattern, phone)):
            # If Householder Name is empty, use Phone# value as Name
            if not name or name.lower() == "nan":
                name = phone
            # Clear the phone field since it's not a phone number
            phone = ""

        # Notes logic
        notes = ""
        alt_mail = str(row.get("Alternative Mailing Address", ""))
        mailbox = str(row.get("Mailbox Y/N", "")).strip().upper()
        door_work = str(row.get("Door to Door Work", ""))
        comments = str(row.get("Comments", ""))
        if "Unknown Resident" in merged:
            notes = "No mailing"
        elif "PO Box" in alt_mail:
            notes = alt_mail
        elif mailbox == "N":
            notes = "No mailing"
        if comments and comments not in notes:
            notes = (notes + " " if notes else "") + comments

        # Status and StatusDate logic
        status = "Available"
        status_date = "0001/01/01"
        if "Letter Writing" in door_work:
            status = "Custom2"
            status_date = extract_date_from_row(row)
        elif "Do Not Call" in door_work:
            status = "DoNotCall"
            status_date = extract_date_from_row(row)

        processed_row = {
            "TerritoryID": territory_id,
            "TerritoryNumber": territory_number,
            "CategoryCode": "D",
            "Category": "Door to Door",
            "TerritoryAddressID": addr_id,
            "ApartmentNumber": apartment_number,
            "Number": number,
            "Street": street,
            "Suburb": row.get("Suburb", ""),
            "PostalCode": row.get("PostalCode", ""),
            "State": "Vermont",
            "Name": name,
            "Phone": phone,
            "Type": type_field,
            "Status": status,
            "StatusDate": status_date,
            "Latitude": 0,
            "Longitude": 0,
            "Notes": notes,
            "NotesFromPublisher": "",
        }
        processed_data.append(processed_row)

    processed_df = pd.DataFrame(processed_data)
    processed_df.to_csv(output_file, index=False, quoting=csv.QUOTE_MINIMAL)