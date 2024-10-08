import sys, os
from wasteDetection.logger import logging
from wasteDetection.exception import AppException
from wasteDetection.components.data_ingestion import DataIngestion
from wasteDetection.components.data_validation import DataValidation
from wasteDetection.components.model_trainer import ModelTrainer


from wasteDetection.entity.config_entity import (DataIngestionConfig,
                                                 DataValidationConfig,
                                                 ModelTrainerConfig)

from wasteDetection.entity.artifacts_entity import (DataIngestionArtifact,
                                                    DataValidationArtifact,
                                                    ModelTrainerArtifact)


class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()
        self.model_trainer_config = ModelTrainerConfig()

    def start_data_ingestion(self)-> DataIngestionArtifact:
        try: 
            logging.info(
                "Entered the start_data_ingestion method of TrainPipeline class"
            )
            logging.info("Getting the data from URL")

            data_ingestion = DataIngestion(
                data_ingestion_config =  self.data_ingestion_config
            )
            if not os.path.exists(self.data_ingestion_config.data_ingestion_dir):
                os.makedirs(self.data_ingestion_config.data_ingestion_dir, exist_ok=True)

            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info("Got the data from URL")
            logging.info(
                "Exited the start_data_ingestion method of TrainPipeline class"
            )

            return data_ingestion_artifact

        except Exception as e:
            raise AppException(e, sys)
          
    def start_data_validation(
        self, data_ingestion_artifact: DataIngestionArtifact
    ) -> DataValidationArtifact:
        logging.info("Entered the start_data_validation method of TrainPipeline class")

        try:
            data_validation = DataValidation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_config=self.data_validation_config,
            )

            data_validation_artifact = data_validation.initiate_data_validation()

            logging.info("Performed the data validation operation")

            logging.info(
                "Exited the start_data_validation method of TrainPipeline class"
            )

            return data_validation_artifact

        except Exception as e:
            raise AppException(e, sys) from e
  
    def start_model_trainer(self
    ) -> ModelTrainerArtifact:
        try:
            model_trainer = ModelTrainer(
                model_trainer_config=self.model_trainer_config,
            )
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            return model_trainer_artifact

        except Exception as e:
            raise AppException(e, sys)

    def run_pipeline(self) -> None:
        try:
            STAGE_NAME = "Data Ingestion and Validation stage"
            logging.info(f">>>>>> stage {STAGE_NAME} started <<<<<<") 
            
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(
                data_ingestion_artifact=data_ingestion_artifact
            )
            logging.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")

            STAGE_NAME = "Training"
            logging.info(f">>>>>> stage {STAGE_NAME} started <<<<<<") 
            
            if data_validation_artifact.validation_status == True:
                self.start_model_trainer()
                logging.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")

            else:
                raise Exception("Your data is not in correct format")

        except Exception as e:
            raise AppException(e, sys)
        

if __name__ == '__main__':
    
    obj = TrainPipeline()
    obj.run_pipeline()