FROM python:3.7-alpine

RUN apk update && apk add \
    gcc \
    musl-dev \
    postgresql-dev \
    python3-dev \
    && pip install --trusted-host pypi.python.org \
    Flask \
    Flask-RESTful \
    psycopg2

WORKDIR /app
COPY . /app
#RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 3030
CMD ["python3", "app.py"]