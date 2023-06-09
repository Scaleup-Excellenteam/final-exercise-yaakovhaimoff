from dataclasses import dataclass
import requests
from datetime import datetime


@dataclass
class Status:
    status: str
    filename: str
    timestamp: datetime
    explanation: str

    def is_done(self):
        return self.status == 'done'


class ExplainerClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def upload(self, file_path):
        try:
            with open(file_path, 'rb') as file:
                response = requests.post(f'{self.base_url}/upload', files={'upload_file': file})
                if response.status_code == 200:
                    response_data = response.json()
                    uid = response_data['uid']
                    return uid
                else:
                    raise Exception("File upload failed. Status code:", response.status_code)
        except FileNotFoundError:
            print("File not found. Please enter a valid file path.")
        except IOError as e:
            print(str(e))

    def status(self, uid):
        try:
            response = requests.get(f'{self.base_url}/status', params={'uid': uid})
            if response.status_code == 200:
                response_data = response.json()
                status = response_data['status']
                if status == 'not found' or status == 'pending':
                    return Status(status, None, None, None)
                filename = response_data['filename']
                timestamp = datetime.fromtimestamp(int(response_data['timestamp']))
                explanation = response_data['explanation']
                return Status(status, filename, timestamp, explanation)
            else:
                raise Exception("Failed to get status. Status code:", response.status_code)
        except IOError as e:
            print(str(e))


def main():
    client = ExplainerClient('http://127.0.0.1:5000')

    while True:
        command = input("Enter 'upload' to upload file, status to check status of a file or 'quit' to exit): ")

        if command == 'quit':
            break
        elif command == 'upload':
            file_path = input("Enter the file path: ")
            uid = client.upload(file_path)
            print("UID:", uid)
        elif command == 'status':
            uid = input("Enter the UID: ")
            status = client.status(uid)
            print(status.is_done())
            print(repr(status))
        else:
            print("Invalid command")


if __name__ == '__main__':
    main()
