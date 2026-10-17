import csv
import random
from datetime import datetime, timedelta

# Number of records
number_of_records = 100000

# ATM locations
locations = [
    "Andheri",
    "Bandra",
    "Dadar",
    "Borivali",
    "Kurla",
    "Thane",
    "Ghatkopar",
    "Vashi",
    "Malad",
    "Navi Mumbai"
]

# Location weights
location_weights = [
    12,  # Andheri
    14,  # Bandra
    10,  # Dadar
    9,   # Borivali
    8,   # Kurla
    10,  # Thane
    11,  # Ghatkopar
    7,   # Vashi
    8,   # Malad
    11   # Navi Mumbai
]

# Transaction types
transaction_types = [
    "Withdrawal",
    "Balance Enquiry",
    "Deposit",
    "Mini Statement"
]

# Start date
start_date = datetime(2026, 1, 1)

# Create CSV file
with open("atm_transactions.csv", "w", newline="") as file:

    writer = csv.writer(file)

    writer.writerow([
        "Transaction_ID",
        "Transaction_Date",
        "Transaction_Time",
        "ATM_Location",
        "Transaction_Type",
        "Amount",
        "Transaction_Status"
    ])

    for i in range(1, number_of_records + 1):

        transaction_id = "T" + str(i).zfill(6)

        # Random date within 2026
        random_days = random.randint(0, 364)

        transaction_date = start_date + timedelta(days=random_days)

        date_value = transaction_date.strftime("%d-%m-%Y")

        # Create realistic time patterns
        time_group = random.choices(
            ["Morning", "Afternoon", "Evening", "Night"],
            weights=[25, 30, 35, 10]
        )[0]

        if time_group == "Morning":
            hour = random.randint(6, 11)

        elif time_group == "Afternoon":
            hour = random.randint(12, 16)

        elif time_group == "Evening":
            hour = random.randint(17, 21)

        else:
            hour = random.randint(22, 23)

        minute = random.randint(0, 59)
        second = random.randint(0, 59)

        time_value = f"{hour:02d}:{minute:02d}:{second:02d}"

        # Select location using weights
        location = random.choices(
            locations,
            weights=location_weights
        )[0]

        # Select transaction type
        transaction_type = random.choices(
            transaction_types,
            weights=[45, 25, 20, 10]
        )[0]

        # Amount
        if transaction_type == "Withdrawal":

            amount = random.choice([
                500,
                1000,
                2000,
                5000,
                10000,
                15000,
                20000
            ])

        elif transaction_type == "Deposit":

            amount = random.choice([
                1000,
                2000,
                5000,
                10000,
                20000,
                50000
            ])

        else:

            amount = 0

        # Transaction status
        status = random.choices(
            ["Success", "Failed"],
            weights=[95, 5]
        )[0]

        writer.writerow([
            transaction_id,
            date_value,
            time_value,
            location,
            transaction_type,
            amount,
            status
        ])

print("ATM dataset created successfully!")
print("Total records:", number_of_records)
print("File: atm_transactions.csv")
