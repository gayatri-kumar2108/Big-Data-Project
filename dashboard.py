import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="ATM Transaction Pattern Analytics",
    page_icon="🏧",
    layout="wide"
)


# ============================================================
# TITLE
# ============================================================

st.title("🏧 ATM Transaction Pattern Analytics System")

st.write(
    "Big Data analysis of ATM transactions using PySpark."
)


# ============================================================
# LOAD RESULT FILES
# ============================================================

location = pd.read_csv(
    "results/location_analysis.csv"
)

transaction_type = pd.read_csv(
    "results/transaction_type_analysis.csv"
)

hourly = pd.read_csv(
    "results/hourly_analysis.csv"
)

status = pd.read_csv(
    "results/status_analysis.csv"
)

monthly = pd.read_csv(
    "results/monthly_analysis.csv"
)

high_value = pd.read_csv(
    "results/high_value_location.csv"
)


# ============================================================
# KEY VALUES
# ============================================================

total_transactions = location[
    "Transaction_Count"
].sum()

total_amount = location[
    "Total_Amount"
].sum()

average_amount = total_amount / total_transactions

successful = status[
    status["Transaction_Status"] == "Success"
]["Transaction_Count"].iloc[0]

failed = status[
    status["Transaction_Status"] == "Failed"
]["Transaction_Count"].iloc[0]


# ============================================================
# KEY METRICS
# ============================================================

st.subheader("📌 Key Transaction Statistics")

col1, col2, col3, col4, col5 = st.columns(5)


with col1:
    st.metric(
        "Total Transactions",
        f"{total_transactions:,}"
    )


with col2:
    st.metric(
        "Total Amount",
        f"₹{total_amount:,.0f}"
    )


with col3:
    st.metric(
        "Average Amount",
        f"₹{average_amount:,.0f}"
    )


with col4:
    st.metric(
        "Successful",
        f"{successful:,}"
    )


with col5:
    st.metric(
        "Failed",
        f"{failed:,}"
    )


# ============================================================
# LOCATION ANALYSIS
# ============================================================

st.subheader("📍 ATM Location Analysis")

fig1, ax1 = plt.subplots(figsize=(10, 5))

ax1.bar(
    location["ATM_Location"],
    location["Transaction_Count"]
)

ax1.set_xlabel("ATM Location")
ax1.set_ylabel("Number of Transactions")
ax1.set_title(
    "Transactions by ATM Location"
)

plt.xticks(rotation=45)

plt.tight_layout()

st.pyplot(fig1)


# ============================================================
# TRANSACTION TYPE
# ============================================================

st.subheader("💳 Transaction Type Analysis")

fig2, ax2 = plt.subplots(figsize=(8, 5))

ax2.bar(
    transaction_type["Transaction_Type"],
    transaction_type["Transaction_Count"]
)

ax2.set_xlabel("Transaction Type")
ax2.set_ylabel("Number of Transactions")
ax2.set_title(
    "Transaction Type Distribution"
)

plt.xticks(rotation=20)

plt.tight_layout()

st.pyplot(fig2)


# ============================================================
# TWO COLUMN SECTION
# ============================================================

col1, col2 = st.columns(2)


# ============================================================
# HOURLY ANALYSIS
# ============================================================

with col1:

    st.subheader("⏰ Transactions by Hour")

    hourly = hourly.sort_values(
        "Transaction_Hour"
    )

    fig3, ax3 = plt.subplots(
        figsize=(8, 5)
    )

    ax3.plot(
        hourly["Transaction_Hour"],
        hourly["Transaction_Count"],
        marker="o"
    )

    ax3.set_xlabel("Hour")
    ax3.set_ylabel("Transactions")
    ax3.set_title(
        "ATM Transactions by Hour"
    )

    ax3.grid(True)

    plt.tight_layout()

    st.pyplot(fig3)


# ============================================================
# STATUS ANALYSIS
# ============================================================

with col2:

    st.subheader("✅ Transaction Status")

    fig4, ax4 = plt.subplots(
        figsize=(7, 5)
    )

    ax4.pie(
        status["Transaction_Count"],
        labels=status["Transaction_Status"],
        autopct="%1.1f%%"
    )

    ax4.set_title(
        "Successful vs Failed Transactions"
    )

    plt.tight_layout()

    st.pyplot(fig4)


# ============================================================
# MONTHLY ANALYSIS
# ============================================================

st.subheader("📅 Monthly Transaction Analysis")

monthly = monthly.sort_values(
    "Month"
)

fig5, ax5 = plt.subplots(
    figsize=(10, 5)
)

ax5.plot(
    monthly["Month"],
    monthly["Transaction_Count"],
    marker="o"
)

ax5.set_xlabel("Month")
ax5.set_ylabel("Transactions")
ax5.set_title(
    "Monthly ATM Transactions"
)

ax5.grid(True)

plt.tight_layout()

st.pyplot(fig5)


# ============================================================
# HIGH-VALUE TRANSACTIONS
# ============================================================

st.subheader("💰 High-Value Transactions")

fig6, ax6 = plt.subplots(
    figsize=(10, 5)
)

ax6.bar(
    high_value["ATM_Location"],
    high_value["High_Value_Transactions"]
)

ax6.set_xlabel("ATM Location")
ax6.set_ylabel(
    "High-Value Transactions"
)

ax6.set_title(
    "High-Value Transactions by ATM Location"
)

plt.xticks(rotation=45)

plt.tight_layout()

st.pyplot(fig6)


# ============================================================
# INSIGHTS
# ============================================================

st.subheader("🔍 Key Findings")

st.write(
    "• Total transactions analyzed: 100,000."
)

st.write(
    "• Withdrawal is the most common transaction type."
)

st.write(
    "• ATM activity is higher during afternoon and evening hours."
)

st.write(
    "• The highest transaction activity occurs around 9 PM."
)

st.write(
    "• Most transactions are successful."
)

st.write(
    "• High-value transactions are mainly associated with deposits and withdrawals."
)


# ============================================================
# FOOTER
# ============================================================

st.write("")
st.write("--------------------------------------------------")

st.write(
    "ATM Transaction Pattern Analytics System | "
    "Big Data Project | PySpark"
)
