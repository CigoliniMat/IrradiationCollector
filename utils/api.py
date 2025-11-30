import cdsapi
import csv
import os

def irradiation(lon, lat, start_day, end_day, file_position="DeleteMe.csv"):
    '''Input example:
    lon / lon = 10.00
    start_day / end_day = "2024-01-01" #format YYYY-MM-DD
    file_position = "Example.csv" #irrilevant, get removed after reading the file

    Output example:
    {'2024-01-01': {'GHI': 100.02, 'DNI': 50.02054, 'DHI': 30, 'BNI': 20},
    '2024-01-02': {'GHI': 110, 'DNI': 60, 'DHI': 40, 'BNI': 25}}'''
    #check if target file exists, if yes remove it
    if os.path.exists(file_position):
        os.remove(file_position)

    #download the file from the API
    client = cdsapi.Client()
    dataset = 'cams-solar-radiation-timeseries'
    target = file_position
    params = {"sky_type": "observed_cloud",
                "location": {"longitude": lon, "latitude": lat},
                "altitude": ["-999."], #???
                "date": [f"{start_day}/{end_day}"],
                "time_step": "1day", #options = 1minute, 15minute, 1hour, 1day, 1month
                "time_reference": "universal_time", #universal_time or true_solar_time, irrilevant
                "format": "csv" #now CSV, but if i learn how to read cdf file, can switch to NETCDF
                }
    client.retrieve(dataset, params, target)

    #open and read the file
    with open(target, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        legend_passed = False
        output = {}
        list_values_to_return = ['GHI', 'BHI','DHI', 'BNI']

        for row in reader:
            if legend_passed:
                time_string = row['# Coding: utf-8'] #value like "2025-01-01T00:00:00.0/2025-01-01T01:00:00.0"
                values = row[None] #irradiation values
                date = time_string[:10] #date in format YYYY-MM-DD
                if date not in output:
                    output[date] = {}
                for value in list_values_to_return:
                    output[date][value] = float(values[values_column[value]]) #add check if error in coverting the value

            if row['# Coding: utf-8'] == '# Observation period':
                header = list(enumerate(row[None]))
                values_column = {}
                for text in header:
                    if text[1] in list_values_to_return:
                        values_column[text[1]] = int(text[0])
                legend_passed = True

    os.remove(target)

    return output
