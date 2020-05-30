FROM python:3.7-slim

MAINTAINER hamishwhc@gmail.com

USER root

WORKDIR /app

ADD . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 80
EXPOSE 5000

CMD ["python", "run.py"]