#script unify command to send to app.py
import utils.api as api
import utils.db_helper as db
import csv
from pathlib import Path
from datetime import datetime, timedelta

db_name = 'database/irradiation.db'

def get_locations ():
    #TODO output if somethink gone wrong
    list = db.get_location_list(db_name)
    return list

def add_location (name,lat,lon,description,validation=True):
    ''' #TODO  add verify if lat and lon isn't already been added:

        1)  get location list -->
        2)  for each lat verify if is not equal or similar (+-0.0010) -->
        3)  if true do it also for lon -->
        4)  if true return:
            'coordinate are equal or similar to location "locationX" add location anyway?'-->
            if user say yes set validation to false to bypass this control
    '''
    try:
        db.insert_location(db_name,name,lat,lon,description)
    except Exception as e:
        return f'error while adding the location to the database,\nerror type: {type(e).__name__} error message: {e}'
    
    return 'location added succesfully'

def insert_irradiation(date_offset=7, api_first_value='2004-01-01'):
    location_list = db.get_location_list(db_name) #take the list of all location
    ''' take the today date and remove the day offset
        (because the api need some day to get the irradiation value, without this the api will work anyway, is for safe),
        the convert the date in the correct format
    '''
    date_obj = datetime.now()
    date_obj = date_obj - timedelta(days=date_offset)
    end_date = date_obj.strftime('%Y-%m-%d')

    for location in location_list:
        lat = location[3]
        lon = location[2]
        location_id = location[0]
        l = db.dowload_irradiation(db_name, location_id) #get the current location irradiation value
        #if there is no value set start date to the first possible
        if l == False:
            start_date = '2004-01-01'
        else:
            l = l[1] #get the list of the current downloaded date
            last_row = l[-1] #get the last date in the list
            start_date = last_row[1]
        irradiation_values = api.irradiation(lon,lat,start_date,end_date)
        db.insert_irradiation_data(db_name,location_id,irradiation_values)

    return #TODO output if somethink gone wrong

def delete_location(location_id):
    '''#TODO
        output if somethink gone wrong
    '''
    table_name = f'location_{location_id}'
    db.delete_location(db_name, location_id)
    db.delete_table(db_name, table_name)

def download_csv(location_id):
    #TODO output if somethink gone wrong
    '''get value from database, convert the sign for the decimal from . to ,
        and save the file in csv with ; as delimiter and ENTER as newline'''
    folder = Path('temp')

    for file in folder.glob('*csv'):#delete all csv file in the temp folder
        file.unlink()

    output = []
    location_name = db.get_location_info(db_name, location_id)['name']
    column_name, rows = db.dowload_irradiation(db_name, location_id)
    column_name.pop(0)
    output.append(column_name)
    for row in rows:
        row = list(row)
        row.pop(0)
        l = []
        for data in row:
            data = str(data)
            data = data.replace('.',',')
            l.append(data)
        output.append(l)
    
    last = output[-1]
    first = output[1]
    file_name = f'{location_name} {first[0]} - {last[0]}.csv'
    with open(f'temp/{file_name}','w', newline='') as file_csv:
        writer = csv.writer(file_csv, delimiter=';')
        for row in output:
            writer.writerow(row)
    
    return file_name
