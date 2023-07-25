FROM python:3.9

RUN apt-get update && apt-get upgrade -y
RUN apt-get update && apt-get install -y python3-opencv
RUN pip install opencv-python
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install Redis

WORKDIR /app
COPY . /app

EXPOSE 80

COPY requirements.txt /app/
RUN pip install -r requirements.txt

ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["gunicorn", "--bind", "0.0.0.0:80", "--access-logfile", "-", "--error-logfile", "-", "django_training.wsgi"]
