import os
from dataclasses import dataclass
from wasteDetection.constant.training_pipeline import *



@dataclass
class TrainingPipelineConfig:
    artifacts_dir: str = ARTIFACTS_DIR



training_pipeline_config:TrainingPipelineConfig = TrainingPipelineConfig() 


@dataclass
class DataIngestionConfig:
    data_ingestion_dir: str = os.path.join(
        training_pipeline_config.artifacts_dir, DATA_INGESTION_DIR_NAME
    )
    feature_store_file_path: str = os.path.join(
        data_ingestion_dir, DATA_INGESTION_FEATURE_STORE_DIR
    )
    data_download_url: str = DATA_DOWNLOAD_URL
    local_data_file: str = LOCAL_DATA_FILE
    unzip_dir: str = UNZIP_DIR


@dataclass
class DataValidationConfig:
    data_validation_dir: str = os.path.join(
        training_pipeline_config.artifacts_dir, DATA_VALIDATION_DIR_NAME
    )

    valid_status_file_dir: str = os.path.join(data_validation_dir, DATA_VALIDATION_STATUS_FILE)
    required_file_list = DATA_VALIDATION_ALL_REQUIRED_FILES

@dataclass
class ModelTrainerConfig:
    model_trainer_dir: str = os.path.join(
        training_pipeline_config.artifacts_dir, MODEL_TRAINER_DIR_NAME
    )

    weight_name = MODEL_TRAINER_PRETRAINED_WEIGHT_NAME
    no_epochs = MODEL_TRAINER_NO_EPOCHS
    batch_size = MODEL_TRAINER_BATCH_SIZE
    mlflow_tracking_uri = MLFLOW_TRACKING_URI
    github_user_name: str = GITHUB_USER_NAME
    github_repo_name: str = GITHUB_REPO_NAME
    s3_model_name:str = S3_MDOEL_NAME
    s3_model_bucket:str = S3_MDOEL_BUCKET

class ModelPredictionConfig:
    trained_model_file_path: str = MODEL_WEIGHT_PATH
    prediction_image_path: str = PREDICTION_IMAGE_PATH
    s3_model_name:str = S3_MDOEL_NAME
    s3_model_bucket:str = S3_MDOEL_BUCKET