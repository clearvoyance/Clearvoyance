import os
import socket
from pathlib import Path
# import threading
# import queue

from flask import Flask, render_template, send_from_directory, url_for
from flask_uploads import UploadSet, IMAGES, configure_uploads
    # FLASK_REUPLOADED
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

this_path = Path(__file__).parent
relative = '../../../Photos_Slides'
dir_path = (this_path / relative).resolve()

app = Flask(__name__)
## THIS LINK WORKS RELATIVE TO COMMAND-LINE
app.config['UPLOADED_PHOTOS_DEST'] = str(dir_path)
app.config["SECRET_KEY"] = os.urandom(24)

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

class UploadForm(FlaskForm):
    photo = FileField(
        validators=[
            FileAllowed(photos, 'Only images are allowed'),
            FileRequired('File field cannot be empty.')
        ]
    )
    submit = SubmitField('Upload')


@app.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)


@app.route('/', methods=['GET', 'POST'])
def upload_image():
    form = UploadForm()
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        upload_queue.put(filename)
        file_url = url_for('get_file', filename=filename)
    else:
        file_url = None
    return render_template('index.html', form=form, file_url=file_url)

def store_server(queue):
    global upload_queue
    upload_queue = queue
    app.run(host=ip_address)