import os
import json
import time
import glob
import uuid
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Get the parent directory of the current script file
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define the paths for uploads and outputs folders
UPLOAD_FOLDER = os.path.join(parent_dir, 'uploads')
OUTPUT_FOLDER = os.path.join(parent_dir, 'outputs')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER


class Status:
    def __init__(self, status, filename, timestamp, explanation):
        self.status = status
        self.filename = filename
        self.timestamp = timestamp
        self.explanation = explanation


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


@app.route('/status', methods=['GET'])
def get_status():
    uid = request.args.get('uid')
    if uid is None:
        return jsonify({'error': 'Missing UID parameter'})

    # check if file exists in uploads folder
    upload_files = glob.glob(os.path.join(app.config['UPLOAD_FOLDER'], f'*_{uid}.*'))
    if not upload_files:
        return jsonify({'status': "not found", })

    # check if file exists in outputs folder
    output_files = glob.glob(os.path.join(app.config['OUTPUT_FOLDER'], f'*_{uid}.json'))
    if not output_files:
        return jsonify({'status': "pending", })

    output_file_path = output_files[0]
    filename, timestamp = extract_filename_and_timestamp(output_file_path)
    status = 'done'
    explanation = parse_output_file(output_file_path)

    return jsonify({'status': status, 'filename': f"{filename}.pptx", 'timestamp': timestamp, 'explanation': explanation})

def extract_filename_and_timestamp(file_path):
    filename = os.path.basename(file_path)
    filename_parts = filename.split('_')
    timestamp = int(filename_parts[1])
    return '_'.join(filename_parts[:-2]), timestamp


def check_output_file_status(uid):
    output_file_path = os.path.join(app.config['OUTPUT_FOLDER'], f'{uid}.json')
    if os.path.isfile(output_file_path):
        return 'done'
    else:
        return 'pending'


def parse_output_file(output_file_path):
    with open(output_file_path, 'r') as file:
        return json.load(file)


if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
    app.run(debug=True)
