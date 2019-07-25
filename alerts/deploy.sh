#!/bin/bash

# simple deploy call (note it can take a couple minutes to finish)

gcloud functions deploy check_moisture --env-vars-file .env.yaml --runtime python37 --trigger-http
