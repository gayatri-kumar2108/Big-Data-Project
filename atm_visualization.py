import pandas as pd
import matplotlib.pyplot as plt
import os


# ============================================================
# CREATE GRAPHS FOLDER
# ============================================================

os.makedirs("graphs", exist_ok=True)


# ============================================================
# 1. ATM LOCATION VS TRANSACTION COUNT
# ============================================================

location = pd.read_csv(
    "results/location_analysis.csv"
)

plt.figure(figsize=(10, 6))

plt.bar(
    location["ATM_Location"],
    location["Transaction_Count"]
)

plt.title("ATM Location vs Transaction Count")
plt.xlabel("ATM Location")
plt.ylabel("Number of Transactions")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "graphs/location_transaction_count.png"
)

plt.close()


# ============================================================
# 2. TRANSACTION TYPE DISTRIBUTION
# ============================================================

transaction_type = pd.read_csv(
    "results/transaction_type_analysis.csv"
)

plt.figure(figsize=(8, 6))

plt.bar(
    transaction_type["Transaction_Type"],
    transaction_type["Transaction_Count"]
)

plt.title("Transaction Type Distribution")
plt.xlabel("Transaction Type")
plt.ylabel("Number of Transactions")

plt.xticks(rotation=20)

plt.tight_layout()

plt.savefig(
    "graphs/transaction_type_distribution.png"
)

plt.close()


# ============================================================
# 3. TRANSACTIONS BY HOUR
# ============================================================

hourly = pd.read_csv(
    "results/hourly_analysis.csv"
)

hourly = hourly.sort_values(
    "Transaction_Hour"
)

plt.figure(figsize=(10, 6))

plt.plot(
    hourly["Transaction_Hour"],
    hourly["Transaction_Count"],
    marker="o"
)

plt.title("ATM Transactions by Hour")
plt.xlabel("Hour of Day")
plt.ylabel("Number of Transactions")

plt.xticks(
    hourly["Transaction_Hour"]
)

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "graphs/transactions_by_hour.png"
)

plt.close()


# ============================================================
# 4. SUCCESS VS FAILED TRANSACTIONS
# ============================================================

status = pd.read_csv(
    "results/status_analysis.csv"
)

plt.figure(figsize=(7, 7))

plt.pie(
    status["Transaction_Count"],
    labels=status["Transaction_Status"],
    autopct="%1.1f%%"
)

plt.title("Transaction Status")

plt.tight_layout()

plt.savefig(
    "graphs/transaction_status.png"
)

plt.close()


# ============================================================
# 5. MONTHLY TRANSACTION ANALYSIS
# ============================================================

monthly = pd.read_csv(
    "results/monthly_analysis.csv"
)

monthly = monthly.sort_values(
    "Month"
)

plt.figure(figsize=(10, 6))

plt.plot(
    monthly["Month"],
    monthly["Transaction_Count"],
    marker="o"
)

plt.title("Monthly ATM Transactions")
plt.xlabel("Month")
plt.ylabel("Number of Transactions")

plt.xticks(
    monthly["Month"]
)

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "graphs/monthly_transactions.png"
)

plt.close()


# ============================================================
# 6. HIGH-VALUE TRANSACTIONS BY ATM LOCATION
# ============================================================

high_value = pd.read_csv(
    "results/high_value_location.csv"
)

plt.figure(figsize=(10, 6))

plt.bar(
    high_value["ATM_Location"],
    high_value["High_Value_Transactions"]
)

plt.title("High-Value Transactions by ATM Location")
plt.xlabel("ATM Location")
plt.ylabel("High-Value Transactions")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "graphs/high_value_transactions.png"
)

plt.close()


# ============================================================
# 7. FAILED TRANSACTIONS BY ATM LOCATION
# ============================================================

failure = pd.read_csv(
    "results/failure_analysis.csv"
)

plt.figure(figsize=(10, 6))

plt.bar(
    failure["ATM_Location"],
    failure["Failed_Transactions"]
)

plt.title("Failed Transactions by ATM Location")
plt.xlabel("ATM Location")
plt.ylabel("Failed Transactions")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "graphs/failed_transactions.png"
)

plt.close()


# ============================================================
# 8. TRANSACTION TYPE BY HOUR
# ============================================================

type_hour = pd.read_csv(
    "results/transaction_type_by_hour.csv"
)

plt.figure(figsize=(12, 7))

for transaction in type_hour["Transaction_Type"].unique():

    data = type_hour[
        type_hour["Transaction_Type"] == transaction
    ]

    data = data.sort_values(
        "Transaction_Hour"
    )

    plt.plot(
        data["Transaction_Hour"],
        data["Transaction_Count"],
        marker="o",
        label=transaction
    )

plt.title("Transaction Type by Hour")
plt.xlabel("Hour of Day")
plt.ylabel("Number of Transactions")

plt.legend()

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "graphs/transaction_type_by_hour.png"
)

plt.close()


# ============================================================
# FINAL MESSAGE
# ============================================================

print()
print("==============================================")
print("ALL GRAPHS CREATED SUCCESSFULLY")
print("==============================================")

print()
print("8 graphs have been saved inside the 'graphs' folder.")
