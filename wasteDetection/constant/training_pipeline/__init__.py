ARTIFACTS_DIR: str = "artifacts"

"""
Data Ingestion related constant start with DATA_INGESTION VAR NAME
"""
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_DOWNLOAD_URL: str = "https://github.com/Mohit-robo/Dataset/raw/main/waste-detection.zip"
LOCAL_DATA_FILE: str = "artifacts/data_ingestion/data.zip"
UNZIP_DIR = "artifacts/data_ingestion"


"""
Data Validation realted contant start with DATA_VALIDATION VAR NAME
"""

DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_STATUS_FILE = 'status.txt'
DATA_VALIDATION_ALL_REQUIRED_FILES = ["train", "valid", "data.yaml"]


"""
MODEL TRAINER related constant start with MODEL_TRAINER var name
"""
MODEL_TRAINER_DIR_NAME: str = "model_trainer"
MODEL_TRAINER_PRETRAINED_WEIGHT_NAME: str = "yolov5s.pt"
MODEL_TRAINER_NO_EPOCHS: int = 1
MODEL_TRAINER_BATCH_SIZE: int = 2
GITHUB_USER_NAME: str = "Mohit-robo"
GITHUB_REPO_NAME: str = "end-to-end-deployment"
S3_MDOEL_NAME: str = "waste_detction_yolov5"
S3_MDOEL_BUCKET: str = "waste-model"

"""
MODEL PREDICTION related constant 
"""
MODEL_WEIGHT_PATH: str = "../artifacts/model_trainer/best.pt"
PREDICTION_IMAGE_PATH: str = "../data/inputImage.jpg"

"""
MLFLOW_TRACKING_URI
"""
MLFLOW_TRACKING_URI:str = "https://dagshub.com/Mohit-robo/end-to-end-deployment.mlflow"