from PyQt5 import QtCore, QtGui, QtWidgets, uic
import sys
from threading import Thread
from assistant import generate_text_response, text_to_speech


class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.thread = None
        self.setupUi(self)

    def setupUi(self, MainWindow):
        # Load UI file
        uic.loadUi("interface.ui", self)

        # Create a QFont object with the desired size
        large_font = QtGui.QFont()
        large_font.setPointSize(
            17
        )  # Set the font size (change the number to the desired size)

        # Set the font for all relevant widgets
        self.setFont(large_font)

        # Find and resize the scrollArea
        scroll_area = self.findChild(QtWidgets.QScrollArea, "scrollArea")
        if scroll_area:
            scroll_area.resize(800, 800)  # Set desired width and height
        else:
            print("ScrollArea not found")

        # Find and resize the groupBox
        group_box = self.findChild(QtWidgets.QGroupBox, "groupBox")
        if group_box:
            group_box.resize(800, 700)  # Set desired width and height
        else:
            print("GroupBox not found")

        # Find and resize the textEdit
        text_edit = self.findChild(QtWidgets.QTextEdit, "textEdit")
        if text_edit:
            text_edit.resize(1200, 1000)  # Set desired width and height
            text_edit.setFont(large_font)  # Set the font for the text edit
        else:
            print("TextEdit not found")

        # Set font for other widgets
        self.lineEdit.setFont(large_font)

        # Connect button click event to generate response
        self.pushButton.clicked.connect(self.generate_response)

        # Connect returnPressed signal of lineEdit to generate_response function
        self.lineEdit.returnPressed.connect(self.generate_response)

    def generate_response(self):
        # Get user input
        user_input = self.lineEdit.text()

        # Start a new thread to generate response
        self.thread = Thread(target=self.process_response, args=(user_input,))
        self.thread.start()

    def process_response(self, user_input):
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
            QtCore.Q_ARG(str, "Assistant: Loading..."),
        )

        # Generate response
        response = generate_text_response(user_input)
        self.textEdit.undo()

        QtCore.QMetaObject.invokeMethod(
            self.textEdit,
            "append",
            QtCore.Qt.QueuedConnection,
            QtCore.Q_ARG(str, "Assistant: " + response),
        )
        self.lineEdit.clear()

        # Call text_to_speech function to convert response to speech
        text_to_speech(response)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()
    sys.exit(app.exec_())
