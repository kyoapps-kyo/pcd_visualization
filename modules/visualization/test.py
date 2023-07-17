import sys
import open3d as o3d
import numpy as np
import pyqtgraph.opengl as gl
from PySide6.QtWidgets import QApplication, QVBoxLayout, QPushButton, QWidget, QFileDialog
from pyqtgraph.opengl import GLViewWidget


class PyQtGraphicDemo(QWidget):
    def __init__(self, parent=None):
        super(PyQtGraphicDemo, self).__init__(parent)

        self.resize(600, 400)
        # 点云显示控件
        self.graphicsView = GLViewWidget(self)
        # 按钮
        self.pushButton = QPushButton(self)
        self.pushButton.setText("PushButton")
        self.pushButton.clicked.connect(self.showImage)
        # 布局
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.addWidget(self.graphicsView)
        self.verticalLayout.addWidget(self.pushButton)
        # 设置窗口布局
        self.setLayout(self.verticalLayout)

        # 显示坐标轴
        x = gl.GLLinePlotItem(pos=np.asarray([[0, 0, 0], [0.2, 0, 0]]), color=(1, 0, 0, 1), width=0.005)
        y = gl.GLLinePlotItem(pos=np.asarray([[0, 0, 0], [0, 0.2, 0]]), color=(0, 1, 0, 1), width=0.005)
        z = gl.GLLinePlotItem(pos=np.asarray([[0, 0, 0], [0, 0, 0.2]]), color=(0, 0, 1, 1), width=0.005)
        self.graphicsView.addItem(x)
        self.graphicsView.addItem(y)
        self.graphicsView.addItem(z)

    def showImage(self):
        fileName, filetype = QFileDialog.getOpenFileName(self, "请选择图像：", '.', "All Files(*);;")
        if fileName != '':
            # 读取点云
            pcd = o3d.io.read_point_cloud(fileName)
            # 获取 Numpy 数组
            np_points = np.asarray(pcd.points)
            # 创建显示对象
            plot = gl.GLScatterPlotItem()
            # 设置显示数据
            plot.setData(pos=np_points, color=(1, 1, 1, 1), size=0.0005, pxMode=False)
            # 显示点云
            self.graphicsView.addItem(plot)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PyQtGraphicDemo()
    window.show()
    sys.exit(app.exec_())
