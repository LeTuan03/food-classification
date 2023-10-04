from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PIL import Image
from googlesearch import search

from PIL import Image
from googlesearch import search

import cv2
import pandas as pd
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub


TF_MODEL_URL = "https://tfhub.dev/google/aiy/vision/classifier/food_V1/1"
LABEL_MAP_URL = "aiy_food_V1_labelmap.csv"
IMAGE_SHAPE = (192, 192)

model = tf.keras.Sequential([
    hub.KerasLayer(TF_MODEL_URL, trainable=False)
])

label_map = pd.read_csv(LABEL_MAP_URL)
labels = dict(zip(label_map['id'], zip(label_map['name'], label_map['recipe'])))
url_image = "2.png" 


def custom_image_path(text):
    return "image: url(" + text + ")"

path_img = custom_image_path(url_image)

def preprocess_image(image_path, img_size=(192, 192)):
    img = tf.keras.preprocessing.image.load_img(image_path, target_size=img_size)
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = img_array / 255.0 
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def predict_image(image_path):
    img_array = preprocess_image(image_path)
    predictions = model.predict(img_array)
    predicted_label, predicted_recipe = labels[np.argmax(predictions)]
    return [predicted_label, predicted_recipe]

def center_bottom_text_position(image):
    x = (image.shape[1] - 640) // 2
    y = image.shape[0] - 50 
    return (x, y)

def is_image(path): 
    try:
        Image.open(path)
        return True
    except FileNotFoundError:
        print("Please select image")
        return False
    except OSError:
        print("Please select image")
        return False

def recipe(name):
    for j in search(name):
        print(j)

def is_not_nan(value):
    if isinstance(value, (int, float, np.number)):
        return not np.isnan(value)
    return True  

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(451, 810)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(150, 30, 151, 41))
        font = QtGui.QFont()
        font.setFamily("JetBrains Mono,monospace")
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet(".QPushButton {\n"
        "  background-color: #FCFCFD;\n"
        "  border-radius: 4px;\n"
        "  color: #36395A;\n"
        "  font-family: \"JetBrains Mono\",monospace;\n"
        "  height: 48px;\n"
        "  font-size: 18px;\n"
        "}\n"
        ".QPushButton:hover {\n"
        "  background-color: #D6D6E7;\n"
        "  color: #36395A;\n"
        "}")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.upload_img)
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(50, 310, 351, 51))
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_2.setGeometry(QtCore.QRect(50, 380, 351, 411))
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(160, 120, 55, 16))
        self.label.setText("")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(50, 90, 351, 211))
        self.label_2.setStyleSheet(path_img)
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "  Take image"))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p></body></html>"))
        self.textBrowser_2.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p></body></html>"))

    def upload_img(self):
        filename = QFileDialog.getOpenFileName()
        path = filename[0]

        if path and is_image(path):   
            _translate = QtCore.QCoreApplication.translate 
            path = str(path)
            styled_path = custom_image_path(path)
            self.label_2.setStyleSheet(styled_path)
            result = predict_image(path)
            if result:
                if result[0]:    
                    self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                    "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                    "p, li { white-space: pre-wrap; }\n"
                    "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
                    "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">"+ result[0] +"</p></body></html>"))
                else:    
                    self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                    "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                    "p, li { white-space: pre-wrap; }\n"
                    "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
                    "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p></body></html>"))
                if result[1] and is_not_nan(result[1]):
                    self.textBrowser_2.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                    "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                    "p, li { white-space: pre-wrap; }\n"
                    "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
                    "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">"+ result[1] +"</p></body></html>"))
                else:
                    self.textBrowser_2.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                    "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                    "p, li { white-space: pre-wrap; }\n"
                    "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
                    "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p></body></html>"))
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            print("No image selected")
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
