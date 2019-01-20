import sys
import vtk
import time


import PyQt5
from PyQt5.QtWidgets import *
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from get_data_api import GetDataFromOWMApi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


# class ImportButton(QWidget):
#     def __init__(self, lay, lst, parent=None):
#         QWidget.__init__(self, parent)
#         self.btn = QPushButton('Select files to load:')
#         self.btn.clicked.connect(self.upload_files)
#         self.lst = lst
#         lay.addWidget(self.btn, 6, 0, 1, 1)
#
#     def upload_files(self):
#         names = QFileDialog.getOpenFileNames(self, 'Open file')
#         for name in names[0]:
#             self.lst.addItem(name)


class ChoiceList(QWidget):
    def __init__(self, lay, vtkWidget,  parent=None):
        QWidget.__init__(self, parent)
        # self.pic_lbl = QLabel()
        # self.pic_lbl.setFixedWidth(800)
        # self.pic_lbl.setFixedHeight(720)
        # lay.addWidget(self.pic_lbl, 2, 0, 4, 4)
        # self.pic_lbl.setPixmap(PyQt5.QtGui.QPixmap("pic2.jpg"))

        # a figure instance to plot on
        self.figure = Figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvasQTAgg(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        #  self.toolbar = NavigationToolbar(self.canvas, self)
        # TODO chyba nie chcemy toolbara?
        # lay.addWidget(self.toolbar, 6, 0, 1, 1)
        lay.addWidget(self.canvas, 2, 0, 4, 4)

        self.date_lst = QListWidget()
        lay.addWidget(self.date_lst, 0, 1, 1, 1)
        self.city_lst = QListWidget()
        lay.addWidget(self.city_lst, 1, 1, 1, 1)
        self.iren = None
       # self.date_lst.itemClicked.connect(self.set_stl)
        self.date_lst.itemClicked.connect(self.show_plot)
        self.city_lst.itemClicked.connect(self.show_plot)
        self.vtkWidget = vtkWidget
        self.city_lst.addItems(['Warsaw, PL', 'Gdansk, PL', 'Pila, PL', 'Torun, PL', 'Plock, PL', 'Poznan, PL', 'Opole, PL',
                       'Krakow, PL', 'Lublin, PL', 'Rzeszow, PL'])
        self.dates = self.set_dates()
        self.date_lst.addItems(self.dates)
        self.date_lst.setCurrentRow(1)
        self.city_lst.setCurrentRow(1)

    def set_stl(self):
        # filename = "files/Part_1.stl"
        filename = str(self.date_lst.currentItem().text())
        # print(filename)

        reader = vtk.vtkSTLReader()
        reader.SetFileName(filename)

        mapper = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            mapper.SetInput(reader.GetOutput())
        else:
            mapper.SetInputConnection(reader.GetOutputPort())

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        # self.vtkWidget = QVTKRenderWindowInteractor()

        ren = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

        ren.AddActor(actor)
        ren.ResetCamera()

        #lay.addWidget(self.vtkWidget, 2, 5, 4, 4)

        self.iren_refresh()


    def iren_refresh(self):
        self.iren.Initialize()
        self.iren.Start()

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
        fore = getter.main(city, date)

        hours = []
        temperatures = []
        rainfalls = []
        snowfalls = []
        press = []
        wind = []
        clouds = []

        for weather in fore:

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

            # TODO a moze sea level?
            press.append(weather[2]['press'])
            wind.append(weather[5]['speed'])
            # TODO a chmurki? :/
            clouds.append(None)

        # print(temperatures)
        # print(hours)
        # print(press)
        # print(rainfalls)
        # print(snowfalls)

        temp_ax = self.figure.add_subplot(611)
        temp_ax.clear()
        temp_ax.plot(temperatures, '*-')

        rain_ax = self.figure.add_subplot(612)
        rain_ax.clear()
        rain_ax.plot(rainfalls, '*-')

        snow_ax = self.figure.add_subplot(613)
        snow_ax.clear()
        snow_ax.plot(snowfalls, '*-')

        snow_ax = self.figure.add_subplot(613)
        snow_ax.clear()
        snow_ax.plot(snowfalls, '*-')

        press_ax = self.figure.add_subplot(614)
        press_ax.clear()
        press_ax.plot(press, '*-')

        wind_ax = self.figure.add_subplot(615)
        wind_ax.clear()
        wind_ax.plot(wind, '*-')

        clouds_ax = self.figure.add_subplot(616)
        clouds_ax.clear()
        clouds_ax.plot(clouds, '*-')

        # refresh canvas
        self.canvas.draw()


# TODO okienko po kliknieciu z listy zeby bylo wiadomo ze pogoda sie liczy -> jakies koleczko krecace czy cos


app = QApplication(sys.argv)

lay = QGridLayout()

lbl1 = QLabel("Choose date:")
lay.addWidget(lbl1, 0, 0, 1, 1)

lbl2 = QLabel("Choose city:")
lay.addWidget(lbl2, 1, 0, 1, 1)


notes = QTextEdit("Tu beda notatki")
lay.addWidget(notes, 0, 3, 2, 4)

vtkWidget = QVTKRenderWindowInteractor()
vtkWidget.setFixedWidth(800)
vtkWidget.setFixedHeight(700)
lay.addWidget(vtkWidget, 2, 4, 4, 5)


choices_list = ChoiceList(lay, vtkWidget)
# btn = ImportButton(lay, date_list.get_list())


w = QWidget()
w.setFixedWidth(1800)
w.setFixedHeight(1100)
w.move(100, 100)
w.setLayout(lay)
w.show()

app.exec_()
