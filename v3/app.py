from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import mysql.connector

import os
import pandas as pd
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import hashlib
import base64
from io import BytesIO
from PIL import Image


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Đặt secret key cho ứng dụng Flask

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
TF_MODEL_URL = "https://tfhub.dev/google/aiy/vision/classifier/food_V1/1"
LABEL_MAP_URL = "aiy_food_V1_labelmap.csv"
IMAGE_SHAPE = (192, 192)

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


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')


@app.route('/index.html', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/user.html', methods=['GET', 'POST'])
def user():
    if 'logged_in' not in session or not session['logged_in']:
        flash('Please log in first!')
        return redirect('login.html')
    uploaded_image_path = None
    if request.method == 'POST' and 'photo' in request.files:
        file = request.files['photo']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)

        predicted_label, predicted_recipe = predict_image(filename)
        uploaded_image_path = url_for(
            'static', filename='uploads/' + file.filename)

        return render_template('user.html',
                               nameOfPredictImage=predicted_label,
                               recipe=predicted_recipe,
                               uploaded_image=uploaded_image_path)

    return render_template('user.html',
                           nameOfPredictImage=None,
                           recipe=None,
                           uploaded_image=uploaded_image_path)


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


@app.route('/process_image', methods=['POST'])
def process_image():
    data = request.json
    image_data = data.get('image_data', '').split('base64,')[-1]
    image_bytes = base64.b64decode(image_data)
    image = Image.open(BytesIO(image_bytes))

    # Lưu ảnh
    filename = os.path.join(app.config['UPLOAD_FOLDER'], "temp.png")
    image.save(filename)

    predicted_label, predicted_recipe = predict_image(filename)
    uploaded_image_path = url_for('static', filename='uploads/temp.png')
    if is_not_nan(predicted_recipe):
        return jsonify({
            'label': predicted_label,
            'recipe': 'no recipe',
            'image_path': uploaded_image_path
        })
    return jsonify({
        'label': predicted_label,
        'recipe': predicted_recipe,
        'image_path': uploaded_image_path
    })


@app.errorhandler(404)
def error(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
