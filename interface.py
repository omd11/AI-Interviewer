import sys
from openai import OpenAI
from PyQt6 import QtWidgets, QtMultimedia, QtMultimediaWidgets



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Interviewer")
        self.api_key = ""

        # instantiate widget and layout
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()

        
        # instanstiate fields
        self.label = QtWidgets.QLabel("Welcome to the AI Interviewer!")
        self.camera_list = QtWidgets.QComboBox()
        self.open_btn = QtWidgets.QPushButton("Open Camera",clicked = self.open_camera)
        self.setclose_btn = QtWidgets.QPushButton("Close Camera",clicked = self.close_camera)
        self.webcam_widget = QtMultimediaWidgets.QVideoWidget()
        self.api_key_input = QtWidgets.QLineEdit()
        self.api_key_label = QtWidgets.QLabel("Enter your OpenAI API Key:")
        self.api_key_verify = QtWidgets.QPushButton("Verify", clicked = self.verify_api_key)
        self.api_key_submit = QtWidgets.QPushButton("Submit", clicked = self.submit_api_key)

        # populate the camera list
        for camera in QtMultimedia.QMediaDevices.videoInputs():
            self.camera_list.addItem(camera.description(), camera)

        # add fields to layout
        layout.addWidget(self.api_key_label)
        layout.addWidget(self.api_key_input)
        layout.addWidget(self.api_key_verify)
        layout.addWidget(self.api_key_submit)
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

    def verify_api_key(self, api_key):
        api_key = self.api_key_input.text()
        client = OpenAI(api_key = api_key)
        try:
            client.responses.create(
            model = "gpt-4o-mini",
            input= "placeholder",
            max_output_tokens= 16
            )
        except Exception as error:
            errorMsg = QtWidgets.QMessageBox()
            errorMsg.setText(f"Invalid API Key, network error or out of credits. {error}")
            errorMsg.setIcon(QtWidgets.QMessageBox.Icon.Critical)
            errorMsg.exec()
        else:
            successMsg = QtWidgets.QMessageBox()
            successMsg.setText("API Key verified successfully.")
            successMsg.setIcon(QtWidgets.QMessageBox.Icon.Information)
            successMsg.exec()

    def submit_api_key(self,api_key):
        api_key = self.api_key_input.text()
        self.api_key = api_key


        
    
    def close_camera(self):
        pass


app = QtWidgets.QApplication(sys.argv)


mainForm  = MainWindow()
mainForm.resize(800, 600)
mainForm.show()


sys.exit(app.exec())