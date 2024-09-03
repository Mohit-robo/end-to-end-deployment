FROM python:3.8-slim-buster

WORKDIR /app
COPY . /app

RUN apt update -y && apt install awscli -y
RUN apt-get install ffmpeg libsm6 libxext6 unzip -y

RUN pip install torch==1.13.0+cu116 \
            torchvision==0.14.0+cu116 \
            torchaudio==0.13.0 --extra-index-url https://download.pytorch.org/whl/cu116

RUN pip install -r requirements.txt

CMD ["python3", "app.py"]