import base64
import datetime
import sys
from os import path

import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

import cv2
from tencent_util import search_person


class RecordVideo(QtCore.QObject):
    image_data = QtCore.pyqtSignal(np.ndarray)

    def __init__(self, camera_port=0, parent=None):
        super().__init__(parent)
        self.camera = cv2.VideoCapture(camera_port)
        self.timer = QtCore.QBasicTimer()

    def start_recording(self):
        self.timer.start(0, self)

    def timerEvent(self, event):
        if (event.timerId() != self.timer.timerId()):
            return

        read, image = self.camera.read()
        if read:
            self.image_data.emit(image)


class FaceDetectionWidget(QtWidgets.QWidget):
    def __init__(self, record_path, parent=None):
        super().__init__(parent)
        self.image = QtGui.QImage()
        self.raw_image = None
        self._red = (0, 0, 255)
        self._width = 2
        self._min_size = (30, 30)
        self.record_file = open(record_path, "w+", encoding='utf-8')

    def search_faces(self):
        if self.raw_image is None:
            print("Click start to open camera")
            return
        frame = self.raw_image
        image = base64.b64encode(cv2.imencode('.jpg',
                                              frame)[1]).decode('utf-8')
        search_result = search_person(image)
        print(search_result['Results'][0]['Candidates'][0])
        try:
            candidate = search_result['Results'][0]['Candidates'][0]
            if candidate['Score'] > 50:
                self.record_file.write(
                    f"{candidate['PersonId']},{candidate['PersonName']},{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')}\n"
                )
                self.record_file.flush()
                QMessageBox.about(self, "Success", f"{candidate['PersonId']}-{candidate['PersonName']} 签到成功")
                return candidate
            else:
                QMessageBox.about(self, "Fail", "无对应人脸")
                return None
        except TypeError:
            QMessageBox(self, "Fail", "签到失败")
            return None

    def image_data_slot(self, image_data):
        self.image = self.get_qimage(image_data)
        if self.image.size() != self.size():
            self.setFixedSize(self.image.size())
        self.update()

    def get_qimage(self, image: np.ndarray):
        self.raw_image = image
        height, width, colors = image.shape
        bytesPerLine = 3 * width
        QImage = QtGui.QImage

        image = QImage(image.data, width, height, bytesPerLine,
                       QImage.Format_RGB888)

        image = image.rgbSwapped()
        return image

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawImage(0, 0, self.image)
        self.image = QtGui.QImage()


class MainWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.face_detection_widget = FaceDetectionWidget(f"./result-{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')}.csv")

        # TODO: set video port
        self.record_video = RecordVideo()
        self.run_button = QtWidgets.QPushButton('Start')
        self.detect_button = QtWidgets.QPushButton('Detect')

        # Connect the image data signal and slot together
        image_data_slot = self.face_detection_widget.image_data_slot
        self.record_video.image_data.connect(image_data_slot)
        # connect the run button to the start recording slot
        self.run_button.clicked.connect(self.record_video.start_recording)
        self.detect_button.clicked.connect(self.face_detection_widget.search_faces)
        # Create and set the layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.face_detection_widget)
        layout.addWidget(self.run_button)
        layout.addWidget(self.detect_button)

        self.setLayout(layout)


def main():
    app = QtWidgets.QApplication(sys.argv)

    main_window = QtWidgets.QMainWindow()
    main_widget = MainWidget()
    main_window.setCentralWidget(main_widget)
    main_window.show()
    sys.exit(app.exec_())


main()
