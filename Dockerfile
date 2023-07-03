FROM python:3.11-alpine
WORKDIR /var/app
ENV PYTHONPATH=$PYTHONPATH:/var/app
COPY ./app/ .
COPY ./requirements.txt .
RUN pip install -r requirements.txt