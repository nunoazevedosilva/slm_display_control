# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 17:02:41 2021

@author: nunoa
"""

import sys
import time

import numpy as np

from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
if is_pyqt5():
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
else:
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        layout = QtWidgets.QVBoxLayout(self._main)

        self.fig = Figure(figsize=(5, 3))
        self.dynamic_canvas = FigureCanvas(self.fig)
        layout.addWidget(self.dynamic_canvas)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        sizeScreen=QtWidgets.QDesktopWidget().screenGeometry(0)
        screenWidth=sizeScreen.width()
        screenHeight=sizeScreen.height()
        
        self.setGeometry(0,0,
                        screenWidth, 
                        screenHeight)


        self._dynamic_ax = self.dynamic_canvas.figure.subplots()
        self._dynamic_ax.set_axis_off()
        self.fig.subplots_adjust(
            left=0, right=1, top=1, bottom=0, wspace=0, hspace=0
        )
        
        self.i = 0

    def _update_canvas(self):
        self._dynamic_ax.clear()
        
        # Shift the sinusoid as a function of time.
        self._dynamic_ax.imshow(self.i*np.ones((100,100)), 
                                    aspect="auto", 
                                    interpolation="none", cmap="Greys", 
                                    vmin=0, vmax=255)
        self._dynamic_ax.set_axis_off()
        self.fig.subplots_adjust(
            left=0, right=1, top=1, bottom=0, wspace=0, hspace=0)
        self._dynamic_ax.figure.canvas.draw()
        self.i += 1
        print(self.i)


if __name__ == "__main__":
    qapp = QtWidgets.QApplication(sys.argv)
    app = ApplicationWindow()
    
    display_monitor=0
    monitor = QtWidgets.QDesktopWidget().screenGeometry(display_monitor)
    app.move(monitor.left(), monitor.top())
    app.showFullScreen()
    
    app.show()
    timer = app.dynamic_canvas.new_timer(
            50, [(app._update_canvas, (), {})])
    timer.start()
        
    qapp.exec_()