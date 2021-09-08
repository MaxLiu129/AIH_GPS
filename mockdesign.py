from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import os
import sys
# change this to switch from real data program to random generated data program
import makememap_real as makememap
import numpy
import random
import math
from math import *   # duplicate? 
import datetime
from datetime import datetime
from datetime import timedelta
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash_extensions.javascript import Namespace
from dash.dependencies import Input, Output
import time
import threading
import csv


# global variables 7/2/2021
toggle_traj = False
toggle_outlier = False
outlier_index_counter = 0

map = None
def makemap():
    makememap.app.run_server(port=8080)
    map = makememap.Map()

thread = threading.Thread(target=makemap)
thread.start()
#main window
class Ui_MainWindow(QMainWindow):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"Main Window")
            
        MainWindow.setEnabled(True)
        #MainWindow.resize(1000, 600)
        MainWindow.showMaximized()
        MainWindow.setMouseTracking(False)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(30, 20, 900, 900))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        # Add Map viewer to Verical Layout
        self.webEngineView = QtWebEngineWidgets.QWebEngineView(self.centralwidget)
        # url = QtCore.QUrl('http://127.0.0.1:8050/')
        # QtCore.QUrl().fromLocalFile(os.path.split(os.path.abspath(__file__))[0]+r'index.html'
        self.webEngineView.load(QtCore.QUrl('http://127.0.0.1:8050/'))
        self.verticalLayout.addWidget(self.webEngineView)

        # outlier selection
        # Pressing button shows a dialog box  
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QtCore.QRect(1200, 300, 200, 30))

        # startDE objects, end and start time for time intervals
        self.startDE = QDateTimeEdit(self.centralwidget)
        self.startDE.setGeometry(1120, 150, 150, 30)
        self.startDE.setMinimumDate(QtCore.QDate.currentDate().addDays(-10000))
        self.startDE.setMaximumDate(QtCore.QDate.currentDate().addDays(10000))
        self.startDE.setDisplayFormat("dd.MM.yyyy hh:mm")
        
        self.endDE = QDateTimeEdit(self.centralwidget)
        self.endDE.setGeometry(1330, 150, 150, 30)
        self.endDE.setMinimumDate(QtCore.QDate.currentDate().addDays(-10000))
        self.endDE.setMaximumDate(QtCore.QDate.currentDate().addDays(10000))
        self.endDE.setDisplayFormat("dd.MM.yyyy hh:mm")
        
        # analysis window
        # button to open analysis window, showing data from start to end time.  
        self.showAnalysisBtn = QPushButton(self.centralwidget)
        self.showAnalysisBtn.setObjectName(u"showAnalysisBtn")
        self.showAnalysisBtn.setGeometry(QtCore.QRect(1200, 100, 200, 30))
        self.showAnalysisBtn.clicked.connect(self.toggle_window)

        # Human anomaly outlier annotate.
        self.pushButton_4 = QPushButton(self.centralwidget)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setGeometry(QtCore.QRect(1200, 350, 200, 30))
        self.pushButton_4.raise_()
        self.pushButton_4.setCheckable(True)
        self.pushButton_4.toggle()
        
        # toggle trajectory
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QtCore.QRect(1200, 50, 200, 30))
        self.comboBox = QComboBox(self.centralwidget)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QtCore.QRect(1200, 400, 200, 30))
        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QtCore.QRect(1200, 509, 200, 30))
        self.pushButton_3.clicked.connect(self.refresh)
        MainWindow.setCentralWidget(self.centralwidget)
        self.pushButton.raise_()
        self.verticalLayoutWidget.raise_()
        # self.horizontalSlider.raise_()
        self.pushButton_2.raise_()
        self.comboBox.raise_()
        self.pushButton_3.raise_()
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QtCore.QRect(0, 0, 955, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        QWidget.setTabOrder(self.pushButton_2, self.comboBox)
        # QWidget.setTabOrder(self.comboBox, self.horizontalSlider)
        # QWidget.setTabOrder(self.horizontalSlider, self.pushButton_3)
        QWidget.setTabOrder(self.pushButton_3, self.pushButton)
        QWidget.setTabOrder(self.pushButton_4, self.pushButton)

        # added for toggle trajectory 7/2/2021
        self.pushButton_2.setCheckable(True)
        self.pushButton_2.toggle()
        self.pushButton_2.clicked.connect(self.btnstate)

        # added for toggle outlier 7/7/2021
        self.pushButton.setCheckable(True)
        self.pushButton.toggle()
        self.pushButton.clicked.connect(self.btnstate_2)
        
        self.retranslateUi(MainWindow)
        # self.pushButton.clicked.connect(self.show_dialog)
        # QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.w = AnotherWindow()
    
    # def showAnalysisWindow(self):
    #     start = self.startDE.dateTime().toPyDateTime()
    #     end = self.endDE.dateTime().toPyDateTime()
    #     print(map.get_time_interval(start, end))

    # for toggling trajectory 7/2/2021
    def btnstate(self):
        global toggle_traj
        if self.pushButton_2.isChecked():
            toggle_traj = True
        else:
            toggle_traj = False
    
    def btnstate_2(self):
        global toggle_outlier
        if self.pushButton.isChecked():
            toggle_outlier = True
        else:
            toggle_outlier = False
    

    def show_dialog(self):
        msg = QMessageBox()
        msg.setWindowTitle("Confirmation")
        msg.setText("Are you sure?")
        msg.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
        x = msg.exec_()

    def refresh(self):
        self.webEngineView.reload()

    def selectionchange(self, i):
        ## T S R
        if i == 0:
            map.change_color_to_time()
        if i == 1:
            map.change_color_to_speed()
        if i == 2:
            map.change_color_to_risk()
    
        self.webEngineView.reload()

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtCore.QCoreApplication.translate("Main Window", u"Window for Monitoring", None))
        self.showAnalysisBtn.setText(QtCore.QCoreApplication.translate("MainWindow", u"Show Analysis Window", None))
        self.pushButton.setText(QtCore.QCoreApplication.translate("MainWindow", u"Random Outlier Generator", None))
        self.pushButton_2.setText(QtCore.QCoreApplication.translate("MainWindow", u"Toggle Trajectory", None))
        self.pushButton_4.setText(QtCore.QCoreApplication.translate("MainWindow", u"Human Anomaly Outlier Annotate", None))
        self.comboBox.setItemText(0, QtCore.QCoreApplication.translate("MainWindow", u"Time", None))
        self.comboBox.setItemText(1, QtCore.QCoreApplication.translate("MainWindow", u"Speed", None))
        self.comboBox.setItemText(2, QtCore.QCoreApplication.translate("MainWindow", u"Risk", None))
        self.comboBox.currentIndexChanged.connect(self.selectionchange)
        self.pushButton_3.setText(QtCore.QCoreApplication.translate("MainWindow", u"Refresh", None))
    # retranslateUi

    def toggle_window(self, checked):
        start = self.startDE.dateTime().toPyDateTime()
        end = self.endDE.dateTime().toPyDateTime()
        if self.w.isVisible():
            self.w.hide()
        else:
            self.w.show()
        f = open("result1.txt", "w")
        f.write(ui.startDE.dateTime().toPyDateTime().strftime("%m/%d/%Y, %H:%M:%S") + '\n')
        f.write(ui.endDE.dateTime().toPyDateTime().strftime("%m/%d/%Y, %H:%M:%S")+ '\n')
        f.close()
        print(makememap.get_time_interval(ui.startDE.dateTime().toPyDateTime(), ui.endDE.dateTime().toPyDateTime()))

class AnotherWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.webEngineView = QtWebEngineWidgets.QWebEngineView()
        # url = QtCore.QUrl('http://127.0.0.1:8050/')
        # QtCore.QUrl().fromLocalFile(os.path.split(os.path.abspath(__file__))[0]+r'index.html'
        self.webEngineView.load(QtCore.QUrl('http://127.0.0.1:8080/'))
        self.setWindowTitle(QtCore.QCoreApplication.translate("Analysis Window", u"Window for Analysis", None))
        layout.addWidget(self.webEngineView)


def run():
    # declare some variables used for cvs reader.
    global locations
    
    datetime_list = []
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


    # for toggling the outlier selection, we firstly randomly generate the outlier points first and 
    # then use the trigger variable to indicate whether or not to show it to the user.
    # for now, we set the outlier data rate to be [50%]    (completed: 7/12/2021)
    outlier_rate = 0.5
    outlier_count = int(data_length * outlier_rate)
    
    outlier_index = []
    outlier_index = random.sample(range(0, data_length-1), outlier_count)
    outlier_index.sort()
    
    print(outlier_index)
    outlier_list = [0] * data_length # indicates if the data is selected as "outlier" / all data are set to be ZERO at first
    
    # now we add a tag to the data that has been selected as "outlier"
    for i in outlier_index:
        for j in range(data_length):
            if i == j:
                outlier_list[i] = 1
                
    locations_base = [] #the data set that will be rendered into the streaming map on main dashboard.
    locations_outlier = []  # the outlier of locations will be stored in this variable.
    start_location=[locations[0][0], locations[0][1]]

    at_risk = numpy.random.uniform(low=0.0, high=1.1, size=(data_length,))
    start_time = 0
    map_dir = "index.html"
    MINUTES_IN_DAY = 1440
    start_date = datetime.now()

    times = list(range(0, data_length))
    time_index = 0
    datetimes = []

    for i in range(len(times)):
        noise = random.randint(1,5)
        times[i] = (times[i] + noise)
        datetimes.append(start_date + timedelta(minutes=times[i]))

    datetimeindex = pd.Series(range(0, data_length), index=datetimes)

    
    #locations_base.append([x[i] + start_location[0], y[i] + start_location[1]])

    ns = Namespace("dlx", "scatter")

    new_markers = [dl.Marker(dl.Tooltip(f"({pos[0]}, {pos[1]}), time:{datetime_list[i]}"), 
        position=pos, 
        id="marker{}".format(i)) for i, pos in enumerate(locations)]

    cluster = dl.MarkerClusterGroup(id="new_markers", 
        children=new_markers, 
        options={"polygonOptions": {"color": "blue"}})

    patterns = [dict(offset='0%', repeat='0', marker={})]
    polyline = dl.Polyline(positions=[locations],id="id_polyline")
    marker_pattern = dl.PolylineDecorator(id="id_marker_pattern", children=polyline, patterns=patterns)
    
    
    app = dash.Dash(external_scripts=["https://cdnjs.cloudflare.com/ajax/libs/chroma-js/2.1.0/chroma.min.js"])
    app.layout = html.Div(
        html.Div([
            dl.Map([dl.TileLayer(), cluster, marker_pattern, dl.LayerGroup(id="layer")],
            id="map",
            center=start_location, zoom=16, style={'height': '100vh'}),
            #html.Div(id='live-update-text'),
            dcc.Interval(
                id="interval",
                interval=1*1000, # in milliseconds
                n_intervals=0)
        ])
    )

    @app.callback(Output('map', 'center'), [Input('interval', 'n_intervals')])
    def update_focus(c):
        center = [locations[c][0], locations[c][1]]
        return center
    
    # update the lines draw between points
    @app.callback(Output('id_marker_pattern','children'), [Input('interval','n_intervals')])
    def update_polyline(b):
        global toggle_traj
        if toggle_traj == True:
            polyline = dl.Polyline(positions=locations_base)
        else:
            polyline = dl.Polyline(positions=[])
        return polyline
    
    
    # update the data point on the map
    
    @app.callback(Output('new_markers','children'), [Input('interval', 'n_intervals')])
    def update_metrics(a):
        global toggle_outlier
        global outlier_index_counter
        
        first_outlier_index = outlier_index[outlier_index_counter]
        locations_base.append([locations[a][0], locations[a][1]])
        # check if the current locations match the numbers in the "outlier_list"
        for i in outlier_index:
            if i == a:
                locations_outlier.append([locations[a][0], locations[a][1]])    
        if(len(locations_base) > 100):
            locations_base.pop(0)
        if(a > first_outlier_index + 100):
            locations_outlier.pop(0)
            outlier_index_counter += 1
            
        if toggle_outlier == True:
            new_markers = [dl.Marker(dl.Tooltip(f"({pos[0]}, {pos[1]}), time:{datetime_list[i]}"), position=pos, id="marker{}".format(i)) for i, pos in enumerate(locations_outlier)]
        else:
            new_markers = [dl.Marker(dl.Tooltip(f"({pos[0]}, {pos[1]}), time:{datetime_list[i]}"), position=pos, id="marker{}".format(i)) for i, pos in enumerate(locations_base)]
        return new_markers

    def rgb_to_hex(rgb):
        return ('%02x%02x%02x' % rgb)

    def get_time_interval(sd, ed):
        indices = datetimeindex[sd:ed].to_numpy()
        print(indices)

    def change_color_to_time():
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
        for i in range(len(locations)):
            time = times[i]
            risk = math.trunc(at_risk[i])            
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
    app.run_server(port=8050)

if __name__ == "__main__":
    thread = threading.Thread(target=run)
    thread.start()
    app = QtWidgets.QApplication(sys.argv)
    Window = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(Window)
    #setLayout(ui.vLayout)
    
    Window.show()
    app.exec_()

    