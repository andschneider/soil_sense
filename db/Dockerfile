# Using 9.6 to match CloudSQL
FROM postgres:9.6-alpine

# copy over seed data
COPY ./test_data.csv .

# overwrite the data's date to today (in utc)
RUN sed "s/2019-05-28/$(date '+%Y-%m-%d' -u)/" test_data.csv > modified_data.csv

# run create.sql on init
ADD create.sql /docker-entrypoint-initdb.d
