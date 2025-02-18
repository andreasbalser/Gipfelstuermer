from flask import Flask, request, render_template, redirect, url_for
from PIL import Image
import os
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'
TEXT_UPLOADS = 'uploads/text/'
IMAGE_UPLOADS = 'uploads/images/'
os.makedirs(TEXT_UPLOADS, exist_ok=True)
os.makedirs(IMAGE_UPLOADS, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

MAX_IMAGE_SIZE = (800, 800)
IMAGE_QUALITY = 70  # JPEG quality from 0 (worst) to 100 (best)

# Store submissions in memory for simplicity
submissions = []
submissionsLayout = []

def updateLayout():
    submissionsLayout.clear()
    for i, submission in enumerate(submissions):
        if i == 0:
            submissionsLayout.append(submission)
            continue
        
        elif submission['start'] != submissions[i-1]['destination']:
            submissionsLayout.append({'name': 'unknown', 'start': submissions[i-1]['destination'], 'destination': submission['start'], 'message': '', 'image': ''})
            
        submissionsLayout.append(submission)

@app.route('/')
def index():
    return render_template('index.html', submissionsLayout=submissionsLayout)

@app.route('/upload', methods=['POST'])
def upload_file():
    name = request.form.get('name')
    date = datetime.now().strftime("%d %b %Y")  # Example: 18 Feb 2025
    start = request.form.get('start')
    destination = request.form.get('destination')
    message = request.form.get('message')
    images = request.files.getlist('images')  # Get multiple files
    image_paths = []

    for image in images:
        if image and image.filename:  # Ensure file exists
            filename = secure_filename(image.filename)
            relative_image_path = os.path.join(IMAGE_UPLOADS, filename)

            with Image.open(image) as img:
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                
                img.thumbnail(MAX_IMAGE_SIZE)
                img.save(os.path.join('static', relative_image_path), "JPEG", quality=IMAGE_QUALITY, optimize=True)

            image_paths.append(relative_image_path)  # Store image paths

    # Add the new submission to the list
    submissions.append({
        'name': name,
        'date': date,
        'start': start,
        'destination': destination,
        'message': message,
        'images': image_paths  # Store list of image paths
    })

    updateLayout()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)