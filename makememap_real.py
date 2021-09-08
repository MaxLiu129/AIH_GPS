import csv
import folium
import numpy
import random
import math
from math import *
import datetime
from datetime import datetime
from datetime import timedelta
import pandas as pd
import dash
import dash_html_components as html
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash_extensions.javascript import Namespace
from dash.dependencies import Input, Output
import os   # test the file




# new work
datetime_list = []

# declare some variables used for cvs reader.
locations = []
time_info = ""
date = []           # the date of the data
time = []           # the time of the data
address = []        # the address of the data
deviceName = ""     # record the device name from the data
data_length = 0     # the total amount of the data
data_speed = []     # store the speed at each data point  # used later below.

# read and store data from csv file.
with open('test.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0  # this is only because the first line of the csv file is the subtitles.
    for row in csv_reader:
        if line_count > 0:
            locations.append([row[2],row[3]])
            datetime_list.append(datetime.strptime(row[6], "%m/%d/%Y %I:%M:%S %p"))
            address.append(row[4])
            deviceName = row[5]
        line_count += 1
data_length = line_count - 1


# calculate the speed of each data point:
R = 6371000 # earth radius
degToRad = float(math.pi / 180)
temp_speed = 0
for i in range(data_length):
    if i == 0 or i == (data_length - 1):
        temp_speed = 0
        data_speed.append(temp_speed)
    else:
        temp_dic1 = float(R) * degToRad * math.sqrt(math.pow(math.cos(float(locations[i-1][0]) * degToRad ) * (float(locations[i-1][1]) - float(locations[i][1])) , 2) + math.pow(float(locations[i-1][0]) - float(locations[i][0]), 2))
        temp_dic2 = float(R) * degToRad * math.sqrt(math.pow(math.cos(float(locations[i][0]) * degToRad ) * (float(locations[i][1]) - float(locations[i+1][1])) , 2) + math.pow(float(locations[i][0]) - float(locations[i+1][0]), 2))
        temp_time1 = (datetime_list[i].hour - datetime_list[i-1].hour) * 3600 + (datetime_list[i].minute - datetime_list[i-1].minute) * 60 + (datetime_list[i].second - datetime_list[i-1].second)
        temp_time2 = (datetime_list[i+1].hour - datetime_list[i].hour) * 3600 + (datetime_list[i+1].minute - datetime_list[i].minute) * 60 + (datetime_list[i+1].second - datetime_list[i].second) 
        if temp_time1 == 0 and temp_time2 == 0:
            temp_speed = 0
        elif temp_time1 == 0:
            temp_speed = temp_dic2 / temp_time2
        elif temp_time2 == 0:
            temp_speed = temp_dic1 / temp_time1
        else:
            temp_speed = (temp_dic1 / temp_time1 + temp_dic2 / temp_time2) / 2
        data_speed.append(round(temp_speed, 2))

# above is TESTED
# temporary time codes: (tested)
startDE_object = None
endDE_object = None
start_time_index = 0
end_time_index = 0
new_locations = []
new_time = []
if os.stat("result1.txt").st_size == 0:
    print('error')
else:
    f_txt = open("result1.txt", "r")
    startDE = f_txt.readline().rstrip('\n')
    endDE = f_txt.readline().rstrip('\n')
    startDE_object = datetime.strptime(startDE, "%m/%d/%Y, %H:%M:%S")
    endDE_object = datetime.strptime(endDE, "%m/%d/%Y, %H:%M:%S") 
    # testcase
    # startDE_object = datetime.strptime('4/22/2020 2:27:49 PM', '%m/%d/%Y %I:%M:%S %p')
    # endDE_object = datetime.strptime('4/22/2020 2:29:35 PM', '%m/%d/%Y %I:%M:%S %p')  
    for i in range(0, data_length):
        if datetime_list[i] < startDE_object:
            start_time_index += 1
    for j in range(0, data_length):
        if datetime_list[j] > endDE_object:
            end_time_index += 1 
    end_time_index = data_length - end_time_index

    # make the new locations data:
    for k in range(start_time_index, end_time_index):
        new_locations.append([locations[k][0], locations[k][1]])
        new_time.append(datetime_list[k])
print(end_time_index)

f_txt.close()
# start_location would be the first data stream. 
# (it needs to be modified when time scaling is changing)

# if new_locations is not None:
#     start_location = [new_locations[0][0], new_locations[0][1]]
# else:
start_location = locations[0]
#[locations[0][0], locations[0][1]]

# create the map with the start_location and start zooming level
m = folium.Map(location=start_location, zoom_start=1)
# for risk display
at_risk = numpy.random.uniform(low=0.0, high=1.1, size=(data_length,))


map_dir = "index.html"  # this is not used... what is it?

# this part is about time initialization,
# no need to change now. 5/29/2021 
start_time = 0
MINUTES_IN_DAY = 1440
start_date1 = datetime.now()

times = list(range(0, data_length))

# # todo

datetimes = []
for i in range(len(times)):
    # No need
    # noise = random.randint(1,5)
    # times[i] = (times[i] + noise)
    # No need
    datetimes.append(start_date1 + timedelta(minutes=times[i]))

datetimeindex = pd.Series(range(0, data_length), index=datetimes)
# todo

# randomly generated speed values:
speed = []
for i in range(data_length):
    speed.append("1")
    
# this part construct the map with variables input here as well.
ns = Namespace("dlx", "scatter")
markers = [dl.Marker(dl.Tooltip(f"Location: ({pos[0]}, {pos[1]})\nTime: {new_time[i]}\nSpeed:{data_speed[i]} m/s"), position=pos, id="marker{}".format(i)) for i, pos in enumerate(new_locations)]
cluster = dl.MarkerClusterGroup(id="markers", children=markers,options={"polygonOptions": {"color": "red"}})
app = dash.Dash(external_scripts=["https://cdnjs.cloudflare.com/ajax/libs/chroma-js/2.1.0/chroma.min.js"])
# the zoom variable here controls the analysis window start zoom level.
# but somehow the result is not acceptable.
app.layout = html.Div([
    dl.Map(center=start_location, zoom=12,children=[dl.TileLayer(),cluster, 
    dl.LayerGroup(id="layer")], id="map",
    style={'height': '100vh','margin': "auto"})
])


def rgb_to_hex(rgb):
    return ('%02x%02x%02x' % rgb)

def get_time_interval(sd, ed):

    indices = datetimeindex[sd:ed].to_numpy()
    return indices

def change_color_to_time():
    #folium.PolyLine(locations).add_to(new_map)
    for i in range(len(locations)):
        time = times[i]
        r = 255 - math.trunc(255 * (time / MINUTES_IN_DAY))
        color_tuple = (r, r, r)
        rgb = rgb_to_hex(color_tuple)
        icon = {
            "iconUrl": f"http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|{rgb}&chf=a,s,ee00FFFF",
            "iconSize": [20, 30],  # size of the icon
        }
        markers[i].icon = icon
    

def change_color_to_risk():
    #new_map = folium.Map(location=start_location)
    #folium.PolyLine(locations).add_to(new_map)
    for i in range(len(locations)):
        time = times[i]
        risk = math.trunc(at_risk[i])
        # color_tuple = (255 * (risk), 255 * (1 - risk), 0)
        # rgb = rgb_to_hex(color_tuple)
        
        if (risk == 1):
            icon = {
                "iconUrl": "http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|FF0000&chf=a,s,ee00FFFF",
                "iconSize": [20, 30],  # size of the icon
            }
        else:
            icon = {
                "iconUrl": "http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|00FF00&chf=a,s,ee00FFFF",
                "iconSize": [20, 30],  # size of the icon
            }
        markers[i].icon = icon
        print("risk")

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

def change_color_to_speed():
    new_map = folium.Map(location=start_location,control_scale=True) 
    speed=0
    avewalk=0.084
 
    speeddiff=0
        
    for i in range(len(locations)):
        if i == 0:
            speed=0
        elif (times[i]-times[i-1])==0:
            speed=0
        else:
            #coords_1 = [locations[i][0], locations[i][1]]
            #coords_2 = [locations[i-1][0], locations[i-1][1]]
            #distance = h3.point_dist(coords_1,coords_2)
            R = 6373.0
            lat1 = radians(locations[i][0])
            lon1 = radians(locations[i][1])
            lat2 = radians(locations[i-1][0])
            lon2 = radians(locations[i-1][1])
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = 2
            ##sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
            c = 2 
            ##2 * atan2(sqrt(a), sqrt(1 - a))
            distance = R * c
            speed = abs(distance / (times[i]-times[i-1]))
        
        speeddiff=speed*1000/60 - 1.4
        r=clamp(100+speeddiff*300,0,255)    #grey normal, yellow fast, blue slow
        g=clamp(100+speeddiff*100,0,255)
        b=clamp(100-speeddiff*100,0,255)
        color_tuple = (int(r), int(g), int(b))
        rgb = rgb_to_hex(color_tuple)
        icon = {
            "iconUrl": f"http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|{rgb}&chf=a,s,ee00FFFF",
            "iconSize": [20, 30],  # size of the icon
        }
        markers[i].icon = icon

#change_color_to_speed()
#get_time_interval(str(datetime.datetime.now()), str(datetime.datetime.now() + timedelta(minutes=4)))
if __name__ == '__main__':
    app.run_server(port=8080)