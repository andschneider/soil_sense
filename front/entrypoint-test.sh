#!/bin/sh

set -e

echo "Waiting for API..."

while ! nc -z api 3030; do
  sleep 1
done

echo "API started"

exec "$@"