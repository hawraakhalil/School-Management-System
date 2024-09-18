import sqlite3
import os,sys

# Connect to the SQLite database
db_path = os.path.join('src/database', 'school_management.db')
conn =  sqlite3.connect(db_path)
cursor = conn.cursor()

# Retrieve the list of tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("Tables in the database:")
for table in tables:
    print(table[0])

# Retrieve the schema of each table
for table in tables:
    print(f"\nSchema for {table[0]}:")
    cursor.execute(f"PRAGMA table_info({table[0]});")
    schema = cursor.fetchall()
    for column in schema:
        print(column)

# Function to fetch and display all rows from a given table
def fetch_and_display_table_data(table_name):
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    
    print(f"\n{table_name} Table Data:")
    if rows:
        for row in rows:
            print(row)
    else:
        print("No data found.")

# Retrieve and display data from each table
fetch_and_display_table_data('Students')
fetch_and_display_table_data('Instructors')
fetch_and_display_table_data('Courses')
fetch_and_display_table_data('Registrations')

# Close the connection
conn.close()
