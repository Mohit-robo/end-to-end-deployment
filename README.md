# DL-End2End

This repository encapsulates a comprehensive deep-learning workflow, guiding you from raw data collection to deploying a fully trained model on the cloud. The project integrates essential components such as data version control, MLFlow for experiment tracking, and Docker for containerization, making it a robust and scalable solution for real-world deep learning applications.

## Key Features
* Logging and Exception Handling
* Modular Coding
* MLFlow - Experiment Tracking
* DVC - Data Version Control
* Flask - Web App
* Docker and AWS for Cloud Deployment

<details>
  <summary><b>Run the App</b></summary>

* <b>Clone the repository</b>
 
    ``` https://github.com/Mohit-robo/end-to-end-deployment.git```

* <b>Create a virtual environment</b> 

    ```
    ### Conda env
    conda create -n waste python=3.7 -y
    conda activate waste

    ### Virtual env
    python3 -m venv waste
    
    source waste/bin/activate ## Linux
    waste/Scripts/activate ## Windows

    ```
* <b>Install Requirements</b> 

    ``` pip install -r requirements.txt```

* <b>Run the App</b>
    
    ``` python app.py```

    open up your local host and port mentioned in the script.
    
    ``` localhost:8080```
  
</details>

## **Step-by-Step Implementation**

### **Step 1: Installation and Setup**

#### **Create a virtual environment**
    
    ### Conda env
    conda create -n waste python=3.7 -y
    conda activate waste

    ### Virtual env
    python3 -m venv waste
    
    source waste/bin/activate ## Linux
    waste/Scripts/activate ## Windows

#### **Install Requirements**

    pip install -r requirements.txt

### **Step 2: Data Gathering**

The URL to the dataset is mentioned in the configs in this [file](wasteDetection/constant/training_pipeline/__init__.py). You can change the URL to your dataset in case you want to use another custom dataset

### **Logging and Exception Handling**

This project incorporates robust logging and exception handling to ensure smooth and traceable execution. Logging provides detailed insights into the workflow by capturing key events, errors, and system states, which aids in debugging and monitoring the application's performance. Exception handling mechanisms are in place to gracefully manage unexpected errors, preventing the application from crashing and ensuring that issues are logged for future analysis. This approach enhances the reliability and maintainability of the entire pipeline.

### **Step 3: Coding**

The directory structure is as shown below:

![Dir Structure](diagrams/coding.png)

Run the ```template.py``` script to automatically create all the required files and folders. Refer to all the files from this repo and test the files individually. 

#### **MLFlow Integration: A Tool for Managing the Machine Learning Lifecycle**

This project leverages MLFlow integrated with DagsHub for efficient experiment tracking, model versioning, and collaboration. Using DagsHub as the remote repository for MLFlow artifacts, you can seamlessly track your experiments, store model artifacts, and visualize performance metrics in one place. This integration ensures that every aspect of your machine learning pipeline is version-controlled and easily accessible, enhancing reproducibility and collaboration within the team.

Once you set up the DagsHub profile, link your current GitHub repo to DagsHub. In the `wasteDetection/constant/training_pipeline/__init__.py` change the `GITHUB_USER_NAME`, `GITHUB_REPO_NAME` and `MLFLOW_TRACKING_URI`.

#### **Model Training**

1. Refering to **Step5**, create and AWS user. As we will be saving the weights into the s3 bucket you need to mention the `S3_MDOEL_NAME` and `S3_MDOEL_BUCKET`. Refer to this [file](wasteDetection/constant/training_pipeline/__init__.py), for the configs.
2. Set the environment variable, here we will set the AWS credentials manually. In the case of Github-Actions, we will be accessing them from GitHub secrets.

        # Windows
        set AWS_ACCESS_KEY_ID=""
        set AWS_SECRET_ACCESS_KEY=""

        # Linux 
        export AWS_ACCESS_KEY_ID=""
        export AWS_SECRET_ACCESS_KEY=""

        python wasteDetection/pipeline/training_pipeline.py

Run the above command to train the object detector model. Check the `artifacts/model_trainer/`  folder, the final weights file will be saved here.  

Now you can check the MLFlow experiment, the DagsHub page would show something such 

![Dir Structure](diagrams/DagsHub.png)

Also, you can log hyperparams, to compare multiple experiments incase to figure out the best-performing combination of hyperparams.
![Dir Structure](diagrams/MLFlow.png)

#### **DVC**

DVC is a tool for version control of data and models. It is used to track the changes in the files or hyperparams. One of the many advantages of DVC is not running the entire pipeline if the step is been performed previously. DVC checks the cache and executes the part of the pipeline not executed previously.

    dvc init
    dvc repro

Now that we have DVC integrated, you can directly run the entire pipeline with DVC commands.

### **Step 4: Testing Flask App Locally**

1. Run the Flask App Locally

        python app.py

2. Open a browser and host ip and the port on which the app is running. In our case:

        localhost:8080

    This opens a page that directs to the `prediction` page. 

3. Incase if you want to access the webcam, open 

        localhost:8080/live

    This will access the webcam

4. In case if you don't have a model trained, open the:  

        localhost:8080/train

### **Step-5: AWS CICD-Deployment with Github-Actions**

   1. Login to the AWS console
   2. Below are the AWS services required:
      
      1.  IAM: To give the necessary permissions to the EC2 machine to access the S3 bucket, ECR and EC@ instance. Set the below policies, when creating a user.
          1. AmazonEC2ContainerRegistryFullAccess
          2. AmazonEC2FullAccess
          3. AmazonS3FullAccess
      2. EC2 machine (Ubuntu): A virtual Machine to host the Docker container and run the use-case.
      3. S3 Bucket: To store the model weights and the data.
      4. ECR: Elastic Container registry to save the Docker image in AWS.
   3. Connect to the EC2 instance. It will open a terminal. Run the following commands:

          sudo apt-get update -y
          sudo apt-get upgrade (Press ENTER when Daemons using outdated libraries window pops up)
          
          curl -fsSL https://get.docker.com -o get-docker.sh
          sudo sh get-docker.sh
          sudo usermod -aG docker ubuntu
          newgrp docker
    
   4. Configure EC2 as self-hosted runner:
        
        A self-hosted runner is a system that you deploy and manage to execute jobs from GitHub Actions on GitHub.com.

            https://github.com/<github-user-name>/<repo-name>/settings/actions/runners/new

            choose the required OS -> then run all the commands on the EC2 instance terminal

   5. Setup GitHub secrets:
    
            https://github.com/<github-user-name>/<repo-name>/settings/secrets/actions

            # Add the values to the bbelow keys one-by-one 
            
            AWS_ACCESS_KEY_ID=
            AWS_SECRET_ACCESS_KEY=
            AWS_REGION = us-east-1
            AWS_ECR_LOGIN_URI = demo>>  566373416292.dkr.ecr.ap-south-1.amazonaws.com
            ECR_REPOSITORY_NAME = waste
   
### Tasks for the next iteration    
* Better data file handling i.e. downloading from the web or drive.
* Auto installing required libraries.
* Exploring DVC functionalities.
* Fast API instead of Flask to run the App locally and for deployment.
