#script unify command to send to app.py
import utils.api as api
import utils.db_helper as db
import json

db_name = 'database.db'

def get_locations ():
    list = db.get_location_list(db_name)
    return list

def add_location (name,lat,lon,description,validation=True):
    '''add verify if lat and long isn't already been added
        get location list --> for each lat verify if is not equal or similar (+-0.0010) -->
        if true do it also for lon --> if true return:
        'coordinate are equal or similar to location "locationX" add location anyway?' -->
        if yes set validation on false and bypass this control
    '''
    try:
        db.insert_location(db_name,name,lat,lon,description)
    except Exception as e:
        return f'error while adding the location to the database,\nerror type: {type(e).__name__} error message: {e}'
    
    return 'location added succesfully'

def insert_irradiation(start_date, end_date):
    '''
    With the ID get the lat and lon, then download the irradiation and save in the database
    '''
    location_list = db.get_location_list(db_name)
    for location in location_list:
        lat = location[3]
        lon = location[2]
        location_id = location[0]
        irradiation_values = api.irradiation(lon,lat,start_date,end_date)
        db.insert_irradiation_data(db_name,location_id,irradiation_values)

    return #give output if all OK

def delete_location(location_id):
    table_name = f'location_{location_id}'
    db.delete_location(db_name, location_id)
    db.delete_table(db_name, table_name)

def download_csv(location_id):
    pass
