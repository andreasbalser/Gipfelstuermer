from flask import Flask, request, render_template, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'
TEXT_UPLOADS = 'uploads/text/'
IMAGE_UPLOADS = 'uploads/images/'
os.makedirs(TEXT_UPLOADS, exist_ok=True)
os.makedirs(IMAGE_UPLOADS, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Store submissions in memory for simplicity
submissions = []

@app.route('/')
def index():
    return render_template('index.html', submissions=submissions)

@app.route('/upload', methods=['POST'])
def upload_file():
    name = request.form.get('name')
    message = request.form.get('message')
    image = request.files.get('image')
    
    if image:
        filename = secure_filename(image.filename)
        relative_image_path = os.path.join(IMAGE_UPLOADS, filename)
        image.save(os.path.join('static', relative_image_path))
    else:
        relative_image_path = None
    
    submissions.append({'name': name, 'message': message, 'image': relative_image_path})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
