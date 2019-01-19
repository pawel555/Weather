import sys
import vtk

import PyQt5
from PyQt5.QtWidgets import *
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


class ImportButton(QWidget):
    def __init__(self, lay, lst, parent=None):
        QWidget.__init__(self, parent)
        self.btn = QPushButton('Select files to load:')
        self.btn.clicked.connect(self.upload_files)
        self.lst = lst
        lay.addWidget(self.btn, 6, 0, 1, 1)

    def upload_files(self):
        names = QFileDialog.getOpenFileNames(self, 'Open file')
        for name in names[0]:
            self.lst.addItem(name)


class ChoiceList(QWidget):
    def __init__(self, lay, vtkWidget,  parent=None):
        QWidget.__init__(self, parent)
        self.date_lst = QListWidget()
        lay.addWidget(self.date_lst, 0, 1, 1, 1)
        self.city_lst = QListWidget()
        lay.addWidget(self.city_lst, 1, 1, 1, 1)
        self.iren = None
        self.date_lst.itemClicked.connect(self.set_stl)
        self.vtkWidget = vtkWidget

    def set_stl(self):
        # filename = "files/Part_1.stl"
        filename = str(self.date_lst.currentItem().text())
        print(filename)

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

date_list = ChoiceList(lay, vtkWidget)
btn = ImportButton(lay, date_list.get_list())

pic_lbl = QLabel()
pic_lbl.setFixedWidth(800)
pic_lbl.setFixedHeight(700)
lay.addWidget(pic_lbl, 2, 0, 4, 4)
pic_lbl.setPixmap(PyQt5.QtGui.QPixmap("pic2.jpg"))

w = QWidget()
w.setFixedWidth(1800)
w.setFixedHeight(1100)
w.move(100, 100)
w.setLayout(lay)
w.show()

app.exec_()
