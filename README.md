# ss_api
Flask API connected to a PostgreSQL backend

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)


## General
This is the API component of the IoT soil sensor. It will link the sensor to the database and the database to the front end. It started as a serverless learning experiment and has morphed into a Dockerized Flask api.

Currently the backend is GCP's managed Cloud SQL offering, running PostgreSQL. This is likely to change to a self-hosted Postgres instance.

## Goals
1) ~~Learn some serverless~~
2) Learn more Docker
3) Learn microservice architectures

## Running Locally
1) Start the Cloud SQL proxy.
2) Run the api container:
```bash
$ docker run --network="host" --env-file ./.env.list -p 3030:3030 ss_api
```
