import sys
from openai import OpenAI
from PyQt6 import QtWidgets, QtMultimedia, QtMultimediaWidgets
import interview
import os



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Interviewer")
        self.api_key = ""

        # instantiate widget and layout
        widget = QtWidgets.QWidget()
        page_layout = QtWidgets.QHBoxLayout()
        widget_layout1 = QtWidgets.QVBoxLayout()
        widget_layout2 = QtWidgets.QVBoxLayout()
        page_layout.addLayout(widget_layout1,1)
        page_layout.addLayout(widget_layout2,1)

        
        # instantiate fields
        self.camera_list = QtWidgets.QComboBox()
        self.webcam_widget = QtMultimediaWidgets.QVideoWidget()

        #api key input, verification and submission
        self.api_key_input = QtWidgets.QLineEdit()
        self.api_key_label = QtWidgets.QLabel("Enter your OpenAI API Key: \nDisclaimer: Up to 16 tokens may be used in verification")

        api_key_btn_layout = QtWidgets.QHBoxLayout()
        self.api_key_verify = QtWidgets.QPushButton("Verify", clicked = self.verify_api_key)
        self.api_key_submit = QtWidgets.QPushButton("Submit Key", clicked = self.submit_api_key)
        api_key_btn_layout.addWidget(self.api_key_verify)
        api_key_btn_layout.addWidget(self.api_key_submit)


        #interview domain
        self.role_label = QtWidgets.QLabel("Enter the job role:")
        self.role_input = QtWidgets.QLineEdit()
        self.role_input.setReadOnly(True)
        self.role_input.setStyleSheet("background-color: lightgray;")
        self.industry_label = QtWidgets.QLabel("Enter the industry:")
        self.industry_input = QtWidgets.QLineEdit()
        self.industry_input.setReadOnly(True)
        self.industry_input.setStyleSheet("background-color: lightgray;")

        #interview difficulty
        self.difficulty_label = QtWidgets.QLabel("Select difficulty level:")

        difficulty_layout = QtWidgets.QHBoxLayout()
        self.easy_radio = QtWidgets.QRadioButton("Easy")
        self.medium_radio = QtWidgets.QRadioButton("Medium")
        self.hard_radio = QtWidgets.QRadioButton("Hard")
        difficulty_layout.addWidget(self.easy_radio)
        difficulty_layout.addWidget(self.medium_radio)
        difficulty_layout.addWidget(self.hard_radio)

        #no. of interview questions
        self.question_no_label = QtWidgets.QLabel("Select number of questions:")
        self.questions_no = QtWidgets.QSpinBox()
        self.questions_no.setRange(1, 10)

        #follow up questions enable/disable
        self.follow_up_checkbox = QtWidgets.QCheckBox(text="Enable follow up questions")


        # populate the camera list
        for camera in QtMultimedia.QMediaDevices.videoInputs():
            self.camera_list.addItem(camera.description(), camera)

      



        # instantiate camera and capture session
        self.camera = None
        self.capsesh = QtMultimedia.QMediaCaptureSession()
        selected_index = self.camera_list.currentIndex()
        if selected_index >= 0:
            selected_device = QtMultimedia.QMediaDevices.videoInputs()[selected_index]
            self.camera = QtMultimedia.QCamera(selected_device)
            self.capsesh.setCamera(self.camera)
            self.capsesh.setVideoOutput(self.webcam_widget)
            self.camera.start()

        self.resume_btn = QtWidgets.QPushButton("Upload Resume (.pdf)", clicked = self.upload_resume)

        self.submit_settings_btn = QtWidgets.QPushButton("Submit Settings", clicked = self.submit_settings)
        self.begin_interview_btn = QtWidgets.QPushButton("Begin Interview", clicked = self.begin_interview)

        widget_layout1.addWidget(self.api_key_label)
        widget_layout1.addWidget(self.api_key_input)
        widget_layout1.addLayout(api_key_btn_layout)
        widget_layout1.addWidget(self.role_label)
        widget_layout1.addWidget(self.role_input)
        widget_layout1.addWidget(self.industry_label)
        widget_layout1.addWidget(self.industry_input)
        widget_layout1.addWidget(self.difficulty_label)
        widget_layout1.addLayout(difficulty_layout)
        widget_layout1.addWidget(self.question_no_label)
        widget_layout1.addWidget(self.questions_no)
        widget_layout1.addWidget(self.resume_btn)
        widget_layout1.addWidget(self.follow_up_checkbox)
        widget_layout1.addWidget(self.submit_settings_btn)
        widget_layout1.addWidget(self.begin_interview_btn)

        widget_layout1.addStretch()


        widget_layout2.addWidget(self.camera_list)        

        widget_layout2.addWidget(self.webcam_widget)


        # set layout to widget
        widget.setLayout(page_layout)
        self.setCentralWidget(widget)

    def currentTextChanged(self, text):
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
            errorMsg.setText(f"Invalid API Key, network error or out of credits: \n {error}")
            errorMsg.setIcon(QtWidgets.QMessageBox.Icon.Critical)
            errorMsg.exec()
        else:
            successMsg = QtWidgets.QMessageBox()
            successMsg.setText("API Key verified successfully.")
            successMsg.setIcon(QtWidgets.QMessageBox.Icon.Information)
            successMsg.exec()

    def submit_api_key(self,api_key):
        api_key = self.api_key_input.text()
        print(api_key,"a")
        self.role_input.setReadOnly(False)
        self.industry_input.setReadOnly(False)
        self.role_input.setStyleSheet("background-color: white;")
        self.industry_input.setStyleSheet("background-color: white;")
        self.InterviewInstance = interview.InterviewSession(api_key)

    def upload_resume(self):
        file_dialog = QtWidgets.QFileDialog()
        file_dialog.setNameFilter("PDF files (*.pdf)")
        file_dialog.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFile)
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            self.resume_path = selected_files[0]

            self.resume = self.InterviewInstance.files.create(
                file=open(self.resume_path, "rb"),
                purpose="resume"
            )

            self.InterviewInstance.resume_uploaded = True

    def submit_settings(self):
        self.InterviewInstance.difficulty = self.difficulty_label.text()
        self.InterviewInstance.industry = self.industry_input.text()
        self.InterviewInstance.role = self.role_input.text()
        self.InterviewInstance.questions_no = self.questions_no.value()
        self.InterviewInstance.follow_up = self.follow_up_checkbox.isChecked()

    def begin_interview(self):
        self.InterviewInstance.begin_interview()
        self.InterviewInstance.log.close()


app = QtWidgets.QApplication(sys.argv)


mainForm  = MainWindow()
mainForm.resize(800, 600)
mainForm.show()


sys.exit(app.exec())