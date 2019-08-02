# soil sense

*README is wip*

## Overview

The soil sense project is a water moisture monitoring application for house plants. 

There are four main services:

- the __front end__ 
- the __API__ 
- the __database__
- the __alert__ system 

In addition to the web based microservices, the actual moisture sensing is handled with a CircuitPython controlled microcontroller. The microcontroller is connected to WiFi and sends sensor data through the API.

## Testing

To run the application with some test data simply use Docker Compose:

```bash
docker-compose up
```

Once the containers are built and running, the front end can be viewed by going to `localhost:8050` in a browser.
