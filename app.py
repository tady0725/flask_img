import matplotlib.pyplot as plt
from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
import shutil
# from torch import randint
from werkzeug.utils import secure_filename
import tensorflow as tf
import tensorflow_hub as hub
import random
import matplotlib
matplotlib.use('Agg')

hub_module = hub.load(
    'https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/1')


def img_scaler(image, max_dim=512):

    # Casts a tensor to a new type.
    original_shape = tf.cast(tf.shape(image)[:-1], tf.float32)

    # Creates a scale constant for the image
    scale_ratio = max_dim / max(original_shape)

    # Casts a tensor to a new type.
    new_shape = tf.cast(original_shape * scale_ratio, tf.int32)

    # Resizes the image based on the scaling constant generated above
    return tf.image.resize(image, new_shape)


def load_img(path_to_img):

    # Reads and outputs the entire contents of the input filename.
    img = tf.io.read_file(path_to_img)

    # Detect whether an image is a BMP, GIF, JPEG, or PNG, and
    # performs the appropriate operation to convert the input
    # bytes string into a Tensor of type dtype
    img = tf.image.decode_image(img, channels=3)

    # Convert image to dtype, scaling (MinMax Normalization) its values if needed.
    img = tf.image.convert_image_dtype(img, tf.float32)

    # Scale the image using the custom function we created
    img = img_scaler(img)

    # Adds a fourth dimension to the Tensor because
    # the model requires a 4-dimensional Tensor
    return img[tf.newaxis, :]


app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

# 判斷副檔名


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# @app.route('/')
# def home():

#     return render_template('test.html')


@app.route('/', methods=['GET', 'POST'])
def upload_image():

    if request.method == 'POST':

        if request.values['send'] == '送出':

            allFileList = os.listdir(UPLOAD_FOLDER)
            # print(len(allFileList))
            shutil.rmtree("static/uploads")
            os.mkdir("static/uploads")
            if 'file' not in request.files:
                flash('No file part')

                return redirect(request.url)
            file = request.files['file']
            file2 = request.files['file2']
            print(file, file2)
            if file.filename == '' and file2.filename == '':
                print(request.url)
                flash('No image selected for uploading')
                return render_template('test.html')  # redirect(request.url)
            if file and allowed_file(file.filename) and file2 and allowed_file(file2.filename):
                filename = secure_filename(file.filename)
                filename2 = secure_filename(file2.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                file2.save(os.path.join(
                    app.config['UPLOAD_FOLDER'], filename2))
                # print('upload_image filename: ' + filename)
                filename = 'static\\uploads\\' + filename
                filename2 = 'static\\uploads\\' + filename2
                # print(filename, filename2)

                flash('Image successfully uploaded and displayed below')
                # , filename=filename
                # , filename=str(filename), filename2=str(filename2)
                return render_template('test.html', f1=str(filename), f2=str(filename2))
            else:
                flash('Allowed image types are - png, jpg, jpeg, gif')
                return redirect(request.url)
    else:
        return render_template('test.html')


@app.route('/test', methods=['POST', 'GET'])
def get():

    file = request.files['file']
    file2 = request.files['file2']
    return render_template('tp.html')


@app.route('/processes', methods=['POST', 'GET'])
def test():

    FOLDER = 'static/generate/'
    allFileList = os.listdir(FOLDER)
    # print(len(allFileList))
    shutil.rmtree("static/generate")
    os.mkdir("static/generate")

    all = os.listdir(UPLOAD_FOLDER)

    filen = all[0]
    filen2 = all[1]
    print(filen, filen2)

    filen = 'static\\uploads\\' + filen
    filen2 = 'static\\uploads\\' + filen2

    content_image = load_img(filen)
    style_image = load_img(filen2)
    stylized_image = hub_module(tf.constant(
        content_image), tf.constant(style_image))[0]

    img = stylized_image[0]
    plt.imshow(stylized_image[0])
    # plt.show(img)
    # s = random.randint(1, 100000)
    plt.savefig('static\\generate\\style.jpeg')

    fstyle = "static\\generate\\style.jpeg"
    return render_template('tp.html', f1=filen, f2=filen2, fs=fstyle)


@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    print(request.url)
    return redirect(url_for('static', filename='generate/' + filename), code=301)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', debug=True)
