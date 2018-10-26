import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QPoint, QTimer
from PyQt5.QtGui import QFont, QPainter, QPixmap, QImage

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.colors import Colormap
import matplotlib.pyplot as plt
import numpy as np	
import matplotlib.cm as cm

from src.DDbackend import DaisyDriver
from src.mainbackend import RepeatedTimer

from serial.serialutil import SerialException

class Window(QDialog):
	def __init__(self, parent=None):
		super(Window, self).__init__(parent)
		
		self.initFigure()		
		
		self.initUI()
		
		#~ self.connecters()
		
		try: 
			self.DD = DaisyDriver()
			self.DDconnected = True
		except SerialException:
			print('DaisyDriver not connected!')
			self.DDconnected = False
			self.DD = DaisyDriver(connected=False)
			
		self.LightSensorPoll = RepeatedTimer(0.1, self.DD.get_light_sensor_val, self.modifyFigure)
		self.LightSensorPoll.start_all()
		
	def initFigure(self):
		self.figure = plt.figure(figsize=(4.5, 9.5))
		self.canvas = FigureCanvas(self.figure)
		self.figure.clear()
		
		self.ax = self.figure.add_subplot(111)
		self.rects = self.ax.bar(1, [1], align='center')
		self.ax.set_ylim(bottom=0, top=50)
		self.ax.set_yticks([0])
		self.ax.set_yticklabels([""])
		self.ax.set_xticks([1])
		self.ax.set_xticklabels(["Light Level"], fontsize=17)
		#~ self.ax.grid(True, axis='y', which='both')
		#~ self.ax.grid('on')
		
		#~ self.cm = Colormap('jet')
		#~ self.cm = list(cm.seismic(np.linspace(0.0, 1.0, 250)))
		self.cm = list(cm.rainbow(np.linspace(0.0, 1.0, 250)))
	
		self.canvas.draw()
		
	def initUI(self):
		subLayout = QVBoxLayout()
		
		#~ self.slider = QSlider(Qt.Horizontal, self)
		#~ self.slider.setGeometry(30,40,100,30)
		#~ self.slider.setRange(0,255)
		#~ self.slider.setValue(127)
		
		subLayout.addWidget(self.canvas)
		#~ subLayout.addWidget(self.slider)
				
		self.setLayout(subLayout)
		
	def modifyFigure(self, val):
		
		self.rects[0].set_height(val)
		self.rects[0].set_color(self.cm[int(val*5)-1])
		self.canvas.draw()
		
	#~ def connecters(self):
		#~ self.slider.valueChanged[int].connect(self.modifyFigure)
		
	def closeEvent(self, event):
		
		self.LightSensorPoll.stop()
		
		try:
			self.DD.close()
		except AttributeError:
			pass
		
if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = Window()
    main.show()

    sys.exit(app.exec_())
