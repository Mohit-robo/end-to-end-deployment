import os.path
import sys
import yaml
import base64
from pathlib import Path
import s3fs
import zipfile
import tempfile

from wasteDetection.exception import AppException
from wasteDetection.logger import logging

# AWS_ACCESS_KEY = os.environ['AWS_ACCESS_KEY_ID']
# AWS_SECRET_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

# logging.info(f"Fetched AWS Creds | AWS_ACCESS_KEY : {AWS_ACCESS_KEY}")
# logging.info(f"Fetched AWS Creds | AWS_SECRET_ACCESS_KEY : {AWS_SECRET_KEY}")

def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, "rb") as yaml_file:
            logging.info("Read yaml file successfully")
            return yaml.safe_load(yaml_file)

    except Exception as e:
        raise AppException(e, sys) from e
    

def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)

        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w") as file:
            yaml.dump(content, file)
            logging.info("Successfully write_yaml_file")

    except Exception as e:
        raise AppException(e, sys)
    
def get_size(path: Path) -> str:
    """get size in KB

    Args:
        path (Path): path of the file

    Returns:
        str: size in KB
    """
    size_in_kb = round(os.path.getsize(path)/1024)
    return f"~ {size_in_kb} KB"


def decodeImage(imgstring, fileName):
    imgdata = base64.b64decode(imgstring)
    with open("./data/" + fileName, 'wb') as f:
        f.write(imgdata)
        f.close()


def encodeImageIntoBase64(croppedImagePath):
    with open(croppedImagePath, "rb") as f:
        return base64.b64encode(f.read())

    
def get_s3fs():
  return s3fs.S3FileSystem(key=AWS_ACCESS_KEY, secret=AWS_SECRET_KEY)


def zipdir(path, ziph):
  # Zipfile hook to zip up model folders
  length = len(path) # Doing this to get rid of parent folders
  for root, _, files in os.walk(path):
    folder = root[length:] # We don't need parent folders! Why in the world does zipfile zip the whole tree??
    for file in files:
      ziph.write(os.path.join(root, file), os.path.join(folder, file))

            
def s3_save_keras_model(model, model_name, BUCKET_NAME):
  with tempfile.TemporaryDirectory() as tempdir:
    model.save(f"{tempdir}/{model_name}")
    # Zip it up first
    zipf = zipfile.ZipFile(f"{tempdir}/{model_name}.zip", "w", zipfile.ZIP_STORED)
    zipdir(f"{tempdir}/{model_name}", zipf)
    zipf.close()
    s3fs = get_s3fs()
    s3fs.put(f"{tempdir}/{model_name}.zip", f"{BUCKET_NAME}/{model_name}.zip")
    logging.info(f"Saved zipped model at path s3://{BUCKET_NAME}/{model_name}.zip")
 

def s3_get_keras_model(model_name: str, BUCKET_NAME: str):
  with tempfile.TemporaryDirectory() as tempdir:
    s3fs = get_s3fs()
    # Fetch and save the zip file to the temporary directory
    s3fs.get(f"{BUCKET_NAME}/{model_name}.zip", f"{tempdir}/{model_name}.zip")
    # Extract the model zip file within the temporary directory
    with zipfile.ZipFile(f"{tempdir}/{model_name}.zip") as zip_ref:
        zip_ref.extractall(f"{tempdir}/{model_name}")
    # Load the keras model from the temporary directory
    return f"{tempdir}/{model_name}"

def unzip_file(zip_path, extract_to='.'):
    """
    Unzips a ZIP file to the specified directory.

    Parameters:
    zip_path (str): The path to the ZIP file to be extracted.
    extract_to (str): The directory where the contents will be extracted.

    Returns:
    None
    """
    # Ensure the extract_to directory exists
    os.makedirs(extract_to, exist_ok=True)
    
    # Open the zip file in read mode
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        # Extract all contents to the specified directory
        zip_ref.extractall(extract_to)
        logging.info(f"Extracted all contents to {extract_to}")

def get_os_type():
    """
    Determines the operating system type using the os library.

    Returns:
    str: The name of the operating system ('Windows', 'Linux', 'MacOS', etc.).
    """
    if os.name == 'nt':
        return "Windows"
    elif os.name == 'posix':
        # Further check for MacOS (Darwin)
        if os.uname().sysname == 'Darwin':
            return "MacOS"
        else:
            return "Linux"
    else:
        return "Unrecognized OS"