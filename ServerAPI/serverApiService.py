import os
import json
import glob
import uuid
from werkzeug.utils import secure_filename
from flask import jsonify
from abc import ABC, abstractmethod
from datetime import datetime
from DB.database import engine, User, Upload
from sqlalchemy.orm import Session
from sqlalchemy import desc
from macros import MacrosStatus


def save_upload_in_db(email, uid, filename):
    with Session(engine) as session:
        upload = Upload(filename=filename,
                        uid=uid,
                        upload_time=datetime.now())

        if email:
            user = session.query(User).filter(User.email == email).first()
            if not user:
                user = User(email=email)
                session.add(user)
                session.commit()

            upload.user_id = user.id

        session.merge(upload)
        session.commit()


def save_file_in_upload_folder(folder_path, file, filename, uid):
    # save file in uploads folder
    file_name_without_ext, file_ext = os.path.splitext(filename)
    new_filename = f"{uid}{file_ext}"

    upload_path = os.path.join(folder_path, new_filename)
    file.save(upload_path)


def get_output_file_status_with_email_and_filename(email, filename):
    with Session(engine) as session:
        user = session.query(User).filter(User.email == email).first()
        if not user:
            return None

        latest_upload = session.query(Upload). \
            filter(Upload.filename == filename, Upload.user == user). \
            order_by(desc(Upload.upload_time)).first()

    return latest_upload.filename, latest_upload.uid, latest_upload.finish_time, latest_upload.status


def get_output_file_status_with_uid(uid):
    with Session(engine) as session:
        upload = session.query(Upload).filter(Upload.uid == uuid.UUID(uid)).first()
        if upload:
            return upload.filename, upload.finish_time, upload.status
        else:
            return None


def parse_output_file(output_file_path):
    with open(output_file_path, 'r') as file:
        return json.load(file)


class ServerApi(ABC):

    @abstractmethod
    def upload_file(self, request, upload_path):
        pass

    @abstractmethod
    def get_status_response(self, request, output_path):
        pass


class ServerApiService(ServerApi):

    def upload_file(self, request, upload_path):
        if 'upload_file' not in request.files:
            return jsonify({'error': 'No file attached'})

        file = request.files['upload_file']
        email = request.form.get('email')
        filename = secure_filename(file.filename)
        uid = uuid.uuid4()

        # save file in uploads db
        save_upload_in_db(email, uid, filename)

        uid = str(uid)

        if file.filename == '':
            return jsonify({'error': 'No file selected'})

        save_file_in_upload_folder(upload_path, file, filename, uid)
        return jsonify({'uid': uid})

    def get_status_response(self, request, output_path):
        uid = request.args.get('uid')
        filename = request.args.get('filename')
        email = request.args.get('email')
        if uid:
            filename, finish_time, status = get_output_file_status_with_uid(uid)
        elif email and filename:
            filename, uid, finish_time, status = get_output_file_status_with_email_and_filename(email, filename)
        else:
            return jsonify({'error': 'No uid or email and filename provided'})

        if status != MacrosStatus.DONE.value:
            return jsonify({'status': status})

        # check if file exists in outputs folder
        output_files = glob.glob(os.path.join(output_path, f'{uid}.json'))
        if not output_files:
            return jsonify({'status': status, })

        output_file_path = output_files[0]
        explanation = parse_output_file(output_file_path)
        return jsonify(
            {'status': status, 'filename': f"{filename}", 'finish_time': finish_time, 'explanation': explanation})
