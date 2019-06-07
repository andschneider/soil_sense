FROM python:3.7-slim

#RUN apk update && apk add \
#    gcc \
#    musl-dev \
#    postgresql-dev \
#    python3-dev

WORKDIR /app

# add and install requirements
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 3030
CMD ["flask", "run", "-h", "0.0.0.0", "-p", "3030"]