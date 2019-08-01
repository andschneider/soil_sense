CREATE TABLE sensor_data (
                    created timestamp DEFAULT current_timestamp,
                    sensor_id integer NOT NULL,
                    temperature float NOT NULL,
                    moisture integer NOT NULL
                 );

CREATE TABLE sensor_info (
                    created timestamp DEFAULT current_timestamp,
                    updated timestamp,
                    sensor_id integer PRIMARY KEY,
                    plant varchar(20) NOT NULL,
                    alert_level integer NOT NULL
                 );

CREATE TABLE users (
                id serial primary key,
                username varchar(128) UNIQUE NOT NULL,
                password varchar(255) NOT NULL
                );

COPY sensor_data(created,sensor_id,temperature,moisture) FROM '/modified_data.csv' DELIMITER ',' CSV HEADER;
INSERT INTO sensor_info (sensor_id, plant, alert_level) values (1, 'Monstera', 500);

-- delete data from the future
DELETE FROM sensor_data WHERE created > now();
