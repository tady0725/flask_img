from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
import shutil
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

# 判斷副檔名


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('test.html')


@app.route('/', methods=['POST'])
def upload_image():
    allFileList = os.listdir(UPLOAD_FOLDER)
    # print(len(allFileList))
    shutil.rmtree("static/uploads")
    os.mkdir("static/uploads")
    if 'file' not in request.files:
        flash('No file part')

        return   # redirect(request.url)

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
        file2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
        # print('upload_image filename: ' + filename)
        filename = 'static\\uploads\\' + filename
        filename2 = 'static\\uploads\\' + filename2
        # print(filename, filename2)

        flash('Image successfully uploaded and displayed below')
        # , filename=filename
        return render_template('test.html', filename=str(filename), filename2=str(filename2))
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)


@app.route('/processes', methods=['POST', 'GET'])
def test():
    return ""
# @app.route('/display/<filename>')
# def display_image(filename):
#     #print('display_image filename: ' + filename)
#     print(request.url)
#     return redirect(url_for('static', filename='uploads/' + filename), code=301)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', debug=True)
