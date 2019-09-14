# soil sense

## Overview

The soil sense project is a water moisture monitoring application for house plants.

There are four main services:

- the __front end__
- the __API__
- the __database__
- the __alert__ system

In addition to the web based microservices, the actual moisture sensing is handled with a CircuitPython controlled microcontroller. The microcontroller is connected to WiFi and sends sensor data through the API. This code can be found in the [ss_device](https://github.com/andschneider/ss_device) repo.

## Running Locally

To run the application with some test data simply use Docker Compose:

```bash
docker-compose up
```

- Once the containers are built and running, the front end can be viewed by going to `localhost:8050` in a browser.

- To run tests on the API and get the test coverage, run the following:

    ```bash
    docker-compose exec api python3 -m pytest --cov=api
    ```

- Swagger documentation for the API can be viewed by going to `localhost:3030/api/docs`.

## Deployment

Currently the API is deployed to Google Kubernetes Engine (GKE). The goal is to host everything on GKE, but there are some security concerns with the front end (no login) that I would like to address first. Check back later!
