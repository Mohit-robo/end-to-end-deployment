import sys,os, shutil
from wasteDetection.pipeline.training_pipeline import TrainPipeline
from wasteDetection.utils.main_utils import decodeImage, encodeImageIntoBase64, get_os_type, s3_get_model
from flask import Flask, request, jsonify, render_template,Response
from flask_cors import CORS, cross_origin
from wasteDetection.constant.application import APP_HOST, APP_PORT
from wasteDetection.entity.config_entity import ModelPredictionConfig

os_type = get_os_type()

app = Flask(__name__)
CORS(app)

class ClientApp:
    def __init__(self):
        self.filename = "inputImage.jpg"



@app.route("/train")
def trainRoute():
    obj = TrainPipeline()
    obj.run_pipeline()
    return "Training Successfull!!" 


@app.route("/")
def home():
    return render_template("index.html")



@app.route("/predict", methods=['POST','GET'])
@cross_origin()
def predictRoute():
    try:
        image = request.json['image']
        decodeImage(image, clApp.filename)

        prediction_config = ModelPredictionConfig()
        # os.system(f"cd yolov5/ && python detect.py --weights {prediction_config.trained_model_file_path} --img 416 --conf 0.5 --source {prediction_config.prediction_image_path}")

        model_path = s3_get_model(prediction_config.s3_model_name, prediction_config.s3_model_bucket)
        os.system(f"cd yolov5/ && python detect.py --weights {model_path} --img 416 --conf 0.5 --source {prediction_config.prediction_image_path}")

        opencodedbase64 = encodeImageIntoBase64("yolov5/runs/detect/exp/inputImage.jpg")
        result = {"image": opencodedbase64.decode('utf-8')}
        if os_type == "Windows":
            shutil.rmtree("yolov5/runs")
        elif os_type == "Linux":
            os.system("rm -rf yolov5/runs")

    except ValueError as val:
        print(val)
        return Response("Value not found inside  json data")
    except KeyError:
        return Response("Key value error incorrect key passed")
    except Exception as e:
        print(e)
        result = "Invalid input"

    return jsonify(result)



@app.route("/live", methods=['GET'])
@cross_origin()
def predictLive():
    try:
        prediction_config = ModelPredictionConfig()

        model_path = s3_get_model()
        # os.system(f"cd yolov5/ && python detect.py --weights {prediction_config.trained_model_file_path} --img 416 --conf 0.5 --source 0")
        os.system(f"cd yolov5/ && python detect.py --weights {model_path} --img 416 --conf 0.5 --source 0")
        
        if os_type == "Windows":
            shutil.rmtree("yolov5/runs")
        elif os_type == "Linux":
            os.system("rm -rf yolov5/runs")
        return "Camera starting!!" 

    except ValueError as val:
        print(val)
        return Response("Value not found inside  json data")
    



if __name__ == "__main__":
    clApp = ClientApp()
    app.run(host=APP_HOST, port=APP_PORT)
