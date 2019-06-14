import os
from flask import Flask, request, redirect, url_for
from flask import send_file
from werkzeug.utils import secure_filename
from libs import *
from vars import *

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__,static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if os.path.exists(OUTPUT_IMG):
        os.remove(OUTPUT_IMG)
    for _ in os.listdir(UPLOAD_FOLDER):
        os.remove(UPLOAD_FOLDER+_)
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            saved_file_name = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(saved_file_name)
            if os.path.exists(saved_file_name):
                representations = load_obj(REPRESENTATIONS)
                found_faces = load_obj(FOUND_FACES)
                input_img = saved_file_name
                load_image_and_save(input_img,representations,found_faces)
                if os.path.exists(OUTPUT_IMG):
                    base_url = BASE_URL
                    base_url+='<img src="'+OUTPUT_IMG+'">'
                    return send_file(OUTPUT_IMG,mimetype='image/gif')
                    #return base_url
            return BASE_URL
    return BASE_URL
#redirect(url_for('upload_file',filename=filename))
