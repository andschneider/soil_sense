#!/bin/bash

# create a Cloud Scheduler job to hit a Cloud Function HTTP endpoint (specified in an environment variable)
# it is set up to go off everday at 6 PM PCT

JOB_NAME=check_moisture
TIME_ZONE=America/Los_Angeles

gcloud scheduler jobs create http $JOB_NAME \
        --schedule "0 18 * * *" \
        --uri $CLOUD_SCHEDULE_URI \
        --time-zone $TIME_ZONE
