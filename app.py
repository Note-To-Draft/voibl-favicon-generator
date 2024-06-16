from flask import Flask, render_template, request, redirect, url_for, send_file, abort, jsonify
from PIL import Image
import os
import random
import magic
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import Config
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

# Rate limiting
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)

def generate_unique_folder(base_path):
    while True:
        folder_name = ''.join(random.choices('0123456789', k=20))
        folder_path = os.path.join(base_path, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            return folder_path

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/favicon-generator')
def favicon_generator():
    return render_template('crop.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/favicon/<path:filename>')
def serve_favicon(filename):
    secure_name = secure_filename(filename)
    filepath = os.path.join('/home/tmnotetodraft/voibl/static', secure_name)
    if os.path.exists(filepath):
        return send_file(filepath)
    else:
        abort(404)

@app.route('/success')
def success():
    favicon_path = request.args.get('favicon_path')
    return render_template('success.html', favicon_path=favicon_path)

@app.route('/upload', methods=['POST'])
@limiter.limit("10 per minute")
def upload():
    if 'cropped_image' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['cropped_image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Check MIME type
    mime = magic.Magic(mime=True)
    file_mime = mime.from_buffer(file.read(2048))
    file.seek(0)  # Reset file pointer
    if file_mime not in ['image/png', 'image/jpeg', 'image/jpg']:
        return jsonify({'error': 'Invalid file type'}), 400

    if file:
        img = Image.open(file.stream)
        width, height = img.size

        # Determine the size to resize the image to
        if width < 96 and height < 96:
            new_size = (48, 48)
        elif width < 144 and height < 144:
            new_size = (96, 96)
        else:
            new_size = (144, 144)

        img = img.resize(new_size, Image.Resampling.LANCZOS)

        # Generate unique folder in static directory
        static_folder = '/home/tmnotetodraft/voibl/static'
        unique_folder_path = generate_unique_folder(static_folder)
        ico_path = os.path.join(unique_folder_path, 'favicon.ico')

        # Save the ICO file in the unique folder
        img.save(ico_path, format='ICO', sizes=[new_size])

    # Generate the full URL for the favicon
    favicon_url = f"https://www.voibl.com/static/{unique_folder_path.split('/')[-1]}/favicon.ico"

    return redirect(url_for('success', favicon_path=favicon_url))


