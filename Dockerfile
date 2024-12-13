FROM python:3.12

RUN apt-get update -yq && apt-get upgrade -yq

WORKDIR /usr/src/app

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY . .
