from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    avg,
    sum,
    count,
    hour,
    to_timestamp,
    to_date,
    month
)
import os


# ============================================================
# CREATE SPARK SESSION
# ============================================================

spark = SparkSession.builder \
    .appName("ATM Transaction Pattern Analytics") \
    .master("local[*]") \
    .getOrCreate()


# ============================================================
# CREATE RESULTS FOLDER
# ============================================================

os.makedirs("results", exist_ok=True)


# ============================================================
# READ ATM TRANSACTION DATASET
# ============================================================

df = spark.read.csv(
    "atm_transactions.csv",
    header=True,
    inferSchema=False
)


# ============================================================
# DATA TYPE CONVERSION
# ============================================================

df = df.withColumn(
    "Amount",
    col("Amount").cast("int")
)

df = df.withColumn(
    "Time_Timestamp",
    to_timestamp(
        col("Transaction_Time"),
        "HH:mm:ss"
    )
)


# ============================================================
# 1. DISPLAY DATA
# ============================================================

print("\n========== ATM TRANSACTION DATA ==========")

df.select(
    "Transaction_ID",
    "Transaction_Date",
    "Transaction_Time",
    "ATM_Location",
    "Transaction_Type",
    "Amount",
    "Transaction_Status"
).show(
    10,
    truncate=False
)


# ============================================================
# 2. DATA STRUCTURE
# ============================================================

print("\n========== DATA STRUCTURE ==========")

df.printSchema()


# ============================================================
# 3. TOTAL TRANSACTIONS
# ============================================================

total_transactions = df.count()

print("\nTotal Transactions:", total_transactions)


# ============================================================
# 4. TOTAL TRANSACTION AMOUNT
# ============================================================

total_amount = df.select(
    sum("Amount").alias("Total_Amount")
)

print("\n========== TOTAL TRANSACTION AMOUNT ==========")

total_amount.show()


# ============================================================
# 5. LOCATION-WISE ANALYSIS
# ============================================================

location_analysis = df.groupBy(
    "ATM_Location"
).agg(
    count("*").alias("Transaction_Count"),
    sum("Amount").alias("Total_Amount")
).orderBy(
    col("Transaction_Count").desc()
)

print("\n========== LOCATION-WISE ANALYSIS ==========")

location_analysis.show()

location_analysis.toPandas().to_csv(
    "results/location_analysis.csv",
    index=False
)


# ============================================================
# 6. TRANSACTION TYPE ANALYSIS
# ============================================================

type_analysis = df.groupBy(
    "Transaction_Type"
).agg(
    count("*").alias("Transaction_Count"),
    sum("Amount").alias("Total_Amount")
).orderBy(
    col("Transaction_Count").desc()
)

print("\n========== TRANSACTION TYPE ANALYSIS ==========")

type_analysis.show()

type_analysis.toPandas().to_csv(
    "results/transaction_type_analysis.csv",
    index=False
)


# ============================================================
# 7. AVERAGE TRANSACTION AMOUNT
# ============================================================

average_amount = df.select(
    avg("Amount").alias("Average_Amount")
)

print("\n========== AVERAGE TRANSACTION AMOUNT ==========")

average_amount.show()

average_amount.toPandas().to_csv(
    "results/average_amount.csv",
    index=False
)


# ============================================================
# 8. PEAK TRANSACTION HOURS
# ============================================================

df = df.withColumn(
    "Transaction_Hour",
    hour("Time_Timestamp")
)

hour_analysis = df.groupBy(
    "Transaction_Hour"
).agg(
    count("*").alias("Transaction_Count")
).orderBy(
    col("Transaction_Count").desc()
)

print("\n========== PEAK TRANSACTION HOURS ==========")

hour_analysis.show()

hour_analysis.toPandas().to_csv(
    "results/hourly_analysis.csv",
    index=False
)


# ============================================================
# 9. TRANSACTION STATUS ANALYSIS
# ============================================================

status_analysis = df.groupBy(
    "Transaction_Status"
).agg(
    count("*").alias("Transaction_Count")
).orderBy(
    col("Transaction_Count").desc()
)

print("\n========== TRANSACTION STATUS ANALYSIS ==========")

status_analysis.show()

status_analysis.toPandas().to_csv(
    "results/status_analysis.csv",
    index=False
)


# ============================================================
# 10. FAILED TRANSACTIONS BY ATM LOCATION
# ============================================================

failed_analysis = df.filter(
    col("Transaction_Status") == "Failed"
).groupBy(
    "ATM_Location"
).agg(
    count("*").alias("Failed_Transactions")
).orderBy(
    col("Failed_Transactions").desc()
)

print("\n========== FAILED TRANSACTIONS BY ATM LOCATION ==========")

failed_analysis.show()

failed_analysis.toPandas().to_csv(
    "results/failure_analysis.csv",
    index=False
)


# ============================================================
# 11. FAILURE PERCENTAGE BY ATM LOCATION
# ============================================================

total_by_location = df.groupBy(
    "ATM_Location"
).agg(
    count("*").alias("Total_Transactions")
)

failed_by_location = df.filter(
    col("Transaction_Status") == "Failed"
).groupBy(
    "ATM_Location"
).agg(
    count("*").alias("Failed_Transactions")
)

failure_rate = total_by_location.join(
    failed_by_location,
    "ATM_Location"
)

failure_rate = failure_rate.withColumn(
    "Failure_Percentage",
    (
        col("Failed_Transactions")
        / col("Total_Transactions")
        * 100
    )
)

failure_rate = failure_rate.select(
    "ATM_Location",
    "Total_Transactions",
    "Failed_Transactions",
    "Failure_Percentage"
).orderBy(
    col("Failure_Percentage").desc()
)

