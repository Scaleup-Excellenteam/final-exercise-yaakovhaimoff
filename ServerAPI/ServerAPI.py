import os
import time
import uuid
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Get the parent directory of the current script file
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define the path to the uploads folder
UPLOAD_FOLDER = os.path.join(parent_dir, 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'upload_file' not in request.files:
        return jsonify({'error': 'No file attached'})

    file = request.files['upload_file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'})

    filename = secure_filename(file.filename)
    timestamp = int(time.time())
    uid = str(uuid.uuid4())
    file_name_without_ext, file_ext = os.path.splitext(filename)
    new_filename = f"{file_name_without_ext}_{timestamp}_{uid}{file_ext}"

    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
    file.save(upload_path)

    return jsonify({'uid': uid})


if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
