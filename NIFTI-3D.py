# coding=utf-8
import vtk

file = './data/stick0.nii.gz'


def main():
    # source—filter——mapper——actor——render——renderwindow——interactor
    aRenderer = vtk.vtkRenderer()  # 渲染器

    renWin = vtk.vtkRenderWindow()  # 渲染窗口
    renWin.AddRenderer(aRenderer)

    v16 = vtk.vtkNIFTIImageReader()
    v16.SetFileName(file)
    v16.TimeAsVectorOn()
    v16.Update()

    skinExtractor = vtk.vtkContourFilter()
    skinExtractor.SetInputConnection(v16.GetOutputPort())
    skinExtractor.SetValue(0, 500)

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

    aRenderer.AddActor(outline)
    aRenderer.AddActor(skin)
    aRenderer.SetActiveCamera(aCamera)
    aRenderer.ResetCamera()
    aCamera.Dolly(1.5)

    aRenderer.SetBackground(1, 1, 1)
    renWin.SetSize(640, 480)
    aRenderer.ResetCameraClippingRange()

    iren = vtk.vtkRenderWindowInteractor()  # 窗口交互
    iren.SetRenderWindow(renWin)
    iren.Initialize()
    iren.Start()


if __name__ == '__main__':
    main()