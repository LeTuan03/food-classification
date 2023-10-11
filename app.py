from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import mysql.connector
import requests
import os
import pandas as pd
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import hashlib
import base64
from io import BytesIO
from PIL import Image
from urllib.parse import quote


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Đặt secret key cho ứng dụng Flask

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
TF_MODEL_URL = "https://tfhub.dev/google/aiy/vision/classifier/food_V1/1"
LABEL_MAP_URL = "aiy_food_V1_labelmap.csv"
IMAGE_SHAPE = (192, 192)


# Địa chỉ endpoint và API Key
endpoint = "https://api.edamam.com/search"
api_key = "9ca782438c98e160bd0bce9eefb597f9"

# Xây dựng URL
url = "https://api.edamam.com/search?app_id=900da95e&app_key=40698503668e0bb3897581f4766d77f9&q="

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

model = tf.keras.Sequential([
    hub.KerasLayer(TF_MODEL_URL, trainable=False)
])

label_map = pd.read_csv(LABEL_MAP_URL)
labels = dict(zip(label_map['id'], zip(
    label_map['name'], label_map['recipe'])))


def preprocess_image(image_path, img_size=(192, 192)):
    img = tf.keras.preprocessing.image.load_img(
        image_path, target_size=img_size)
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array


def predict_image(image_path):
    img_array = preprocess_image(image_path)
    predictions = model.predict(img_array)
    predicted_label, predicted_recipe = labels[np.argmax(predictions)]
    return [predicted_label, predicted_recipe]


def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Letuan191003+",
            database="loginapp"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Err: {err}")
        return None


def is_not_nan(value):
    if isinstance(value, (int, float, np.number)):
        return np.isnan(value)
    return True


def handleGetDetailByName(name, uploaded_image_path):
    api_url = 'https://api.api-ninjas.com/v1/recipe?query={}'.format(
        name)
    response = requests.get(
        api_url, headers={'X-Api-Key': 'hr1Ux+K7r3l8/MBYaBVtyw==z3MjelZ4KdzV9eDI'})
    print(response.json())
    return jsonify({
        'label': name,
        'image_path': uploaded_image_path,
        "detail": response.json()
    })


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')


@app.route('/index.html', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/user.html', methods=['GET', 'POST'])
def user():
    if 'logged_in' not in session or not session['logged_in']:
        print('Please log in first!')
        return redirect('login.html')

    return render_template('user.html')


@app.route('/login.html', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(
                    "SELECT * FROM list_user WHERE username = %s AND password = %s", (username, password))
                result = cursor.fetchone()
                cursor.close()
                connection.close()
                if result:
                    session['logged_in'] = True
                    session['username'] = username
                    print("Login successed")
                    return redirect('/')
                else:
                    print("User name or password error")
            except mysql.connector.Error as err:
                flash(f"Err: {err}", "danger")
                cursor.close()
                connection.close()
    username = session.get('username', None)
    return render_template('login.html')


@app.route('/register.html', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO list_user VALUE (%s, %s)", (username, password))
                connection.commit()
                print("Account created successed")
                cursor.close()
                connection.close()
                return redirect('login.html')
            except mysql.connector.Error as err:
                print(err)
                cursor.close()
                connection.close()

    return render_template('register.html')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    print('Logged out!')
    return redirect('login.html')


@app.route('/process_image', methods=['POST'])
def process_image():
    if 'photo' in request.files:
        file = request.files['photo']
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)

    predicted_label, predicted_recipe = predict_image(filename)
    uploaded_image_path = url_for(
        'static', filename='uploads/' + os.path.basename(filename))
    return handleGetDetailByName(predicted_label, uploaded_image_path)


@app.route('/process_base64', methods=['POST'])
def process_base64():
    data = request.json
    image_data = data.get('image_data', '').split('base64,')[-1]

    if not image_data:
        return jsonify({"error": "Image data is missing!"}), 400

    try:
        image_bytes = base64.b64decode(image_data)
    except base64.binascii.Error:
        return jsonify({"error": "Invalid base64 format!"}), 400

    image = Image.open(BytesIO(image_bytes))
    filename = os.path.join(app.config['UPLOAD_FOLDER'], "temp.png")
    image.save(filename)

    predicted_label, predicted_recipe = predict_image(filename)
    uploaded_image_path = url_for(
        'static', filename='uploads/' + os.path.basename(filename))
    return handleGetDetailByName(predicted_label, uploaded_image_path)


@app.route('/process_text', methods=['POST'])
def process_text():
    data = request.get_json()
    searchName = data.get("searchName", "")
    encoded_text = quote(searchName)
    url = "https://api.edamam.com/search?app_id=900da95e&app_key=40698503668e0bb3897581f4766d77f9&q=" + encoded_text
    response = requests.get(url)
    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        return jsonify({
            "message": "No information"
        })


@app.errorhandler(404)
def error(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
