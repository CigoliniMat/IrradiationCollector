from flask import Flask, render_template, request
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
    name = request.form.getlist('name')[0]
    lat = request.form.getlist('lat')[0]
    lon = request.form.getlist('lon')[0]
    description = request.form.getlist('description')[0]
    validation = True
    result = f.add_location(name, lat, lon, description)
    return result

if __name__ == '__main__':
    app.run(debug=True)

