import pandas as pd
import sqlite3

# create a database in sqlite3
db_connection = sqlite3.connect('/workspaces/gamzat-python/db/support_tickets.db')
cursor = db_connection.cursor()

# create global tickets table in sql
db_creation = '''CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY NOT NULL,
    creation_date DATE NOT NULL,
    last_log_time DATE NOT NULL,
    ref TEXT NOT NULL,
    id_arbo INT NOT NULL,
    marque TEXT NOT NULL,
    id_status INT NOT NULL,
    status TEXT NOT NULL,
    contrat TEXT NOT NULL,
    type_ticket TEXT NOT NULL,
    ticket_admin TEXT NOT NULL,
    is_read INT NOT NULL,
    distributor TEXT,
    station TEXT,
    EAN INT,
    purchase_date DATE,
    ticket_total_log_count INT,
    ticket_log_count_today INT
    )'''

cursor.execute(db_creation)
db_connection.commit()

db_creation = '''CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY NOT NULL,
    log_admin DATE NOT NULL,
    logs_qty DATE NOT NULL
    )'''

cursor.execute(db_creation)
db_connection.commit()

#  the code below is used once to feed sql db with past data and is should not be used only once, during app deployment
# ---------------------------------------------------------------------------------------------------------------------
# Read CSV file into a pandas DataFrame
csv_file = '/workspaces/gamzat-python/db/csv_db.csv'
df = pd.read_csv(csv_file)

# Write DataFrame to SQLite database
df.to_sql('tickets', db_connection, index=False, if_exists='replace')

# Commit changes and close connection
db_connection.commit()

# Read CSV file into a pandas DataFrame
csv_file = '/workspaces/gamzat-python/db/logs.csv'
df = pd.read_csv(csv_file)

# Write DataFrame to SQLite database
df.to_sql('logs', db_connection, index=False, if_exists='replace')

# Commit changes and close connection
db_connection.commit()
# -------------------------------------------------------------------------------------------------------------------
db_connection.close()