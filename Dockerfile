# syntax=docker/dockerfile:experimental
FROM python:3.7.6-slim
ENV DISPLAY=:99
WORKDIR /app

ADD ./scripts/setup.sh /app/scripts/setup.sh
ADD ./requirements.txt /app/requirements.txt
ADD ./commonutils /app/commonutils

RUN bash scripts/setup.sh

RUN pip install -r requirements.txt
RUN pip install ./commonutils
ADD ./ /app
CMD ["bash", "./scripts/run.sh"]
