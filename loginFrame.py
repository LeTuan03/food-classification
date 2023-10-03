import sys
from PyQt5 import QtWidgets

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Create the central widget and set the layout
        central_widget = QtWidgets.QWidget(self)
        central_layout = QtWidgets.QVBoxLayout()
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)

        # Create the frames
        self.frame_a = QtWidgets.QFrame()
        self.frame_b = QtWidgets.QFrame()

        # Set layouts for the frames
        layout_a = QtWidgets.QVBoxLayout()
        layout_b = QtWidgets.QVBoxLayout()
        self.frame_a.setLayout(layout_a)
        self.frame_b.setLayout(layout_b)

        # Add widgets to the frames
        self.label_a = QtWidgets.QLabel("Frame A")
        layout_a.addWidget(self.label_a)

        self.label_b = QtWidgets.QLabel("Frame B")
        layout_b.addWidget(self.label_b)

        # Create the checkbox
        self.checkbox = QtWidgets.QCheckBox("Switch to frame A")
        self.checkbox.stateChanged.connect(self.switch_frames)

        # Add the checkbox and frames to the window layout
        central_layout.addWidget(self.checkbox)
        central_layout.addWidget(self.frame_a)
        central_layout.addWidget(self.frame_b)

        # Set the window title
        self.setWindowTitle("Two Frames")

        # Show the window
        self.show()

    def switch_frames(self, state):
        if state:
            self.frame_a.show()
            self.frame_b.hide()
        else:
            self.frame_a.hide()
            self.frame_b.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    app.exec_()