print("\n========== FAILURE PERCENTAGE BY ATM LOCATION ==========")

failure_rate.show()

failure_rate.toPandas().to_csv(
    "results/failure_percentage.csv",
    index=False
)


# ============================================================
# 12. TRANSACTION TYPE BY ATM LOCATION
# ============================================================

location_type_analysis = df.groupBy(
    "ATM_Location",
    "Transaction_Type"
).agg(
    count("*").alias("Transaction_Count"),
    sum("Amount").alias("Total_Amount")
).orderBy(
    "ATM_Location",
    col("Transaction_Count").desc()
)

print("\n========== TRANSACTION TYPE BY ATM LOCATION ==========")

location_type_analysis.show(
    50,
    truncate=False
)

location_type_analysis.toPandas().to_csv(
    "results/location_type_analysis.csv",
    index=False
)


# ============================================================
# 13. MONTHLY TRANSACTION ANALYSIS
# ============================================================

df = df.withColumn(
    "Transaction_Date_Formatted",
    to_date(
        col("Transaction_Date"),
        "dd-MM-yyyy"
    )
)

monthly_analysis = df.groupBy(
    month(
        "Transaction_Date_Formatted"
    ).alias("Month")
).agg(
    count("*").alias("Transaction_Count"),
    sum("Amount").alias("Total_Amount")
).orderBy(
    "Month"
)

print("\n========== MONTHLY TRANSACTION ANALYSIS ==========")

monthly_analysis.show()

monthly_analysis.toPandas().to_csv(
    "results/monthly_analysis.csv",
    index=False
)


# ============================================================
# 14. HIGH-VALUE TRANSACTIONS
# ============================================================

high_value_transactions = df.filter(
    col("Amount") >= 20000
)

high_value_count = high_value_transactions.count()

print("\n========== HIGH-VALUE TRANSACTIONS ==========")

print(
    "High-Value Transactions:",
    high_value_count
)

high_value_transactions.select(
    "Transaction_ID",
    "Transaction_Date",
    "Transaction_Time",
    "ATM_Location",
    "Transaction_Type",
    "Amount",
    "Transaction_Status"
).orderBy(
    col("Amount").desc()
).show(
    20,
    truncate=False
)

high_value_transactions.select(
    "Transaction_ID",
    "Transaction_Date",
    "Transaction_Time",
    "ATM_Location",
    "Transaction_Type",
    "Amount",
    "Transaction_Status"
).toPandas().to_csv(
    "results/high_value_transactions.csv",
    index=False
)


# ============================================================
# 15. HIGH-VALUE TRANSACTIONS BY ATM LOCATION
# ============================================================

high_value_location = df.filter(
    col("Amount") >= 20000
).groupBy(
    "ATM_Location"
).agg(
    count("*").alias(
        "High_Value_Transactions"
    ),
    sum("Amount").alias(
        "High_Value_Amount"
    )
).orderBy(
    col("High_Value_Transactions").desc()
)

print(
    "\n========== HIGH-VALUE TRANSACTIONS BY ATM LOCATION =========="
)

high_value_location.show()

high_value_location.toPandas().to_csv(
    "results/high_value_location.csv",
    index=False
)


# ============================================================
# 16. TRANSACTION TYPE BY HOUR
# ============================================================

peak_hour_type = df.groupBy(
    "Transaction_Hour",
    "Transaction_Type"
).agg(
    count("*").alias("Transaction_Count")
).orderBy(
    "Transaction_Hour",
    col("Transaction_Count").desc()
)

print(
    "\n========== TRANSACTION TYPE BY HOUR =========="
)

peak_hour_type.show(
    100,
    truncate=False
)

peak_hour_type.toPandas().to_csv(
    "results/transaction_type_by_hour.csv",
    index=False
)


# ============================================================
# 17. FAILED TRANSACTIONS BY TRANSACTION TYPE
# ============================================================

failed_type_analysis = df.filter(
    col("Transaction_Status") == "Failed"
).groupBy(
    "Transaction_Type"
).agg(
    count("*").alias("Failed_Transactions")
).orderBy(
    col("Failed_Transactions").desc()
)

print(
    "\n========== FAILED TRANSACTIONS BY TYPE =========="
)

failed_type_analysis.show()

failed_type_analysis.toPandas().to_csv(
    "results/failed_type_analysis.csv",
    index=False
)


# ============================================================
# 18. HIGH-VALUE FAILED TRANSACTIONS
# ============================================================

high_value_failed = df.filter(
    (col("Amount") >= 20000) &
    (col("Transaction_Status") == "Failed")
)

print(
    "\n========== HIGH-VALUE FAILED TRANSACTIONS =========="
)

print(
    "High-Value Failed Transactions:",
    high_value_failed.count()
)

high_value_failed.select(
    "Transaction_ID",
    "Transaction_Date",
    "Transaction_Time",
    "ATM_Location",
    "Transaction_Type",
    "Amount",
    "Transaction_Status"
).orderBy(
    col("Amount").desc()
).show(
    20,
    truncate=False
)

high_value_failed.select(
    "Transaction_ID",
    "Transaction_Date",
    "Transaction_Time",
    "ATM_Location",
    "Transaction_Type",
    "Amount",
    "Transaction_Status"
).toPandas().to_csv(
    "results/high_value_failed.csv",
    index=False
)


# ============================================================
# FINAL MESSAGE
# ============================================================

spark.stop()

print("\n================================================")
print("ATM TRANSACTION ANALYSIS COMPLETED SUCCESSFULLY")
print("================================================")

print("\nAll analysis results have been saved in the 'results' folder.")
