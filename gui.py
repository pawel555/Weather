import sys
import vtk
import time
import PyQt5
from PyQt5.QtWidgets import *
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from get_data_api import GetDataFromOWMApi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from weather_3d_vtk_reader import Weather3D


class Activity(QWidget):
    def __init__(self, lay, parent=None):
        QWidget.__init__(self, parent)

        self.fore = None

        # prepare vtk window - now its just an empty stub
        self.we3d = Weather3D()
        self.vtkWidget = QVTKRenderWindowInteractor()

        # now its time to set up checkboxes for 3d plot
        self.temperatures_checkbox = QCheckBox()
        self.rainfalls_checkbox = QCheckBox()
        self.snowfalls_checkbox = QCheckBox()
        self.press_checkbox = QCheckBox()
        self.wind_checkbox = QCheckBox()
        self.clouds_checkbox = QCheckBox()

        self.temperatures_checkbox.setChecked(True)
        self.rainfalls_checkbox.setChecked(True)
        self.snowfalls_checkbox.setChecked(True)
        self.press_checkbox.setChecked(True)
        self.wind_checkbox.setChecked(True)
        self.clouds_checkbox.setChecked(True)

        self.temperatures_checkbox.stateChanged.connect(self.checkbox_state_changed)
        self.rainfalls_checkbox.stateChanged.connect(self.checkbox_state_changed)
        self.snowfalls_checkbox.stateChanged.connect(self.checkbox_state_changed)
        self.press_checkbox.stateChanged.connect(self.checkbox_state_changed)
        self.wind_checkbox.stateChanged.connect(self.checkbox_state_changed)
        self.clouds_checkbox.stateChanged.connect(self.checkbox_state_changed)

        lay.addWidget(QLabel("Temperature:"),  0, 4, 1, 1)
        lay.addWidget(self.temperatures_checkbox, 0, 5, 1, 1)

        lay.addWidget(QLabel("Rain:"), 1, 4, 1, 1)
        lay.addWidget(self.rainfalls_checkbox, 1, 5, 1, 1)

        lay.addWidget(QLabel("Snow:"), 0, 6, 1, 1)
        lay.addWidget(self.snowfalls_checkbox, 0, 7, 1, 1)

        lay.addWidget(QLabel("Pressure:"), 1, 6, 1, 1)
        lay.addWidget(self.press_checkbox, 1, 7, 1, 1)

        lay.addWidget(QLabel("Wind:"), 0, 8, 1, 1)
        lay.addWidget(self.wind_checkbox, 0, 9, 1, 1)

        lay.addWidget(QLabel("Clouds:"), 1, 8, 1, 1)
        lay.addWidget(self.clouds_checkbox, 1, 9, 1, 1)

        # a figure instance to plot on
        self.figure = Figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvasQTAgg(self.figure)

        lay.addWidget(self.canvas, 2, 0, 4, 4)

        self.date_lst = QListWidget()
        lay.addWidget(self.date_lst, 0, 1, 1, 1)
        self.city_lst = QListWidget()
        lay.addWidget(self.city_lst, 1, 1, 1, 1)
        self.date_lst.itemClicked.connect(self.hax_method)
        self.city_lst.itemClicked.connect(self.show_plot)
        self.city_lst.addItems(['Warsaw, PL', 'Gdansk, PL', 'Pila, PL', 'Torun, PL', 'Plock, PL', 'Poznan, PL', 'Opole, PL',
                       'Krakow, PL', 'Lublin, PL', 'Rzeszow, PL'])
        self.dates = self.set_dates()
        self.date_lst.addItems(self.dates)
        self.date_lst.setCurrentRow(1)
        self.city_lst.setCurrentRow(1)

        self.lay = lay

    def hax_method(self):
        self.checkbox_state_changed(1)
        self.show_plot()

    def get_list(self):
        return self.date_lst

    def get_vtk_widget(self):
        return self.vtkWidget

    def set_dates(self):
        import time

        curr_day = int(time.strftime("%d"))
        curr_month = int(time.strftime("%m"))
        curr_year = int(time.strftime("%Y"))

        dates_list = []

        for i in range(curr_day, curr_day + 5):
            if i > 31:
                dates_list.append(str(curr_year) + '-0' + str(curr_month + 1) + '-' + str(i - 31))
            else:
                dates_list.append(str(curr_year) + '-0' + str(curr_month) + "-" + str(i))

        return dates_list

    def show_plot(self):

        date = str(self.date_lst.currentItem().text())
        city = str(self.city_lst.currentItem().text())

        getter = GetDataFromOWMApi()
        self.fore = getter.main(city, date)

        hours = []
        temperatures = []
        rainfalls = []
        snowfalls = []
        press = []
        wind = []
        clouds = []

        for weather in self.fore:

            hours.append(weather[0])
            temperatures.append(weather[3]['temp'])
            try:
                rainfalls.append(weather[1]['3h'])
            except KeyError:
                rainfalls.append(0)

            try:
                snowfalls.append(weather[4]['3h'])
            except KeyError:
                snowfalls.append(0)

            press.append(weather[2]['press'])
            wind.append(weather[5]['speed'])
            clouds.append(weather[6])

        # print(temperatures)
        # print(hours)
        # print(press)
        # print(rainfalls)
        # print(snowfalls)

        temp_ax = self.figure.add_subplot(611)
        temp_ax.clear()
        temp_ax.set_ylabel('Temperature\n[C]')
        temp_ax.plot(hours, temperatures, color='red', marker='o', linestyle='dashed', linewidth=2, markersize=12)
        temp_ax.grid()
        temp_ax.get_xaxis().set_ticklabels([])

        rain_ax = self.figure.add_subplot(612)
        rain_ax.clear()
        rain_ax.set_ylabel('Rain\n[mm]')
        rain_ax.plot(hours, rainfalls, color='blue', marker='o', linestyle='dashed', linewidth=2, markersize=12)
        rain_ax.grid()
        rain_ax.get_xaxis().set_ticklabels([])

        snow_ax = self.figure.add_subplot(613)
        snow_ax.clear()
        snow_ax.set_ylabel('Snow\n[mm]')
        snow_ax.plot(hours, snowfalls, color='darkblue', marker='o', linestyle='dashed', linewidth=2, markersize=12)
        snow_ax.grid()
        snow_ax.get_xaxis().set_ticklabels([])

        press_ax = self.figure.add_subplot(614)
        press_ax.clear()
        press_ax.set_ylabel('Pressure\n[hPa]')
        press_ax.plot(hours, press, color='purple', marker='o', linestyle='dashed', linewidth=2, markersize=12)
        press_ax.grid()
        press_ax.get_xaxis().set_ticklabels([])

        wind_ax = self.figure.add_subplot(615)
        wind_ax.clear()
        wind_ax.set_ylabel('Wind\n[m/s]')
        wind_ax.plot(hours, wind, color='green', marker='o', linestyle='dashed', linewidth=2, markersize=12)
        wind_ax.grid()
        wind_ax.get_xaxis().set_ticklabels([])

        clouds_ax = self.figure.add_subplot(616)
        clouds_ax.clear()
        clouds_ax.set_ylabel('Clouds\n[%]')
        clouds_ax.plot(hours, clouds, color='gray', marker='o', linestyle='dashed', linewidth=2, markersize=12)
        clouds_ax.grid()

        # refresh canvas
        self.canvas.draw()

    def checkbox_state_changed(self, int):
        checkboxes = []
        if self.temperatures_checkbox.isChecked():
            checkboxes.append({"temp": True})
        else:
            checkboxes.append({"temp": False})

        if self.rainfalls_checkbox.isChecked():
            checkboxes.append({"rain": True})
        else:
            checkboxes.append({"rain": False})

        if self.snowfalls_checkbox.isChecked():
            checkboxes.append({"snow": True})
        else:
            checkboxes.append({"snow": False})

        if self.press_checkbox.isChecked():
            checkboxes.append({"pressure": True})
        else:
            checkboxes.append({"pressure": False})

        if self.wind_checkbox.isChecked():
            checkboxes.append({"wind": True})
        else:
            checkboxes.append({"wind": False})

        if self.clouds_checkbox.isChecked():
            checkboxes.append({"clouds": True})
        else:
            checkboxes.append({"clouds": False})

        date = str(self.date_lst.currentItem().text())

        self.vtkWidget = self.we3d.main(GetDataFromOWMApi().return_weather_for_all_cities(date), date, checkboxes)

        self.vtkWidget.setFixedWidth(800)
        self.vtkWidget.setFixedHeight(700)
        self.lay.addWidget(self.vtkWidget, 2, 4, 4, 5)


app = QApplication(sys.argv)

lay = QGridLayout()

lbl1 = QLabel("Choose date:")
lay.addWidget(lbl1, 0, 0, 1, 1)

lbl2 = QLabel("Choose city:")
lay.addWidget(lbl2, 1, 0, 1, 1)

choices_list = Activity(lay)

choices_list.show_plot()

choices_list.checkbox_state_changed(1)

w = QWidget()
w.setFixedWidth(1800)
w.setFixedHeight(1040)
w.move(100, 100)
w.setLayout(lay)
w.show()

app.exec_()
