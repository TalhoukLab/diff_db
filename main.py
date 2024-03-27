from bokeh.plotting import figure
import subprocess
import sqlite3
import time
import pandas as pd

database_1 = "./Data/test.db"
database_2 = "./Data/test2.db"

conn = sqlite3.connect(database_1)
cursor = conn.cursor()
conn2 = sqlite3.connect(database_2)
cursor2 = conn2.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
table_names = cursor.fetchall()
table_names

for name in table_names:
    print(name[0])

return_code = subprocess.check_output(["./sqldiff.exe", database_1, database_2])
output = return_code.decode("utf-8").splitlines()
inserts = [line for line in output if line.startswith("INSERT")]
updates = [line for line in output if line.startswith("UPDATE")]
deletes = [line for line in output if line.startswith("DELETE")]

tables_altered = {'updated':[], 'insertions':[], 'deletions':[]}
total_tables_altered = set()

for i in range(len(updates)):
    x = updates[i].split()[1]
    print(x)
    tables_altered.get('updated').append(x)
    total_tables_altered.add(x)

for i in range(len(inserts)):
    x = inserts[i].split()[2].split('(')[0]
    print(x)
    tables_altered.get('insertions').append(x)
    total_tables_altered.add(x)

for i in range(len(deletes)):
    x = deletes[i].split()[2]
    print(x)
    tables_altered.get('deletions').append(x)
    total_tables_altered.add(x)

start_time = time.time()

n_inserts = len(inserts)
insert_data = []

for i in range(n_inserts):
    table_changed = inserts[i].split(" ")[2].split("(")[0]
    table_cols = inserts[i].split(" ")[2]
    all_values = "".join(inserts[i].split(" ")[3:])

    cols = "".join(table_cols.split("(")[1:])[:-1].split(",")
    values = "".join(all_values.split("(")[1:])[:-2].split(",")

    cursor.execute(f"PRAGMA table_info({table_changed})")
    table_info = cursor.fetchall()

    for column in table_info:
        if column[5] == 1:
            primary_key = column[1]
            break


    cols, values, primary_key

    idx_of = cols.index(primary_key)
    
    for ijk in range(len(cols)):
        insert_data.append([table_changed, primary_key, values[idx_of], cols[ijk], values[ijk]])


print("--- %s seconds ---" % (time.time() - start_time))

df1 = pd.DataFrame(insert_data, columns=['Table Name', 'Primary Key', 'PK Value', 'Column', 'New Value'])
df1['Old Value'] = None
df1['type'] = 'Insert'

start_time = time.time()
delete_data = []

for i in range(len(deletes)):
    table = deletes[i].split(" ")[2]
    primary_key, pk_value = deletes[i].split(" ")[4][:-1].split("=")

    old_value = cursor.execute(f"SELECT * FROM {table} WHERE {primary_key}={pk_value};").fetchall()
    cols = cursor.execute(f"PRAGMA table_info({table})").fetchall()
    col_values = [value[1] for value in cols]

    for ijk in range(len(old_value[0])):
        delete_data.append((table, primary_key, pk_value, col_values[ijk], old_value[0][ijk]))


print("--- %s seconds ---" % (time.time() - start_time))
df2 = pd.DataFrame(delete_data, columns=['Table Name', 'Primary Key', 'PK Value', 'Column', 'Old Value'])
df2['New Value'] = None
df2['type'] = 'Delete'


update_data = []

for i in range(len(updates)):
    table_changed = updates[i].split(" ")[1]
    primary_key, pk_value = updates[i].split(" ")[-1][:-1].split("=")
    [value.split("=") for value in "".join(updates[i].split(" ")[3:-2]).split(",")]
    cols_changed = [value.split("=")[0] for value in "".join(updates[i].split(" ")[3:-2]).split(",")]
    
    for col in cols_changed:
        cursor.execute(f"SELECT {col} FROM {table_changed} WHERE {primary_key}={pk_value};")
        old_values = cursor.fetchall()[0][0]

        cursor2.execute(f"SELECT {col} FROM {table_changed} WHERE {primary_key}={pk_value};")
        new_values = cursor2.fetchall()[0][0]
    
    for ijk in range(len(cols_changed)):
        update_data.append((table_changed, primary_key, pk_value, cols_changed[ijk], old_values, new_values))
        

cursor.close()
conn.close()
cursor2.close()
conn2.close()

df3 = pd.DataFrame(update_data, columns=['Table Name', 'Primary Key', 'PK Value', 'Column', 'Old Value', 'New Value'])
df3['type'] = 'Update'

df = pd.concat([df1, df2, df3], ignore_index=True)

df.to_csv('changes.csv', index=False)