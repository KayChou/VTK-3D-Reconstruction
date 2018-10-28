import vtk

file = './data/ct_stick.nii.gz'
NiftiReader = vtk.vtkNIFTIImageReader()
NiftiReader.SetFileName(file)
NiftiReader.TimeAsVectorOn()
NiftiReader.Update()

ren = vtk.vtkRenderer() 
ren.SetBackground(0, 0, 0)

renWin = vtk.vtkRenderWindow()
renWin.SetSize(800, 600) 
renWin.AddRenderer(ren)

iren = vtk.vtkRenderWindowInteractor() 
iren.SetRenderWindow(renWin) 
iren.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera()) 

surface = vtk.vtkContourFilter() 
surface.SetInputConnection(NiftiReader.GetOutputPort()) 
surface.SetValue(0, 500)

# Colors
lut = vtk.vtkLookupTable() 
lut.SetNumberOfColors(3)
lut.SetTableValue(0, 1, 0, 0, 0.5)  # Red
lut.SetTableValue(1, 0, 1, 0, 0.5)  # Green
lut.SetTableValue(2, 1, 1, 1, 0.5)  # Blue
'''
lut.SetTableValue(3, 0.8900, 0.8100, 0.3400, 0.5)  # Banana
lut.SetTableValue(4, 1.0000, 0.3882, 0.2784, 0.5)  # Tomato

lut.SetTableValue(7, 0.9608, 0.8706, 0.7020, 0.5)  # Wheat
lut.SetTableValue(8, 0.9020, 0.9020, 0.9804, 0.5)  # Lavender
lut.SetTableValue(9, 1.0000, 0.4900, 0.2500, 0.5)  # Flesh
lut.SetTableValue(10, 0.5300, 0.1500, 0.3400, 0.5)  # Raspberry
lut.SetTableValue(11, 0.9804, 0.5020, 0.4471, 0.5)  # Salmon
lut.SetTableValue(12, 0.7400, 0.9900, 0.7900, 0.5)  # Mint
lut.SetTableValue(13, 0.2000, 0.6300, 0.7900, 0.5)  # Peacock

lut.SetTableValue(3, 0, 0, 0, 0.5)  # Black
lut.SetTableValue(3, 1, 1, 1, 0.5)  # White
'''
'''
lut.SetTableRange(500, 900)
lut.SetHueRange(0.0, 1.0)  # se diao
lut.SetSaturationRange(1.0, 1.0)  # bao he du
lut.SetValueRange(1.0, 1.0)
'''
lut.Build() 

# Map to colors
mapToC = vtk.vtkImageMapToColors() 
mapToC.PassAlphaToOutputOn() 
mapToC.SetLookupTable(lut) 
mapToC.SetInputConnection(NiftiReader.GetOutputPort()) 
# mapToC.SetOutputFormatToLuminance()
mapToC.Update() 

# Probe
probe = vtk.vtkProbeFilter() 
probe.SetInputConnection(surface.GetOutputPort()) 
probe.SetSourceConnection(mapToC.GetOutputPort()) 
probe.Update() 

# Create a mapper and an actor for the extracted surface 
smapper = vtk.vtkPolyDataMapper() 
smapper.SetInputConnection(probe.GetOutputPort())

actor = vtk.vtkActor() 
actor.SetMapper(smapper) 
ren.AddActor(actor) 

iren.Initialize() 
renWin.Render() 
iren.Start() 