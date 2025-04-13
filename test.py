import cdsapi
import csv
import os

#just dowload file, think about give output (maybe a dict?)
def irradiation_api(lon, lat, start_day, end_day, intervall, file_position):
    client = cdsapi.Client()
    dataset = 'cams-solar-radiation-timeseries'
    target = file_position
    params = {'sky_type': 'observed_cloud',
                'location': {'longitude': lon, 'latitude': lat},
                'altitude': ['-999.'],
                'date': [f'{start_day}/{end_day}'],
                'time_step': intervall,
                'time_reference': 'universal_time', #universal_time or true_solar_time
                'format': 'csv' #now CSV, but if i learn how to read cdf file, can switch to NETCDF
                }
    client.retrieve(dataset, params, target)

def read_csv(target):
    with open(target, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        legend_passed = False
        output = {}
        list_values_to_return = ['GHI', 'BHI','DHI', 'BNI']

        for row in reader:
            #take the row of the header of the table and find th number of the column where is is the value to return
            if row['# Coding: utf-8'] == '# Observation period':
                header = list(enumerate(row[None]))
                values_column = {}
                for text in header:
                    if text[1] in list_values_to_return:
                        values_column[text[1]] = int(text[0])
                legend_passed = True

            if legend_passed:
                time_string = row['# Coding: utf-8'] #value like "2025-01-01T00:00:00.0/2025-01-01T01:00:00.0"
                values = row[None] #irradiation values
                date = time_string[:10] #date in format YYYY-MM-DD
                if date not in output:
                    output[date] = {}
                for value in list_values_to_return:
                    output[date][value] = values[values_column[value]]

            
        #os.remove(target)
        #delete the file after reading it, to save space in the computer
        return output

def write_db(target, data):
    pass
        


lon = 10
lat = 45
start_day = '2024-01-01' #format YYYY-MM-DD
end_day = '2025-01-01'
value_intervall = '1day' #options = 1minute, 15minute, 1hour, 1day, 1month
file_position = 'private/Test.csv' #name and position where the file from the API will be saved

a = read_csv(file_position)
print(a)




