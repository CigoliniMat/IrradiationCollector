#script unify command to send to app.py
import utils.api as api
import utils.db_helper as db

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