import enum
import os

class MacrosStatus(enum.Enum):
    Processing = "Processing"
    PENDING = "Pending"
    DONE = "Done"
    FAILED = "Failed"


class Routes(enum.Enum):
    UPLOAD = "/upload"
    STATUS = "/status"


# Get the parent directory of the current script file
parent_dir = os.path.dirname(os.path.abspath(__file__))

# Define the paths for uploads and outputs folders
UPLOAD_FOLDER = os.path.join(parent_dir, 'uploads')
OUTPUT_FOLDER = os.path.join(parent_dir, 'outputs')

