# Bank Views Quick Reference

All commands assume we are in `/home/dk/code/SQL/table_union_view` and have `sqlite3` installed. The database file is `bank_transactions.db`.

## 1. Table creation
- Create the primary dataset and schema plus its insert statement file.
  ```sh
  .venv/bin/python generate_transactions.py
  sqlite3 bank_transactions.db "SELECT COUNT(*) FROM bank_transactions;"
  ```
- Build the secondary dataset that shares the same schema for future unions.
  ```sh
  .venv/bin/python generate_transactions_alt.py
  sqlite3 bank_transactions.db "SELECT COUNT(*) FROM bank_transactions_alt;"
  ```

## 2. Table union
- Materialize the joined data into `bank_combined_data` (200 rows).
  ```sh
  sqlite3 bank_transactions.db "DROP TABLE IF EXISTS bank_combined_data;"
  sqlite3 bank_transactions.db "CREATE TABLE bank_combined_data AS SELECT * FROM bank_transactions UNION ALL SELECT * FROM bank_transactions_alt;"
  sqlite3 bank_transactions.db "SELECT COUNT(*) FROM bank_combined_data;"
  ```

## 3. View creation
- Create the `bank_transactions_union_view` from the same union logic so downstream objects like `third_party` can query it safely.
  ```sh
  sqlite3 bank_transactions.db "CREATE VIEW IF NOT EXISTS bank_transactions_union_view AS SELECT * FROM bank_transactions UNION ALL SELECT * FROM bank_transactions_alt;"
  ```

## `third_party` view
- Show the view definition:
  ```sh
  sqlite3 bank_transactions.db ".schema third_party"
  ```
- Count rows exposed to third parties:
  ```sh
  sqlite3 bank_transactions.db "SELECT COUNT(*) FROM third_party;"
  ```
- Sample the data (defaults to pipe-delimited output):
  ```sh
  sqlite3 bank_transactions.db "SELECT transaction_date, amount, currency, reference_number FROM third_party LIMIT 5;"
  ```

- Export the view as JSON for hand-off:
  ```sh
  sqlite3 bank_transactions.db <<'EOF'
  .mode json
  .output third_party.json
  SELECT transaction_date, amount, currency, reference_number FROM third_party;
  EOF
  ```

## `bank_transactions_union_view`
- Show its definition (union of both tables):
  ```sh
  sqlite3 bank_transactions.db ".schema bank_transactions_union_view"
  ```
- Count how many rows (should be 200):
  ```sh
  sqlite3 bank_transactions.db "SELECT COUNT(*) FROM bank_transactions_union_view;"
  ```
- Peek at the merged data:
  ```sh
  sqlite3 bank_transactions.db "SELECT * FROM bank_transactions_union_view LIMIT 5;"
  ```

Both views can be queried directly whenever the database file is present. If you need to refresh either view, recreate it using the `CREATE VIEW` statements you can find in the project history or run the generator scripts again.