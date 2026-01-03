# Bank Views Quick Reference

All commands assume we are in `/home/dk/code/SQL/table_union_view` and have `sqlite3` installed. The database file is `bank_transactions.db`.

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