import os
import subprocess
import sys
import time
from ClientSide.Client import ExplainerClient

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
web_api_path = os.path.join(parent_dir, 'ServerAPI', 'ServerAPI.py')
explainer_path = os.path.join(parent_dir, 'Explainer', 'Explainer.py')
python_path = sys.executable


def start_web_api():
    # Start the Web API using subprocess.Popen
    subprocess.Popen([python_path, web_api_path])


def start_explainer():
    # Start the Explainer using subprocess.Popen
    subprocess.Popen([python_path, explainer_path])


def delete_content_of_folder(folder_path):
    # Delete all files in the folder
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)


def run_system_test():
    # Start the Web API
    start_web_api()

    # Give some time for the Web API to start
    time.sleep(2)

    # Start the Explainer
    start_explainer()

    # Give some time for the Explainer to start
    time.sleep(2)

    # Create an instance of the ExplainerClient
    client = ExplainerClient('http://127.0.0.1:5000')

    # Upload a sample presentation
    file_path = '/final.pptx'
    uid = client.upload(file_path)
    print("UID:", uid)

    # Wait for the presentation to be processed
    time.sleep(20)
    status = client.status(uid)
    print(repr(status))

    # Wait more for the presentation to be processed
    time.sleep(40)
    # Check the status of the presentation
    status = client.status(uid)
    print(repr(status))

    outputs_folder = os.path.join(parent_dir, 'outputs')
    delete_content_of_folder(outputs_folder)
    uploads_folder = os.path.join(parent_dir, 'uploads')
    delete_content_of_folder(uploads_folder)


if __name__ == '__main__':
    run_system_test()
