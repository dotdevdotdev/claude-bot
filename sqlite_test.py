#!/usr/bin/env python3
import sqlite3
from datetime import datetime

# Connect to the database
db_path = "/home/dotdev/projects/claude-bot/database.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create the table
print("Creating table...")
cursor.execute("""
CREATE TABLE IF NOT EXISTS mcp_test_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    server_name TEXT NOT NULL,
    status TEXT NOT NULL,
    test_date TEXT NOT NULL
)
""")
conn.commit()
print("Table created successfully!")

# Insert test results
print("\nInserting test results...")
test_data = [
    ("filesystem", "success", "2025-01-29 14:30:00"),
    ("github", "success", "2025-01-29 14:35:00"),
    ("playwright", "failed", "2025-01-29 14:40:00"),
    ("taskmaster-ai", "success", "2025-01-29 14:45:00"),
    ("sqlite", "success", "2025-01-29 14:50:00")
]

cursor.executemany("""
INSERT INTO mcp_test_results (server_name, status, test_date)
VALUES (?, ?, ?)
""", test_data)
conn.commit()
print(f"Inserted {cursor.rowcount} rows")

# Query all results
print("\nQuerying all results:")
cursor.execute("SELECT * FROM mcp_test_results")
results = cursor.fetchall()

print("\nID | Server Name    | Status  | Test Date")
print("-" * 50)
for row in results:
    print(f"{row[0]:<3}| {row[1]:<15}| {row[2]:<8}| {row[3]}")

# Close the connection
conn.close()
print("\nDatabase operations completed successfully!")