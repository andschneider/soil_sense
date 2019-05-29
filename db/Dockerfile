# Using 9.6 to match CloudSQL
FROM postgres:9.6-alpine

# copy over seed data
COPY ./test_data.csv .

# run create.sql on init
ADD create.sql /docker-entrypoint-initdb.d
