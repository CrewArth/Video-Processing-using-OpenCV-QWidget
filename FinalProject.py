import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QSlider
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap, QImage


def start_stream():
    global video_capture, timer
    video_capture = cv2.VideoCapture(1)
    timer.timeout.connect(update_frame)
    timer.start(30)

def stop_stream():
    global video_capture, timer
    timer.stop()
    if video_capture is not None:
        video_capture.release()
        video_capture = None


def update_frame():
    global video_capture, threshold_value
    ret, frame = video_capture.read()
    if ret:
        grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ret, processed_frame = cv2.threshold(grayFrame, threshold_value, 255, cv2.THRESH_BINARY)

        h, w = processed_frame.shape
        q_image = QImage(processed_frame.data, w, h, w, QImage.Format_Grayscale8)

        # Display the processed frame
        pixmap = QPixmap.fromImage(q_image)
        video_label.setPixmap(pixmap)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create main window
    window = QMainWindow()
    window.setWindowTitle("Video Processing App")
    window.setGeometry(100, 100, 800, 600)

    # Create widget and layout
    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    layout = QVBoxLayout()
    central_widget.setLayout(layout)

    #To Display Frame
    video_label = QLabel()
    layout.addWidget(video_label)

    # Buttons for start/stop
    start_button = QPushButton("Start Stream")
    layout.addWidget(start_button)

    stop_button = QPushButton("Stop Stream")
    layout.addWidget(stop_button)

    # Slider for Canny
    threshold_slider = QSlider(Qt.Horizontal)
    threshold_slider.setMinimum(0)
    threshold_slider.setMaximum(255)
    threshold_slider.setValue(127)  # Initial value
    layout.addWidget(threshold_slider)

    video_capture = None
    timer = QTimer()
    threshold_value = threshold_slider.value()

    start_button.clicked.connect(start_stream)
    stop_button.clicked.connect(stop_stream)
    threshold_slider.valueChanged.connect(lambda: setattr(threshold_slider, "threshold_value", threshold_slider.value()))

    window.show()
    sys.exit(app.exec_())
