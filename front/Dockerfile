FROM python:3.7-slim

COPY ./requirements.txt .
RUN pip install --trusted-host pypi.python.org -r requirements.txt

WORKDIR /app
COPY . /app

EXPOSE 8050

CMD ["python3", "app.py"]
