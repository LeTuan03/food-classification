from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(451, 810)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(110, 480, 231, 61))
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton.setStyleSheet("QPushButton {\n"
"    background-color: #FCFCFD;\n"
"    color: #36395A;\n"
"    font-size: 18px;\n"
"    border: none;\n"
"    border-radius: 10px;\n"
"    border-bottom: 2px solid #ffd49d;\n"
"}\n"
"")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(110, 560, 231, 61))
        self.pushButton_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_3.setStyleSheet("QPushButton {\n"
"    background-color: #FCFCFD;\n"
"    color: #36395A;\n"
"    font-size: 18px;\n"
"    border: none;\n"
"    border-radius: 10px;\n"
"    border-bottom: 2px solid #ffd49d;\n"
"}\n"
"")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(40, 20, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_4.setStyleSheet("QPushButton {\n"
"    background-color: #FCFCFD;\n"
"    color: #36395A;\n"
"    font-size: 18px;\n"
"    border: none;\n"
"    border-radius: 10px;\n"
"    border-bottom: 2px solid #ffd49d;\n"
"}\n"
"")
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(390, 750, 31, 31))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_5.setStyleSheet("QPushButton {\n"
"    border-radius: 13px;\n"
"    border: 2px solid red;\n"
"}\n"
"")
        self.pushButton_5.setObjectName("pushButton_5")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 160, 451, 251))
        self.label.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.label.setStyleSheet("image: url(:/newPrefix/banner.png)")
        self.label.setText("")
        self.label.setObjectName("label")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(-10, -10, 461, 821))
        self.widget.setStyleSheet("QWidget {\n"
"    background: #fff;\n"
"}")
        self.widget.setObjectName("widget")
        self.widget.raise_()
        self.pushButton.raise_()
        self.pushButton_3.raise_()
        self.pushButton_4.raise_()
        self.pushButton_5.raise_()
        self.label.raise_()
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Upload Image"))
        self.pushButton_3.setText(_translate("MainWindow", "Take A Picture Now"))
        self.pushButton_4.setText(_translate("MainWindow", "Home"))
        self.pushButton_5.setText(_translate("MainWindow", "O"))

    def set_button_action(self, action):
        self.pushButton.clicked.connect(action)


# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     MainWindow = QtWidgets.QMainWindow()
#     ui = Ui_MainWindow()
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#     sys.exit(app.exec_())
