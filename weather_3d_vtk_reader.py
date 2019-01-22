import vtk
import time
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


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
        renderer.ResetCamera()

        interactor.Initialize()
        interactor.Start()

        return vtkWidget
