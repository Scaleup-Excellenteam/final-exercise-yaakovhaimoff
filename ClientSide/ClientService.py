from dataclasses import dataclass
import requests
from datetime import datetime
from macros import Routes, MacrosStatus

@dataclass
class Status:
    status: str
    filename: str
    finish_time: datetime
    explanation: str

    def is_done(self):
        return self.status == MacrosStatus.DONE.value


class ExplainerClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def upload(self, file_path, email):
        try:
            with open(file_path, 'rb') as file:
                response = requests.post(self.base_url + Routes.UPLOAD.value, files={'upload_file': file},
                                         data={'email': email})
                if response.status_code == 200:
                    response_data = response.json()
                    uid = response_data['uid']
                    print("UID:", uid)
                else:
                    raise Exception("File upload failed. Status code:", response.status_code)
        except FileNotFoundError:
            print("File not found. Please enter a valid file path.")
        except IOError as e:
            print(str(e))

    def status(self, params):
        try:
            response = requests.get(self.base_url + Routes.STATUS.value, params=params)
            if response.status_code == 200:
                response_data = response.json()
                status = response_data['status']
                if status != MacrosStatus.DONE.value:
                    return Status(status, None, None, None)
                filename = response_data['filename']
                finish_time = response_data['finish_time']
                explanation = response_data['explanation']['explanations']
                return Status(status, filename, finish_time, explanation)
            else:
                raise Exception("Failed to get status. Status code:", response.status_code)
        except IOError as e:
            print(str(e))
