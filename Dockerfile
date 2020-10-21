FROM python:3.8.3-alpine
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# Install psycopg2 depencias
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev


RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ADD . /app/