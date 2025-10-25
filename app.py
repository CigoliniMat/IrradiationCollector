from flask import Flask, render_template, request, jsonify, send_file
import script as f
import time

app = Flask(__name__)

@app.route('/')
def main():
    locations_list = f.get_locations()
    return render_template('main.html', locations_list=locations_list)

@app.route('/select_location', methods=['POST'])
def select_location():
    selection = request.form.getlist('selection')
    if len(selection) > 0:
        selection = selection[0]
        selection = int(selection)
        result = f'you select location: {selection}'
    else:
        result = "you don't select any location"
    
    return jsonify(result), 200
    
@app.route('/add_location', methods=['POST'])
def add_location():
    name = request.form['name']
    lat = request.form['lat']
    lon = request.form['lon']
    description = request.form.get('description','')
    validation = True #check if verify (future project)
    result = f.add_location(name, lat, lon, description)
    if result == 'location added succesfully':
        result = f.get_locations()



    return jsonify(result), 200

@app.route('/download_csv', methods=['POST'])
def download_csv():
    selection = request.form.getlist('selection')
    if len(selection) > 0:
        selection = selection[0]
        selection = int(selection)
        csv_path = f.download_csv(selection)
        csv_path = f'temp/{csv_path}'
        return send_file(csv_path, as_attachment=True), 200
        
    else:
        result = "you don't select any location"
        print(result)
    
@app.route('/update_api', methods=['POST'])
def update_api():
    f.insert_irradiation()

    result = True
    return jsonify(result), 200

@app.route('/delete_location', methods=['POST'])
def delete_location():
    selection = request.form.getlist('selection')
    if len(selection) > 0:
        selection = selection[0]
        selection = int(selection)
        f.delete_location(selection)
        result = f.get_locations()
    else:
        result = "you don't select any location"
    
    return jsonify(result), 200


if __name__ == '__main__':
    app.run(debug=True)

