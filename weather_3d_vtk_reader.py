import vtk
import time
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtk.util.colors import tomato

class Weather3D:

    def main(self, forecast, date, checkboxes):

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
        list_of_actors = list(self.return_weather_actor(forecast, date, checkboxes))

        for l in range(0,len(list_of_actors)):
            new_actor = (list_of_actors[l])
            if l>0:
                new_actor.SetPosition(0,l,0)
            renderer.AddActor(new_actor)
        renderer.ResetCamera()

        interactor.Initialize()
        interactor.Start()
        print(checkboxes)
        #print(date)
        print(forecast)
        #self.return_weather_widget(forecast, date, checkboxes)
        #[{'temp': True}, {'rain': True}, {'snow': True}, {'pressure': True}, {'wind': True}, {'clouds': True}]
        return vtkWidget


    def return_weather_actor(self, weather, date, checkboxes):
        #actor = vtk.vtkActor()
        actor = vtk.vtkTextActor()
        actor2 = vtk.vtkActor()
        if checkboxes[0].get('temp'):
            #print("True")
            #cylinder = vtk.vtkCylinderSource()
            #cylinderMapper = vtk.vtkPolyDataMapper()
            #cylinderMapper.SetInputConnection(cylinder.GetOutputPort())
#
            #vtkTransform = vtk.vtkTransform()
#
            #vtkTransform.Scale(12,12,12)
            #
            #actor.SetMapper(cylinderMapper)
            #actor.SetUserTransform(vtkTransform)
            #actor.GetProperty().SetColor(tomato)
            actor.SetInput("123")
            txtprop=actor.GetTextProperty()
            txtprop.SetFontFamilyToArial()
            txtprop.SetFontSize(200)
            txtprop.SetColor(1,1,1)
        if checkboxes[1].get('rain'):
            print("True")
            cube = vtk.vtkCubeSource()
            cubeMapper = vtk.vtkPolyDataMapper()
            cubeMapper.SetInputConnection(cube.GetOutputPort())

            vtkTransform = vtk.vtkTransform()

            vtkTransform.Scale(15,15,15)
            
            actor2.SetMapper(cubeMapper)
            actor2.SetUserTransform(vtkTransform)
            actor2.GetProperty().SetColor(tomato)
        return actor,actor2

