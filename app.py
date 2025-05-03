from flask import Flask, render_template, request, jsonify
import script as f

app = Flask(__name__)

@app.route('/')
def main():
    locations_list = f.get_locations()
    return render_template('main.html', locations_list=locations_list)

@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/select_location', methods=['POST'])
def select_location():
    selection = request.form.getlist('selection')
    if len(selection) > 0:
        selection = selection[0]
        selection = int(selection)
        return f"you select location: {selection}"
    else:
        return "you don't select any location"
    
@app.route('/add_location', methods=['POST'])
def add_location():
    name = request.form['name']
    lat = request.form['lat']
    lon = request.form['lon']
    description = request.form.get('description','')
    validation = True #
    result = f.add_location(name, lat, lon, description)
    if result == 'location added succesfully':
        result = f.get_locations()



    return jsonify(result), 200


if __name__ == '__main__':
    app.run(debug=True)

