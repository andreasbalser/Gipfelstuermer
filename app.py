from flask import Flask, request, render_template, redirect, url_for
from PIL import Image
import os
from werkzeug.utils import secure_filename

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

@app.route('/')
def index():
    return render_template('index.html', submissions=submissions)

@app.route('/upload', methods=['POST'])
def upload_file():
    name = request.form.get('name')
    start = request.form.get('start')
    destination = request.form.get('destination')
    message = request.form.get('message')
    image = request.files.get('image')
    
    if image:
        filename = secure_filename(image.filename)
        relative_image_path = os.path.join(IMAGE_UPLOADS, filename)

        with Image.open(image) as img:
            # Convert to RGB if necessary (for consistent JPEG format)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            
            # Resize and compress the image
            img.thumbnail(MAX_IMAGE_SIZE)  # Resize to fit within max dimensions
            img.save(os.path.join('static', relative_image_path), "JPEG", quality=IMAGE_QUALITY, optimize=True)  # Save as JPEG with quality compression
        
    else:
        relative_image_path = None
    
    submissions.append({'name': name, 'start': start, 'destination': destination, 'message': message, 'image': relative_image_path})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
