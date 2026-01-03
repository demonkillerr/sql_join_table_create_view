"""Create a bank transaction table in SQLite and emit insert statements."""
from __future__ import annotations

import random
from datetime import date, timedelta
from pathlib import Path
import sqlite3

DB_PATH = Path("bank_transactions.db")
SQL_PATH = Path("bank_transactions_inserts.sql")
NUM_ROWS = 100
random.seed(42)

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS bank_transactions (
    id INTEGER PRIMARY KEY,
    transaction_date TEXT NOT NULL,
    description TEXT NOT NULL,
    account_number TEXT NOT NULL,
    amount REAL NOT NULL,
    currency TEXT NOT NULL,
    transaction_type TEXT NOT NULL,
    merchant TEXT NOT NULL,
    balance_after REAL NOT NULL,
    category TEXT NOT NULL,
    status TEXT NOT NULL,
    reference_number TEXT NOT NULL
);
"""

DESCRIPTIONS = [
    "Subscription fee",
    "Card payment",
    "Transfer from savings",
    "Online purchase",
    "Cash deposit",
    "Wire out",
    "Salary posting",
    "Refund",
    "Investment transfer",
    "Mortgage payment",
    "Utility bill",
    "Insurance premium",
]

MERCHANTS = [
    "Northwind Markets",
    "Pioneer Tech",
    "Citywide Utilities",
    "Mercer Grocers",
    "Orbit Mobility",
    "Asteria Health",
    "Bluefin Travel",
    "Peak Apparel",
    "Praxis Electronics",
    "Sunset Insurance",
]

ACCOUNTS = [
    "ACCT-1083-983",
    "ACCT-3301-776",
    "ACCT-4409-224",
    "ACCT-5022-118",
    "ACCT-9011-410",
]

CURRENCIES = ["USD", "EUR", "GBP", "CAD"]
TRANSACTION_TYPES = ["debit", "credit", "transfer"]
CATEGORIES = [
    "groceries",
    "travel",
    "health",
    "entertainment",
    "utilities",
    "salary",
    "mortgage",
    "investment",
]
STATUSES = ["completed", "pending", "failed"]


def escape_sql(value: str) -> str:
    return value.replace("'", "''")


def format_amount(value: float) -> str:
    return f"{value:.2f}"


def build_transaction_rows() -> tuple[list[tuple], list[str]]:
    rows: list[tuple] = []
    insert_statements: list[str] = []
    next_balance = 5000.0
    start_date = date(2024, 1, 1)

    for idx in range(1, NUM_ROWS + 1):
        transaction_date = start_date + timedelta(days=idx * 3)
        merchant = random.choice(MERCHANTS)
        description = random.choice(DESCRIPTIONS)
        account_number = random.choice(ACCOUNTS)
        currency = random.choice(CURRENCIES)
        transaction_type = random.choice(TRANSACTION_TYPES)
        category = random.choice(CATEGORIES)
        status = random.choice(STATUSES)
        amount = round(random.uniform(-1500, 3000), 2)
        next_balance = round(next_balance + amount, 2)
        reference_number = f"REF-{random.randint(100000, 999999)}"

        rows.append(
            (
                idx,
                transaction_date.isoformat(),
                description,
                account_number,
                amount,
                currency,
                transaction_type,
                merchant,
                next_balance,
                category,
                status,
                reference_number,
            )
        )

        escaped_values = [
            str(idx),
            f"'{escape_sql(transaction_date.isoformat())}'",
            f"'{escape_sql(description)}'",
            f"'{escape_sql(account_number)}'",
            format_amount(amount),
            f"'{escape_sql(currency)}'",
            f"'{escape_sql(transaction_type)}'",
            f"'{escape_sql(merchant)}'",
            format_amount(next_balance),
            f"'{escape_sql(category)}'",
            f"'{escape_sql(status)}'",
            f"'{escape_sql(reference_number)}'",
        ]

        insert_statements.append(
            "INSERT INTO bank_transactions (id, transaction_date, description, account_number, amount, currency, transaction_type, merchant, balance_after, category, status, reference_number) VALUES (" +
            ", ".join(escaped_values) +
            ");"
        )

    return rows, insert_statements


def main() -> None:
    rows, insert_statements = build_transaction_rows()

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(SCHEMA_SQL)
        conn.executemany(
            """
            INSERT INTO bank_transactions (
                id,
                transaction_date,
                description,
                account_number,
                amount,
                currency,
                transaction_type,
                merchant,
                balance_after,
                category,
                status,
                reference_number
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            rows,
        )

    SQL_PATH.write_text("\n".join(insert_statements) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()