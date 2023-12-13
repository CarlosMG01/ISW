FROM python:3.9-slim-buster
WORKDIR /app
#host: your PC, laptop, cloud server,...
#Copy from "host" to "container"
COPY requirements.txt requirements.txt
#Run this command in the container
RUN pip3 install -r requirements.txt
COPY . .
#contenido exclusiones .dockerignore

#Run command in container
CMD [ "python3", "main.py"]
