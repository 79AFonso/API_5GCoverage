import math
import csv
from flask import Flask, render_template, jsonify, send_file, request
from math import radians, cos, sin, asin, sqrt, atan2, degrees

app = Flask(__name__, static_url_path='/static')

data_atcll = []
data_gnb = []
list_coords = []
count=0

def ass():
    global count
    count=count+1
    print(count)

def degrees_to_radians(degrees):
    return degrees * math.pi / 180.0



def haversine_distance(lat1, lon1, lat2, lon2):
    longitude_distance = radians(lon2) - radians(lon1)
    latitute_distance = radians(lat2) - radians(lat1)
    haversine_distance = 2 * 6371.0 * asin(sqrt(sin(latitute_distance / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(longitude_distance / 2) ** 2))
    return  round(haversine_distance, 3)


def is_point_inside_circle(center_latitude, center_longitude, radius, point_latitude, point_longitude):
    # Calculate the distance between the center and the given point
    distance = haversine_distance(center_latitude, center_longitude, point_latitude, point_longitude)

    # Compare the distance with the radius of the circle

    return distance <= radius

def calculate_midpoint(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Calculate the midpoint
    dlon = lon2 - lon1
    Bx = math.cos(lat2) * math.cos(dlon)
    By = math.cos(lat2) * math.sin(dlon)
    lat3 = math.atan2(math.sin(lat1) + math.sin(lat2), math.sqrt((math.cos(lat1) + Bx) ** 2 + By ** 2))
    lon3 = lon1 + math.atan2(By, math.cos(lat1) + Bx)

    # Convert the result back to degrees
    lat3 = math.degrees(lat3)
    lon3 = math.degrees(lon3)

    return lat3, lon3

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

    return render_template('index.html', data_atcll=data_atcll, data_gnb=data_gnb, list_coords=list_coords)

@app.route('/get_csv')
def get_csv():
    return send_file('atcll.csv', mimetype='text/csv')

@app.route('/run_python_code')
def run_python_code():

    latitude = float(request.args.get('latitude'))
    longitude = float(request.args.get('longitude'))
    
    '''for row in data_gnb:
        if is_point_inside_circle(float(row[1]), float(row[2]), float(row[6]), latitude, longitude) and (float(row[5]) > 5):
            return jsonify({'message': "yes"})
        elif (float(row[5]) <= 5):
            result_message = "no"
            for row_atcll in data_atcll:
                if is_point_inside_circle(float(row_atcll[1]), float(row_atcll[2]), 0.1, latitude, longitude):
                    midpoint_lat, midpoint_lon = calculate_midpoint(float(row_atcll[1]), float(row_atcll[2]), latitude, longitude)
                    list_coords.append([midpoint_lat, midpoint_lon])
                    ass()
                    print(str(latitude) +" "+" "+ str(longitude) + " " + row[5])
                    return jsonify({'message': result_message})'''
    
    result_message = "yes"  # Set a default value

    for row_atcll in data_atcll:
        if is_point_inside_circle(float(row_atcll[1]), float(row_atcll[2]), 0.1, latitude, longitude):
            for row in data_gnb:
                if is_point_inside_circle(float(row[1]), float(row[2]), 3, latitude, longitude):
                    result_message = "no"
                    midpoint_lat, midpoint_lon = calculate_midpoint(float(row_atcll[1]), float(row_atcll[2]), latitude, longitude)
                    list_coords.append([midpoint_lat, midpoint_lon])
                    ass()
                    return jsonify({'message': result_message})

    return jsonify({'message': result_message})

    
    
if __name__ == '__main__':
    app.run(debug=True)
