# ss alerts

A simple Cloud Function to send alerts when a plant needs to be watered or the sensor needs to be restarted.

## Architecture

Cloud Scheduler[0] and Cloud Functions[1] are being tied together to create the alert system.

Cloud Scheduler is used as a cron job scheduler, which calls a HTTP Cloud Function at a set interval. The Cloud Function then takes care of pulling and checking data, and, if needed, sending alerts.

The alerting is done by sending a message to a Slack channel. This is done using the wonderful Notifiers[2] Python library.

The total cost of this is free! Cloud Scheduler is free for up to three jobs per account. Cloud Functions is free up to 2 million invocations. I have set up the alert for once a day, so I am well under the threshold.

## Deployment

The `.env-blank.yaml` should be filled out with correct values and then renamed to `.env.yaml`.

These scripts assume the Google Cloud SDK[3] is installed on your system.

1) Use the `deploy.sh` script to create and/or update the Cloud Function. 
2) Use the `cloud_schedule.sh` script to create the Cloud Scheduler Job. (Note this only needs to be run once)

### Limitations

1) Security

    The Cloud Function is unauthenticated at the moment. This is slightly mitigated by keeping the url for the Function secret, but this not a good long term solution.

---

[0] [Cloud Scheduler](https://cloud.google.com/scheduler/)

[1] [Cloud Functions](https://cloud.google.com/functions/)

[2] [Notifiers](https://pypi.org/project/notifiers/)

[3] [Google Cloud SDK](https://cloud.google.com/sdk/)
