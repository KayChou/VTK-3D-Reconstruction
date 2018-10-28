# coding=utf-8
import vtk


def render_g(file, layer):
    render0 = vtk.vtkRenderer()  # 渲染器
    render0.SetLayer(layer)
    render0.SetBackground(1, 1, 1)

    v16 = vtk.vtkNIFTIImageReader()
    v16.SetFileName(file)
    v16.TimeAsVectorOn()
    v16.Update()

    skinExtractor = vtk.vtkContourFilter()
    skinExtractor.SetInputConnection(v16.GetOutputPort())
    skinExtractor.SetValue(2, 500)

    skinNormals = vtk.vtkPolyDataNormals()
    skinNormals.SetInputConnection(skinExtractor.GetOutputPort())
    skinNormals.SetFeatureAngle(60.0)

    skinMapper = vtk.vtkPolyDataMapper()  # 映射器
    skinMapper.SetInputConnection(skinNormals.GetOutputPort())
    skinMapper.ScalarVisibilityOff()

    skin = vtk.vtkActor()
    skin.SetMapper(skinMapper)

    outlineData = vtk.vtkOutlineFilter()
    outlineData.SetInputConnection(v16.GetOutputPort())
    mapOutline = vtk.vtkPolyDataMapper()
    mapOutline.SetInputConnection(outlineData.GetOutputPort())

    outline = vtk.vtkActor()
    outline.SetMapper(mapOutline)
    outline.GetProperty().SetColor(0, 0, 0)

    aCamera = vtk.vtkCamera()
    aCamera.SetViewUp(0, 0, -1)
    aCamera.SetPosition(0, 1, 0)
    aCamera.SetFocalPoint(0, 0, 0)
    aCamera.ComputeViewPlaneNormal()

    render0.AddActor(outline)
    render0.AddActor(skin)
    render0.SetActiveCamera(aCamera)
    render0.ResetCamera()
    aCamera.Dolly(1.5)
    render0.ResetCameraClippingRange()

    return render0