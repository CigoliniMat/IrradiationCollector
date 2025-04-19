from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def show_list():
    locations_list = [
        {'ID':1,'name': 'Orzivecchi (BS)', 'lat': 10.2555, 'lon':45.4555},
        {'ID':2,'name': 'Settimo Torinese (TO)', 'lat': 10.2555, 'lon':45.4555},
        {'ID':3,'name': 'Dolcè (VR)', 'lat': 10.2555, 'lon':45.4555},
        {'ID':4,'name': 'Settimo Torinese (TO)', 'lat': 10.2555, 'lon':45.4555},
    ]
    return render_template('list.html', locations_list=locations_list)

@app.route('/select_location', methods=['POST'])
def select_location():
    selection = request.form.getlist('selection')[0]
    selection = int(selection)
    return f"you select location: {selection}" if selection else "you don't select any location"

if __name__ == '__main__':
    app.run(debug=True)

