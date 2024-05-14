from PyQt5 import QtCore, QtWidgets
import sys
from threading import Thread
from assistant import generate_text_response, text_to_speech


class Ui_MainWindow(object):
    def __init__(self):
        super().__init__()
        self.thread = None

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(140, 60, 321, 401))
        self.groupBox.setObjectName("groupBox")
        self.scrollArea = QtWidgets.QScrollArea(self.groupBox)
        self.scrollArea.setGeometry(QtCore.QRect(0, 20, 321, 351))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 319, 349))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.textEdit = QtWidgets.QTextEdit(
            self.scrollAreaWidgetContents
        )  # Add textEdit attribute
        self.textEdit.setGeometry(
            QtCore.QRect(0, 0, 321, 351)
        )  # Add textEdit attribute
        self.textEdit.setObjectName("textEdit")  # Add textEdit attribute
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit.setGeometry(QtCore.QRect(0, 370, 231, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(230, 370, 91, 31))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Connect button click event to generate response
        self.pushButton.clicked.connect(self.generate_response)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "GroupBox"))
        self.pushButton.setText(_translate("MainWindow", "Send"))

    def generate_response(self):
        # Get user input
        user_input = self.lineEdit.text()

        # Start a new thread to generate response
        self.thread = Thread(target=self.process_response, args=(user_input,))
        self.thread.start()

    def process_response(self, user_input):
        # Generate response
        response = generate_text_response(user_input)

        # Display response in text edit widget
        QtCore.QMetaObject.invokeMethod(
            self.textEdit,
            "append",
            QtCore.Qt.QueuedConnection,
            QtCore.Q_ARG(str, "You: " + user_input),
        )
        QtCore.QMetaObject.invokeMethod(
            self.textEdit,
            "append",
            QtCore.Qt.QueuedConnection,
            QtCore.Q_ARG(str, "Assistant: " + response),
        )
        self.lineEdit.clear()

        # Call text_to_speech function to convert response to speech
        text_to_speech(response)


class MyMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())
