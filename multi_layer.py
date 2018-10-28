# coding=utf-8
import vtk
from render_layer import render_g

file = './data/stick0.nii.gz'


def main():
    render0 = render_g('./data/stick0.nii.gz', 0)
    render1 = render_g('./data/ct.nii.gz', 1)

    render1.SetUseDepthPeeling(1)
    render1.SetMaximumNumberOfPeels(100)
    render1.SetOcclusionRatio(0.1)

    renWin = vtk.vtkRenderWindow()  # 渲染窗口
    renWin.SetMultiSamples(0)
    renWin.SetAlphaBitPlanes(1)
    renWin.SetNumberOfLayers(2)
    renWin.AddRenderer(render0)
    renWin.AddRenderer(render1)
    renWin.SetSize(640, 480)

# ===============================================================
    iren = vtk.vtkRenderWindowInteractor()  # 窗口交互
    iren.SetRenderWindow(renWin)
    iren.Initialize()
    iren.Start()


if __name__ == '__main__':
    main()