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
    '''Insert a new location into the database'''
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO locations (name, longitude, latitude, description)
        VALUES (?, ?, ?, ?)
    ''', (name, longitude, latitude,  description))

    conn.commit()
    conn.close()

def modify_location(db_name, id, name=None, latitude=None, longitude=None, description=None):
    ''' Modify an existing location in the database
        this isn't utilized yet but can be usefull in the future'''
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

def insert_irradiation_data(db_name, id, dict_irradiation):
    '''Insert daily irradiation data into the specific location table
    example dict_irradiation input=
    {'2024-01-01': {'GHI': 100, 'DNI': 50, 'DHI': 30, 'BNI': 20},
    '2024-01-02': {'GHI': 110, 'DNI': 60, 'DHI': 40, 'BNI': 25}}'''
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS location_{id} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT UNIQUE,
    GHI REAL,
    BHI REAL,
    DHI REAL,
    BNI REAL
    );
    """)

    for date, values in dict_irradiation.items():
        cursor.execute(f'''
            INSERT INTO location_{id} (date, GHI, BHI, DHI, BNI)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(date) DO UPDATE SET
            GHI = excluded.GHI,
            BHI = excluded.BHI,
            DHI = excluded.DHI,
            BNI = excluded.BNI
        ''', (date, values['GHI'], values['BHI'], values['DHI'], values['BNI']))

    conn.commit()
    conn.close()

def get_irradiation_data(db_name, id, start_date=None, end_date=None, all=False):
    '''Retrieve irradiation data for a specific location'''
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    if all:
        cursor.execute(f'SELECT * FROM daily_irr_{id}')
        rows = cursor.fetchall()

    conn.close()
    return rows

def get_location_list(db_name):
    '''Retrieve all locations from the database'''
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM locations')
    rows = cursor.fetchall()

    conn.close()
    return rows

def get_location_info(db_name, id):
    location_column = ['id','name','lon','lat','description']
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute(f'SELECT * FROM locations WHERE id = {id}')
    row = cursor.fetchone()
    conn.close()
    if not row:
        return #give output for id not found

    output = dict(zip(location_column,row))
    return output

def delete_table(db_name, table_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    conn.commit()
    conn.close()

def delete_location(db_name, location_id):
    #TODO delete also the location table with the irradiation value
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM locations WHERE ID ={location_id}")
    conn.commit()
    conn.close()

def dowload_irradiation(db_name, location_id):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT * FROM location_{location_id}")
        column_name = [description[0] for description in cursor.description]
        row = cursor.fetchall()
    except:
        return False
    conn.commit()
    conn.close()
    return column_name, row