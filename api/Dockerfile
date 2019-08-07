FROM python:3.7-slim

RUN apt-get update && apt-get install -y \
    netcat-openbsd

WORKDIR /app

# add and install requirements
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 3030
CMD ["/app/entrypoint-test.sh"]
