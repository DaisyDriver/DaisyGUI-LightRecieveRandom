from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap, QImage, QIcon

class SettingsWindow(QDialog):
	
	def __init__(self, parent, camera):
		super(SettingsWindow, self).__init__(parent)
		
		# announce camera handle
		self.camera = camera
		
		# initialise user interface
		self.initUI()
		
	def initUI(self):
		# set title
		self.setWindowTitle('Camera Settings')
		
		# set form (2 column layout style)
		settings_layout = QFormLayout()

		