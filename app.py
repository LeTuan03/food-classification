# LABEL_MAP_URL = "https://www.gstatic.com/aihub/tfhub/labelmaps/aiy_food_V1_labelmap.csv"
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QIcon
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
        return Image.open(path)
    except FileNotFoundError:
        print("Please select image")
        return False
    except OSError:
        print("Please select image")
        return False

def recipe(name):
    for j in search(name):
        print(j)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(408, 750)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(0, 0, 411, 751))
        self.graphicsView.setObjectName("graphicsView")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(130, 30, 171, 51))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(120, 170, 181, 181))
        self.label_2.setStyleSheet("image: url(google-lens_image.png)")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(130, 590, 151, 51))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet(".QPushButton {\n"
"    background-color: #1877f2;\n"
"    border: #fff;\n"
"    color: #fff;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
".QPushButton:hover {\n"
"    background-color: #4c95f3;\n"
"    color: #fff;\n"
"    text-decoration: none;\n"
"}""\n"
".QPushButton:click {\n"
"    background-color: #fff;\n"
"    color: #fff;\n"
"    text-decoration: none;\n"
"}"
)
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Lens"))
        MainWindow.setWindowIcon(QIcon("google-lens_image.png"))
        self.label.setText(_translate("MainWindow", "Smart Lens"))
        self.pushButton.setText(_translate("MainWindow", "Select Image"))
        self.pushButton.clicked.connect(self.upload_img)
        
    def upload_img(self):
        filename = QFileDialog.getOpenFileName()
        path = filename[0]
        path = str(path)

        if(is_image(path)):    
            image = cv2.imread(path)
            result = predict_image(path)
            font = cv2.FONT_HERSHEY_SIMPLEX 
            org = (50, 250) 
            fontScale = 3
            color = (255, 0, 0)
            thickness = 10
            org = center_bottom_text_position(image)
            image = cv2.putText(image, result[0], org, font, fontScale, color, thickness, cv2.LINE_AA)
            DISPLAY_SIZE = (640, 480) 
            image_display = cv2.resize(image, dsize=DISPLAY_SIZE, interpolation=cv2.INTER_CUBIC)
            cv2.imshow("Predicted Image", image_display)
            cv2.imshow("Recipe", image_display)
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

