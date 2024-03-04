import sqlite3

# Connect to the SQLite database file
conn = sqlite3.connect('chinook.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Execute the query to get all table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
# Execute the query to get all data from the table sqlite_sequence
cursor.execute("SELECT * FROM sqlite_sequence;")

# Fetch all the data from the query result
data = cursor.fetchall()

# Print the data
for row in data:
    print(row)


# Fetch all the table names from the query result
table_names = cursor.fetchall()

# Print the table names
for name in table_names:
    print(name[0])


cursor.close()
conn.close()