# ss_api
Flask API connected to a PostgreSQL backend

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)


## General
This is the API component of the IoT soil sensor. It will link the sensor to the database and the database to the front end. It started as a serverless learning experiment and has morphed into a Dockerized Flask api. The serverless code can be found on the branch `serverless_iced`, or with the `serverless_1.0.0` tag.

Currently the backend is GCP's managed Cloud SQL offering, running PostgreSQL. This is likely to change to a self-hosted Postgres instance.

## Goals
1) ~~Learn some serverless~~
2) Learn more Docker
3) Learn microservice architectures
4) Learn Postgres

## Running Locally with Docker Compose
This is *wip* right now. The Postgres container only has fake data in it right now, among other things. 
```bash
$ docker-compose up
```

## Running Locally connected to CloudSQL
This is for connecting to the real database, hosted using GCP CloudSQL.
1) Start the Cloud SQL proxy.
2) Build the Dockerfile
    ```bash
    $ docker build -t ss_api .
    ```
3) Run the api container:
    ```bash
    $ docker run --network="host" --env-file ./.env.list -p 3030:3030 ss_api
    ```

## Testing
Run the tests using:
```bash
$ python3 -m pytest --cov=endpoints tests/unit -vs
```
