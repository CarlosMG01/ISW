FROM python:3.9-slim-buster

WORKDIR /src/app

COPY /requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3","main.py"]
