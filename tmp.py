import vtk
import numpy as np

data_matrix = np.zeros([75, 75, 75], dtype=np.uint8)
data_matrix[1:35, 1:35, 1:35] = 1
data_matrix[25:55, 25:55, 25:55] = 2
data_matrix[45:74, 45:74, 45:74] = 3

w, d, h = data_matrix.shape
dicom_images = vtk.vtkImageImport()
dicom_images.CopyImportVoidPointer(data_matrix.tostring(),
                                   len(data_matrix.tostring()))
dicom_images.SetDataScalarTypeToUnsignedChar()
dicom_images.SetNumberOfScalarComponents(1)
dicom_images.SetDataExtent(0, h - 1, 0, d - 1, 0, w - 1)
dicom_images.SetWholeExtent(0, h - 1, 0, d - 1, 0, w - 1)
dicom_images.SetDataSpacing(1, 1, 1)

render = vtk.vtkRenderer()
render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(render)
render_interact = vtk.vtkRenderWindowInteractor()
render_interact.SetRenderWindow(render_window)

threshold_dicom_image = vtk.vtkImageThreshold()
threshold_dicom_image.SetInputConnection(dicom_images.GetOutputPort())
threshold_dicom_image.Update()

discrete_marching_cubes = vtk.vtkDiscreteMarchingCubes()
discrete_marching_cubes.SetInputConnection(threshold_dicom_image.GetOutputPort())
discrete_marching_cubes.GenerateValues(3, 1, 3)
discrete_marching_cubes.ComputeNormalsOn()
discrete_marching_cubes.Update()

colorLookupTable = vtk.vtkLookupTable()
colorLookupTable.SetNumberOfTableValues(3)
colorLookupTable.Build()


colorLookupTable.SetTableValue(0, 1, 0, 0, 0.5)
colorLookupTable.SetTableValue(1, 0, 1, 0, 0.5)
colorLookupTable.SetTableValue(2, 0, 0, 1, 0.5)
'''
colorLookupTable.SetTableValue(0, 1, 0, 0, 0.5)
colorLookupTable.SetTableValue(1, 0, 1, 0, 1)
colorLookupTable.SetTableValue(2, 0, 0, 1, 0.5)
'''

dicom_data_mapper = vtk.vtkPolyDataMapper()
dicom_data_mapper.SetInputConnection(discrete_marching_cubes.GetOutputPort())
dicom_data_mapper.ScalarVisibilityOn()
dicom_data_mapper.SetLookupTable(colorLookupTable)
dicom_data_mapper.SetScalarRange(1, 3)
dicom_data_mapper.Update()

actor_dicom_3d = vtk.vtkActor()
actor_dicom_3d.SetMapper(dicom_data_mapper)

render.AddActor(actor_dicom_3d)
render.ResetCamera()

render_window.Render()
render_interact.Start()