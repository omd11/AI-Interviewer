import sys

from PyQt6 import QtWidgets, QtMultimedia, QtMultimediaWidgets


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Interviewer")

        # instantiate widget and layout
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()

        
        # instanstiate fields
        self.label = QtWidgets.QLabel("Welcome to the AI Interviewer!")
        self.camera_list = QtWidgets.QComboBox()
        self.open_btn = QtWidgets.QPushButton("Open Camera",clicked = self.open_camera)
        self.setclose_btn = QtWidgets.QPushButton("Close Camera",clicked = self.close_camera)
        self.webcam_widget = QtMultimediaWidgets.QVideoWidget()

        # populate the camera list
        for camera in QtMultimedia.QMediaDevices.videoInputs():
            self.camera_list.addItem(camera.description(), camera)

        # add fields to layout
        layout.addWidget(self.label)
        layout.addWidget(self.camera_list)        
        layout.addWidget(self.open_btn)
        layout.addWidget(self.setclose_btn)
        layout.addWidget(self.webcam_widget)


        # set layout to widget
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # instantiate camera and capture session
        self.camera = None
        self.capsesh = QtMultimedia.QMediaCaptureSession()

    def open_camera(self):

        # close any previously running camera
        if self.camera:
            self.camera.stop()


        # get index of selected camera
        selected_index = self.camera_list.currentIndex()

        #set camera to webcam widget
        if selected_index >= 0:
            selected_device = QtMultimedia.QMediaDevices.videoInputs()[selected_index]
            self.camera = QtMultimedia.QCamera(selected_device)
            self.capsesh.setCamera(self.camera)
            self.capsesh.setVideoOutput(self.webcam_widget)
            self.camera.start()

        



    
    def close_camera(self):
        pass


app = QtWidgets.QApplication(sys.argv)


window  = MainWindow()
window.resize(800, 600)
window.show()


sys.exit(app.exec())