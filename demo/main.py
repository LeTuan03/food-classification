import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal
import subprocess
import MySQLdb as mdb
import hashlib
from sucd import Ui_MainWindow



def save_credentials(username, password, filename="credentials.txt"):

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    with open(filename, 'a', encoding='utf-8') as file:
        file.write(f"{username} {hashed_password}\n")

def check_credentials(username, password, filename="credentials.txt"):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            stored_username, stored_hashed_password = line.strip().split()
            if stored_username == username and stored_hashed_password == hashed_password:
                return True
    return False

class Login_w(QMainWindow):
    def __init__(self):
        super(Login_w, self).__init__()
        uic.loadUi("login.ui", self)
        self.pushButton.clicked.connect(self.login)
        self.pushButton_2.clicked.connect(self.redirectToReg)
    def login(self):
        un = self.textEdit.toPlainText().strip()
        psw = self.textEdit_2.toPlainText().strip()
        
        # logic login
        if check_credentials(un, psw):
            QMessageBox.information(self, "Login output", "Login success")
            widget.setCurrentIndex(2)
        else:
            QMessageBox.information(self, "Login output", "Login fail")
            widget.setCurrentIndex(0)
    def redirectToReg(self):
        widget.setCurrentIndex(1)

class Reg_w(QMainWindow):   
    def __init__(self):
        super(Reg_w, self).__init__()
        uic.loadUi("signUp.ui", self)
        self.pushButton_2.clicked.connect(self.redirectToLogin)
        self.pushButton.clicked.connect(self.register)
    def redirectToLogin(self):
        widget.setCurrentIndex(0)

    def register(self):
        un = self.textEdit.toPlainText().strip()
        psw = self.textEdit_3.toPlainText().strip()
        save_credentials(un, psw)

class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.clicked.emit()

class Main_w(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Main_w, self).__init__()
        self.setupUi(self)
        self.pushButton_4 = ClickableLabel(self)
        self.pushButton_4.clicked.connect(self.logout)
    def logout(self):
        widget.setCurrentIndex(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = QStackedWidget()

    Login_f = Login_w()
    Reg_f = Reg_w()
    Main_f = Main_w()

    widget.addWidget(Login_f)
    widget.addWidget(Reg_f)
    widget.addWidget(Main_f)
    widget.setFixedHeight(810)
    widget.setFixedWidth(451)
    widget.setCurrentIndex(0)
    widget.show()

    sys.exit(app.exec_())
