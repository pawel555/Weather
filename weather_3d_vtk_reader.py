import vtk
import time
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtk.util.colors import tomato
from get_data_api import GetDataFromOWMApi

class Weather3D:

    def __init__(self):
        self.fore = None
        self.date_of_data_generation= None
        self.filename = "cloud.stl"

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

  
        for i in range (len(self.fore)):
            list_of_actors = list(self.return_weather_actor(self.fore[i], date, checkboxes))
            if self.fore[i][0] == 'Warsaw, PL':
                l=0
                for actor_from_list in list_of_actors:
                    actor_from_list.SetPosition(330-l*5,280,5)
                    l+=1
                    renderer.AddActor(actor_from_list)
            elif self.fore[i][0] == 'Gdansk, PL':
                l=0
                for actor_from_list in list_of_actors:
                    actor_from_list.SetPosition(245-l*5,420,5)
                    l+=1
                    renderer.AddActor(actor_from_list)        
            elif self.fore[i][0] == 'Pila, PL':
                l=0
                for actor_from_list in list_of_actors:
                    actor_from_list.SetPosition(150-l*5,340,5)
                    l+=1
                    renderer.AddActor(actor_from_list)
            elif self.fore[i][0] == 'Torun, PL':
                l=0
                for actor_from_list in list_of_actors:
                    actor_from_list.SetPosition(230-l*5,320,5)
                    l+=1
                    renderer.AddActor(actor_from_list)
            elif self.fore[i][0] == 'Plock, PL':
                l=0
                for actor_from_list in list_of_actors:
                    actor_from_list.SetPosition(280-l*5,300,5)
                    l+=1
                    renderer.AddActor(actor_from_list)
            elif self.fore[i][0] == 'Poznan, PL':
                l=0
                for actor_from_list in list_of_actors:
                    actor_from_list.SetPosition(160-l*5,280,5)
                    l+=1
                    renderer.AddActor(actor_from_list)
            elif self.fore[i][0] == 'Opole, PL':
                l=0
                for actor_from_list in list_of_actors:
                    actor_from_list.SetPosition(200-l*5,150,5)
                    l+=1
                    renderer.AddActor(actor_from_list)
            elif self.fore[i][0] == 'Krakow, PL':
                l=0
                for actor_from_list in list_of_actors:
                    actor_from_list.SetPosition(290-l*5,100,5)
                    l+=1
                    renderer.AddActor(actor_from_list)
            elif self.fore[i][0] == 'Lublin, PL':
                l=0
                for actor_from_list in list_of_actors:
                    actor_from_list.SetPosition(420-l*5,195,5)
                    l+=1
                    renderer.AddActor(actor_from_list)     
            elif self.fore[i][0] == 'Rzeszow, PL':
                l=0
                for actor_from_list in list_of_actors:
                    actor_from_list.SetPosition(390-l*5,100,5)
                    l+=1
                    renderer.AddActor(actor_from_list)    
        renderer.ResetCamera()
        renderer.SetBackground(1,1,1)
        interactor.Initialize()
        interactor.Start()
        return vtkWidget


    def return_weather_actor(self, weather, date, checkboxes):
        actor = vtk.vtkActor()
        actor2 = vtk.vtkActor()
        actor3 = vtk.vtkActor()
        actor4 = vtk.vtkActor()
        actor5 = vtk.vtkActor()
        if checkboxes[0].get('temp'):
            textSource = vtk.vtkTextSource()
            textSource.SetText(str(weather[4].get('temp')))
            textSource.SetBackgroundColor(1, 1, 1)
            textSource.SetForegroundColor(0.0, 0.0, 0.0)
            textSource.BackingOn()
            textSource.Update()
            textMapper = vtk.vtkPolyDataMapper()
            textMapper.SetInputConnection(textSource.GetOutputPort())
            actor.SetMapper(textMapper)
            actor.SetScale(0.9)
        if checkboxes[2].get('snow'):
            cube = vtk.vtkCubeSource()
            cubeMapperSnow = vtk.vtkPolyDataMapper()
            cubeMapperSnow.SetInputConnection(cube.GetOutputPort())         
            actor4.SetMapper(cubeMapperSnow)
            try:
                actor4.SetScale(7,7,float(weather[5].get('3h'))*100)
            except:
                actor4.SetScale(7,7,0)
            actor4.GetProperty().SetColor(0,0,1)
        if checkboxes[3].get('pressure'):
            cube = vtk.vtkCubeSource()
            cubeMapper = vtk.vtkPolyDataMapper()
            cubeMapper.SetInputConnection(cube.GetOutputPort())      
            actor2.SetMapper(cubeMapper)
            actor2.SetScale(7,7,(float(weather[3].get('press'))-950)*40/100)
            actor2.GetProperty().SetColor((float(weather[3].get('press'))-950)/100,0,0)
        if checkboxes[4].get('wind'):
            arrow = vtk.vtkArrowSource()
            arrowMapper = vtk.vtkPolyDataMapper()
            arrowMapper.SetInputConnection(arrow.GetOutputPort())
         
            actor3.SetMapper(arrowMapper)
            actor3.SetScale(float(weather[6].get('speed'))*15)
            actor3.GetProperty().SetColor(0,1,0)
            actor3.SetOrientation(0,0,float(weather[6].get('deg')))
        if checkboxes[5].get('clouds'):
            readerStl = vtk.vtkSTLReader()
            readerStl.SetFileName(self.filename)
            mapperStl = vtk.vtkPolyDataMapper()
            mapperStl.SetInputConnection(readerStl.GetOutputPort())
            actor5.SetMapper(mapperStl)
            try:
                actor5.SetScale(0.5*float(weather[7])/100)
            except:
                actor5.SetScale(0.1)
        return actor,actor2,actor3,actor4,actor5

