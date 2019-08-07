FROM python:3.7-slim

RUN apt-get update && apt-get install -y \
    netcat-openbsd

COPY ./requirements.txt .
RUN pip install --trusted-host pypi.python.org -r requirements.txt

WORKDIR /app
COPY . /app

EXPOSE 8050
CMD ["./entrypoint-test.sh", "python", "app.py"]
