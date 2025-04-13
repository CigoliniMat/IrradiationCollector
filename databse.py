import sqlite3

def create_database(db_name):
    """Create a SQLite database with a table for save locations."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create table for locations
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS locations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    longitude REAL,
    latitude  REAL,
    description TEXT
    );
    """)

    conn.commit()
    conn.close()

def insert_location(db_name, name, latitude, longitude, description):
    """Insert a new location into the database."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO locations (name, longitude, latitude, description)
        VALUES (?, ?, ?, ?)
    ''', (name, longitude, latitude,  description))

    conn.commit()
    conn.close()

def modify_location(db_name, id, name=None, latitude=None, longitude=None, description=None):
    """Modify an existing location in the database."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create a list of columns to update
    columns = []
    values = []

    if name is not None:
        columns.append('name = ?')
        values.append(name)
    if latitude is not None:
        columns.append('latitude = ?')
        values.append(latitude)
    if longitude is not None:
        columns.append('longitude = ?')
        values.append(longitude)
    if description is not None:
        columns.append('description = ?')
        values.append(description)

    # Add the ID to the end of the values list
    values.append(id)

    # Create the SQL query
    sql_query = f'UPDATE locations SET {", ".join(columns)} WHERE id = ?'

    cursor.execute(sql_query, values)
    conn.commit()
    conn.close()

db_name = 'daily_irradiation.db'
name = 'impianto2'
latitude = 45.454545
longitude = 10.11110
description = ''

insert_location(db_name, name, latitude, longitude, description)
