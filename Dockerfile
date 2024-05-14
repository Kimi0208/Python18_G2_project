FROM python:3.12

WORKDIR /app

ENV PYTHONDONTWRTITEBYCODE 1
ENV PYTHONUNBUFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt


COPY . .