import os
import sys
import zipfile
import gdown
from pathlib import Path
import urllib.request as request
from wasteDetection.utils.main_utils import get_size
from wasteDetection.logger import logging
from wasteDetection.exception import AppException
from wasteDetection.entity.config_entity import DataIngestionConfig
from wasteDetection.entity.artifacts_entity import DataIngestionArtifact


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig = DataIngestionConfig()):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
           raise AppException(e, sys)
        
    
    def download_file(self):

        try: 
            if not os.path.exists(self.data_ingestion_config.local_data_file):
                filename, headers = request.urlretrieve(
                    url = self.data_ingestion_config.data_download_url,
                    filename = self.data_ingestion_config.local_data_file
                )
                logging.info(f"{filename} download! with following info: \n{headers}")
            else:
                logging.info(f"File already exists of size: {get_size(Path(self.data_ingestion_config.local_data_file))}")  

            return self.data_ingestion_config.local_data_file

        except Exception as e:
            raise AppException(e, sys)

    def extract_zip_file(self,zip_file_path: str)-> str:
    #     """
    #     zip_file_path: str
    #     Extracts the zip file into the data directory
    #     Function returns None
    #     """
        try:
            feature_store_path = self.data_ingestion_config.feature_store_file_path
            os.makedirs(feature_store_path, exist_ok=True)
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(feature_store_path)
            logging.info(f"Extracting zip file: {zip_file_path} into dir: {feature_store_path}")

            return feature_store_path

        except Exception as e:
            raise AppException(e, sys)
    

    def initiate_data_ingestion(self)-> DataIngestionArtifact:
        logging.info("Entered initiate_data_ingestion method of Data_Ingestion class")
        try: 
            zip_file_path = self.download_file()
            feature_store_path = self.extract_zip_file(zip_file_path)

            data_ingestion_artifact = DataIngestionArtifact(
                data_zip_file_path = zip_file_path,
                feature_store_path = feature_store_path
            )

            logging.info("Exited initiate_data_ingestion method of Data_Ingestion class")
            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")

            return data_ingestion_artifact

        except Exception as e:
            raise AppException(e, sys)
        
if __name__ == '__main__':
    
    data_ingestion_config = DataIngestionConfig()
    data_ingestion = DataIngestion(
                data_ingestion_config =  data_ingestion_config
            )
    
    data_ingestion_artifact = data_ingestion.initiate_data_ingestion()