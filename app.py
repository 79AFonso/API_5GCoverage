import math
import csv
from flask import Flask, render_template, jsonify, send_file, request

app = Flask(__name__, static_url_path='/static')

data_atcll = []
data_gnb = []

def degrees_to_radians(degrees):
    return degrees * math.pi / 180.0

def haversine_distance(lat1, lon1, lat2, lon2):
    # Radius of the Earth in kilometers
    earth_radius = 6371.0

    # Convert latitude and longitude from degrees to radians
    lat1_rad = degrees_to_radians(lat1)
    lon1_rad = degrees_to_radians(lon1)
    lat2_rad = degrees_to_radians(lat2)
    lon2_rad = degrees_to_radians(lon2)

    # Haversine formula
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = earth_radius * c

    return distance

def is_point_inside_circle(center_latitude, center_longitude, radius, point_latitude, point_longitude):
    # Calculate the distance between the center and the given point
    distance = haversine_distance(center_latitude, center_longitude, point_latitude, point_longitude)

    # Compare the distance with the radius of the circle
    return distance <= radius

@app.route('/')
def index():
    with open('atcll.csv', 'r') as file:
        reader = csv.reader(file)
        for idx, row in enumerate(reader):
            if idx != 0:
                data_atcll.append(row)
    with open('data.csv', 'r') as file:
        reader = csv.reader(file)
        for idx, row in enumerate(reader):
            if idx != 0:
                data_gnb.append(row)
                
    
    return render_template('index.html', data_atcll=data_atcll, data_gnb=data_gnb)

@app.route('/get_csv')
def get_csv():
    return send_file('atcll.csv', mimetype='text/csv')

@app.route('/run_python_code')
def run_python_code():

    latitude = float(request.args.get('latitude'))
    longitude = float(request.args.get('longitude'))


    
    for idx, row in enumerate(data_atcll):
        if idx != 0:
            
            if is_point_inside_circle(float(row[1]), float(row[2]), 0.1, latitude, longitude):
                result_message = "yes"
                print("Yes it is inside")
            else:
                result_message = "no"
            

    return jsonify({'message': result_message})
    
    


if __name__ == '__main__':
    app.run(debug=True)
