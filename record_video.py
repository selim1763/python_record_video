import os
import cv2
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets                     # uic
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QWidget,
                             QLabel, QVBoxLayout)              # +++

from ui import Ui_Form                                   # +++
from video_settings import *


class video (QtWidgets.QDialog, Ui_Form):
    def __init__(self):
        super().__init__()

        self.setupUi(self)                                     # +++

        self.control_bt.clicked.connect(self.start_webcam)
        self.record.clicked.connect(self.record_video)

        self.image_label.setScaledContents(True)

        self.cap = None                                        #  -capture <-> +cap
        self.out = None
        self.recording = False

        self.timer = QtCore.QTimer(self, interval=5)
        self.timer.timeout.connect(self.update_frame)
        self.video_counter = 1


    @QtCore.pyqtSlot()
    def start_webcam(self):
        if self.cap is None:
            self.cap = cv2.VideoCapture(0)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,  640)
            self.timer.start()

    @QtCore.pyqtSlot()
    def update_frame(self):
        ret, image = self.cap.read()
        simage     = cv2.flip(image, 1)
        self.displayImage(image, True)

        if self.cap is not None:
            if self.recording == True:
                self.out.write(image)
            else:
                pass


    @QtCore.pyqtSlot()
    def record_video(self):
        global filepath
        if self.cap is not None:
            if self.recording == True:
                self.record.setText("Record")
                self.recording = False

                if self.out != None:
                    self.out.release()
                    self.out = None

                    self.video_counter += 1
                    filepath = filename + str(self.video_counter) + filetype
            else:
                self.record.setText("Save")
                self.recording = True

                if self.out == None:
                    filepath = filename + str(self.video_counter) + filetype
                    self.out = cv2.VideoWriter(filepath, get_video_type(filepath), 25, get_dims(self.cap, res))


    def displayImage(self, img, window=True):
        qformat = QtGui.QImage.Format_Indexed8
        if len(img.shape)==3 :
            if img.shape[2]==4:
                qformat = QtGui.QImage.Format_RGBA8888
            else:
                qformat = QtGui.QImage.Format_RGB888
        outImage = QtGui.QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)
        outImage = outImage.rgbSwapped()
        if window:
            self.image_label.setPixmap(QtGui.QPixmap.fromImage(outImage))

### +++ ^^^


if __name__=='__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = video()
    window.setWindowTitle('main code')
    window.show()
    sys.exit(app.exec_())