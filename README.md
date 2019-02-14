# ss_api
Serverless API connected to a PostgreSQL backend

## General
This is the API component of the IoT soil sensor. It will link the sensor to the database and the database to the front end. I will be experimenting with a serverless architecture, using Google’s so called Cloud Functions[1] on the Google Cloud Platform (GCP). The backend will be Postgres hosted on GCP, either using their managed Cloud SQL offering[2] or a self hosted Postgres on a VM using their Compute Engine.

---
[1] [Cloud Functions](https://cloud.google.com/functions/)    
[2] [Cloud SQL](https://cloud.google.com/sql/)    
