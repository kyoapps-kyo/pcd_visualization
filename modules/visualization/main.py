from typing import Optional
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PySide6.QtCore import QThread, Signal
import os
import numpy as np
from transform_tools import polar_to_cartesian, get_radar_xyz, xyz_loader

import time

import pyqtgraph.opengl as gl
# import pyqtgraph as pg
# from pyqtgraph import Transform3D, ColorMap, mkColor, makeRGBA

"""
编写主界面，读取显示图片
创建子线程，渲染点云数据，渲染完成通知主线程更新界面
"""

class BoxThread(QThread):
    # """
    # 文件夹路径
    folder_path = "modules/visualization/training/velodyne"
    # 获取文件夹中的点云文件列表
    file_list = sorted([f for f in os.listdir(folder_path) if f.endswith('.bin')])
    data_arrive_signal = Signal()
    pointcloud_arrive_signal = Signal()
    # 初始化帧数
    current_frame = 1
    file_path = os.path.join(folder_path, file_list[current_frame])
    points = xyz_loader(file_path)
    print(points.shape)
    # 关闭标记
    stop_flag = False
    print('run')

    def __init__(self) -> None:
        super().__init__()
        self.point = None

    def run(self):
        for i in range(10):
            # 2. 信号的手动触发
            self.signal.emit(str(i))
            time.sleep(1)
    # """

class MyMainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.mainLayout = QVBoxLayout(self)
        self.show_box = BoxThread()
        self.og_widget = gl.GLViewWidget(self)
        self.grid_item = gl.GLGridItem()
        self.og_widget.addItem(self.grid_item)
        # 画线
        self.x_axis_item = gl.GLLinePlotItem(pos = np.array([[0, 0, 0], [10, 0, 0]], dtype = np.float32), color = (1, 0, 0, 1), width = 2)
        self.y_axis_item = gl.GLLinePlotItem(pos = np.array([[0, 0, 0], [0, 10, 0]], dtype = np.float32), color = (0, 1, 0, 1), width = 2)
        self.z_axis_item = gl.GLLinePlotItem(pos = np.array([[0, 0, 0], [0, 0, 10]], dtype = np.float32), color = (0, 0, 1, 1), width = 2)
        self.og_widget.addItem(self.x_axis_item)
        self.og_widget.addItem(self.y_axis_item)
        self.og_widget.addItem(self.z_axis_item)

        # 渲染点云
        # self.show_pointcloud()
        self.box_item = gl.GLScatterPlotItem(pos=np.array([10, 10, 10]),
                                             size=5,
                                             pxMode=False)
        self.og_widget.addItem(self.box_item)

        self.mainLayout.addWidget(self.og_widget)



        # def closeEvent(self, a0):
        #     self.show_box.stop_flag = True
        #     self.show_box.quit()

    def show_pointcloud(self):
        points = self.show_box.points
        colors = np.ones(shape=(points.shape[0], 4))
        size = np.zeros(shape=points.shape[0]) + 1
        self.points_item = gl.GLScatterPlotItem(pos=points,
                                     color=(1, 1, 1, 1),
                                     size=size,
                                     pxMode=False)
        self.og_widget.addItem(self.points_item)
        print('hello')


if __name__ == '__main__':
    app = QApplication([])
    window = MyMainWindow()
    window.resize(1400, 1000)
    window.show()
    app.exec()