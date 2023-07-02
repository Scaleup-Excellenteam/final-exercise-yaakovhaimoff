from ClientService import ExplainerClient


def upload_command(client):
    command = input("Enter 'user_upload' to upload with email or 'file_upload' to upload with file path: ")
    command_functions.get(command, invalid_command)(client)


def user_upload(client):
    email = get_user()
    file_path = get_file_path()
    client.upload(file_path, email)


def file_upload(client):
    file_path = get_file_path()
    client.upload(file_path, "")


def status_command(client):
    command = input("Enter 'uid' to get status with uid or 'user_status' to get status"
                    " with email and file name: ")
    command_functions.get(command, invalid_command)(client)


def uid(client):
    uid = input("Enter the UID: ")
    status = client.status({'uid': uid})
    print(status.is_done())
    print(repr(status))


def user_status(client):
    email = get_user()
    filename = get_file_path()
    status = client.status({'email': email,
                            'filename': filename})
    print(status.is_done())
    print(repr(status))


def get_user():
    email = input("Enter your email: ")
    return email


def get_file_path():
    filename = input("Enter the file path: ")
    return filename


def invalid_command(*args, **kwargs):
    print("Invalid command")


command_functions = {
    'upload': upload_command,
    'user_upload': user_upload,
    'file_upload': file_upload,
    'status': status_command,
    'uid': uid,
    'user_status': user_status,
}


def main():
    client = ExplainerClient('http://127.0.0.1:5000')

    while True:
        command = input("Enter 'upload' to upload file, 'status' to check status of a file or 'quit' to exit): ")

        if command == 'quit':
            break

        command_functions.get(command, invalid_command)(client)


if __name__ == '__main__':
    main()
