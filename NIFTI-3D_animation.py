# coding=utf-8
import vtk

base = './data/'
global v16
global skinExtractor
global skinNormals
global skinMapper
global skin
global outline
global outlineData
global mapOutline
global aCamera
global aRenderer
global renWin

class TimeEvent():
    def __init__(self):
        self.time_count = 0

    def execute(self, obj, event):
        global v16
        global skinExtractor
        global skinNormals
        global skinMapper
        global skin
        global outline
        global outlineData
        global mapOutline
        global aCamera
        global aRenderer
        global renWin

        file = 'stick' + str(self.time_count%8) + '.nii.gz'
        v16.SetFileName(base + file)
        v16.TimeAsVectorOn()
        v16.Update()

        skinExtractor.SetInputConnection(v16.GetOutputPort())
        skinExtractor.SetValue(0, 500)

        skinNormals.SetInputConnection(skinExtractor.GetOutputPort())
        skinNormals.SetFeatureAngle(60.0)

        skinMapper.SetInputConnection(skinNormals.GetOutputPort())
        skinMapper.ScalarVisibilityOff()

        skin.SetMapper(skinMapper)

        outlineData.SetInputConnection(v16.GetOutputPort())
        mapOutline.SetInputConnection(outlineData.GetOutputPort())

        outline.SetMapper(mapOutline)
        outline.GetProperty().SetColor(0, 0, 0)

        # Actors are added to the renderer.An initial camera view is created.
        # The Dolly() method moves the camera towards the Focal　Point,
        # thereby enlarging the image.
        aRenderer.AddActor(outline)
        aRenderer.AddActor(skin)
        aRenderer.SetActiveCamera(aCamera)
        aRenderer.ResetCamera()
        aCamera.Dolly(1.5)

        aRenderer.SetBackground(1, 1, 1)
        # renWin.SetSize(640, 480)
        aRenderer.ResetCameraClippingRange()

        iren = obj
        iren.GetRenderWindow().Render()

        print "Time Count:", self.time_count, file
        self.time_count += 1


def main():
    global v16
    global skinExtractor
    global skinNormals
    global skinMapper
    global skin
    global outline
    global outlineData
    global mapOutline
    global aCamera
    global aRenderer
    global renWin

    v16 = vtk.vtkNIFTIImageReader()
    skinExtractor = vtk.vtkContourFilter()
    skinNormals = vtk.vtkPolyDataNormals()
    skinMapper = vtk.vtkPolyDataMapper()  # 映射器
    skin = vtk.vtkActor()
    outlineData = vtk.vtkOutlineFilter()
    mapOutline = vtk.vtkPolyDataMapper()
    outline = vtk.vtkActor()
    aCamera = vtk.vtkCamera()
    renWin = vtk.vtkRenderWindow()
    aRenderer = vtk.vtkRenderer()  # 渲染器

    # source—filter——mapper——actor——render——renderwindow——interactor
    renWin.AddRenderer(aRenderer)

    v16.SetFileName(base + 'stick0.nii.gz')
    v16.TimeAsVectorOn()
    v16.Update()

    skinExtractor.SetInputConnection(v16.GetOutputPort())
    skinExtractor.SetValue(0, 500)

    skinNormals = vtk.vtkPolyDataNormals()
    skinNormals.SetInputConnection(skinExtractor.GetOutputPort())
    skinNormals.SetFeatureAngle(60.0)

    skinMapper.SetInputConnection(skinNormals.GetOutputPort())
    skinMapper.ScalarVisibilityOff()

    skin.SetMapper(skinMapper)

    outlineData.SetInputConnection(v16.GetOutputPort())
    mapOutline = vtk.vtkPolyDataMapper()
    mapOutline.SetInputConnection(outlineData.GetOutputPort())

    outline.SetMapper(mapOutline)
    outline.GetProperty().SetColor(0, 0, 0)

    aCamera.SetViewUp(0, 0, -1)
    aCamera.SetPosition(0, 1, 0)
    aCamera.SetFocalPoint(0, 0, 0)
    aCamera.ComputeViewPlaneNormal()

    # Actors are added to the renderer.An initial camera view is created.
    # The Dolly() method moves the camera towards the Focal　Point,
    # thereby enlarging the image.
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

    cb = TimeEvent()
    iren.AddObserver('TimerEvent', cb.execute)
    iren.CreateRepeatingTimer(50)

    iren.Start()


if __name__ == '__main__':
    main()