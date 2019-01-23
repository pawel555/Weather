import vtk
import time
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtk.util.colors import tomato
from get_data_api import GetDataFromOWMApi

class Weather3D:

    def __init__(self):
        self.fore = None
        self.date_of_data_generation= None
    def main(self, forecast, date, checkboxes):

        if self.fore is None or self.date_of_data_generation != date:
            self.fore = GetDataFromOWMApi().return_weather_for_all_cities(date)
            self.date_of_data_generation =date

        reader = vtk.vtkPNGReader()
        reader.SetFileName("Poland.png")
        quant = vtk.vtkImageQuantizeRGBToIndex()
        quant.SetInputConnection(reader.GetOutputPort())
        quant.SetNumberOfColors(32)
        i2pd = vtk.vtkImageToPolyDataFilter()
        i2pd.SetInputConnection(quant.GetOutputPort())
        i2pd.SetLookupTable(quant.GetLookupTable())
        i2pd.SetColorModeToLUT()
        i2pd.SetOutputStyleToPolygonalize()
        i2pd.SetError(0)
        i2pd.DecimationOn()
        i2pd.SetDecimationError(0.0)
        i2pd.SetSubImageSize(25)
        tf = vtk.vtkTriangleFilter()
        tf.SetInputConnection(i2pd.GetOutputPort())

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(tf.GetOutputPort())
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        renderer = vtk.vtkRenderer()

        vtkWidget = QVTKRenderWindowInteractor()

        vtkWidget.GetRenderWindow().AddRenderer(renderer)

        interactor = vtkWidget.GetRenderWindow().GetInteractor()
        renderer.AddActor(actor)

        #warszawa
        for i in range (len(self.fore)):
            list_of_actors = list(self.return_weather_actor(self.fore[i], date, checkboxes))
            if self.fore[i][0] == 'Warsaw, PL':
                l=0
                for actor_from_list in list_of_actors:
                    actor_from_list.SetPosition(330-l*5,280,1)
                    l+=1
                    renderer.AddActor(actor_from_list)
            elif self.fore[i][0] == 'Gdansk, PL':
                l=0
                for actor_from_list in list_of_actors:
                    actor_from_list.SetPosition(245-l*5,420,1)
                    l+=1
                    renderer.AddActor(actor_from_list)        
        renderer.ResetCamera()

        interactor.Initialize()
        interactor.Start()
        #print(checkboxes)
        #print(date)
        #print(self.fore)
        #self.return_weather_widget(forecast, date, checkboxes)
        #[{'temp': True}, {'rain': True}, {'snow': True}, {'pressure': True}, {'wind': True}, {'clouds': True}]
        return vtkWidget


    def return_weather_actor(self, weather, date, checkboxes):
        #actor = vtk.vtkActor()
        actor = vtk.vtkActor()
        actor2 = vtk.vtkActor()
        print(weather)
        if checkboxes[0].get('temp'):
            textSource = vtk.vtkTextSource()
            textSource.SetText(str(weather[4].get('temp')))
            textSource.SetForegroundColor(1.0, 0.0, 0.0)
            textSource.BackingOn()
            textSource.Update()
            textMapper = vtk.vtkPolyDataMapper()
            textMapper.SetInputConnection(textSource.GetOutputPort())
            actor.SetMapper(textMapper)
            actor.SetScale(0.9)
        if checkboxes[3].get('pressure'):
            print("True")
            cube = vtk.vtkCubeSource()
            cubeMapper = vtk.vtkPolyDataMapper()
            cubeMapper.SetInputConnection(cube.GetOutputPort())
            print(str(weather[3].get('press')))            
            actor2.SetMapper(cubeMapper)
            actor2.SetScale((float(weather[3].get('press'))-950)*12/100)
            actor2.GetProperty().SetColor((float(weather[3].get('press'))-950)/100,0,0)
        return actor,actor2

