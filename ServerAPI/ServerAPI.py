import os
from flask import Flask, request
from macros import Routes, UPLOAD_FOLDER, OUTPUT_FOLDER
from serverApiService import ServerApiService

app = Flask(__name__)

app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route(Routes.UPLOAD.value, methods=['POST'])
def upload_file():
    return service.upload_file(request, app.config['UPLOAD_FOLDER'])


@app.route(Routes.STATUS.value, methods=['GET'])
def get_status():
    return service.get_status_response(request, app.config['OUTPUT_FOLDER'])


if __name__ == '__main__':
    service = ServerApiService()

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    app.run(debug=True)
