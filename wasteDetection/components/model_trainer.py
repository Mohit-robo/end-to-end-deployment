import os,sys, shutil
import yaml

from wasteDetection.utils.main_utils import read_yaml_file, unzip_file, get_os_type
from wasteDetection.logger import logging
from wasteDetection.exception import AppException
from wasteDetection.entity.config_entity import ModelTrainerConfig
from wasteDetection.entity.artifacts_entity import ModelTrainerArtifact

import dagshub

os_type = get_os_type()

class ModelTrainer:
    def __init__(
        self,
        model_trainer_config: ModelTrainerConfig,
    ):
        self.model_trainer_config = model_trainer_config
    
        dagshub.init(repo_owner=self.model_trainer_config.github_user_name,  
                    repo_name=self.model_trainer_config.github_repo_name, 
                    mlflow=True)

    def initiate_model_trainer(self,) -> ModelTrainerArtifact:
        logging.info("Entered initiate_model_trainer method of ModelTrainer class")

        try:
            logging.info("Unzipping data")
            if os_type == "Windows":
                unzip_file("data.zip")
            elif os_type == "Linux":
                os.system("unzip data.zip")
    
            # os.system("rm data.zip")

            with open("data.yaml", 'r') as stream:
                num_classes = str(yaml.safe_load(stream)['nc'])

            model_config_file_name = self.model_trainer_config.weight_name.split(".")[0]

            config = read_yaml_file(f"yolov5/models/{model_config_file_name}.yaml")

            config['nc'] = int(num_classes)


            with open(f'yolov5/models/custom_{model_config_file_name}.yaml', 'w') as f:
                yaml.dump(config, f)

            os.system(f"cd yolov5/ && python train.py --img 416 --batch {self.model_trainer_config.batch_size} --epochs {self.model_trainer_config.no_epochs} --data ../data.yaml --cfg ./models/custom_yolov5s.yaml --weights {self.model_trainer_config.weight_name} --name yolov5s_results  --cache --mlflow_uri {self.model_trainer_config.mlflow_tracking_uri}")
            os.makedirs(self.model_trainer_config.model_trainer_dir, exist_ok=True)
            
            if os_type == "Windows":
                shutil.copy('yolov5/runs/train/yolov5s_results/weights/best.pt', 'yolov5/')
                shutil.copy(f'yolov5/runs/train/yolov5s_results/weights/best.pt', self.model_trainer_config.model_trainer_dir)
            elif os_type == "Linux":
                os.system("cp yolov5/runs/train/yolov5s_results/weights/best.pt yolov5/")
                os.system(f"cp yolov5/runs/train/yolov5s_results/weights/best.pt {self.model_trainer_config.model_trainer_dir}/")
           
            # os.system("rm -rf yolov5/runs")
            # os.system("rm -rf train")
            # os.system("rm -rf valid")
            # os.system("rm -rf data.yaml")

            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path="yolov5/best.pt",
            )

            logging.info("Exited initiate_model_trainer method of ModelTrainer class")
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")

            return model_trainer_artifact


        except Exception as e:
            raise AppException(e, sys)
