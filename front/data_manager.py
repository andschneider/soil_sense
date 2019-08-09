import datetime

import pandas as pd

from api_calls import SensorAPI


class DataManager:
    def __init__(self):
        self.sensor_api = SensorAPI()
        self.alert_levels = {}
        self.sensor_ids = self.get_sensor_ids()
        self.plant_names = self.get_plant_names()
        self.sensor_data = {}
        self.cache_data = {}

    def get_sensor_ids(self):
        status, data = self.sensor_api.get_sensor_ids()
        if status == 200:
            return data["sensor_ids"]

    def update_sensor_data(self, minutes, sensor_ids):
        """Pulls data from the database and prepares it for plotting.

        There is a shady caching implementation that stores all the data that has been downloaded and will determine
        whether to download new data or just display cached data.

        Parameters
        ----------
        minutes : int
            The desired number of minutes of data to pull down and display.
        sensor_ids : list
            The sensor ids to get data for.
        """

        for sensor in sensor_ids:
            # get new data the first time the app is loaded
            if self.sensor_data.get(sensor) is None:
                self._get_new_data(minutes, [sensor])
            # compare desired minutes to the already present data and
            # determine the smallest amount of minutes to be pulled from db
            else:
                current_time_diff, dataframe_time_diff = self.compare_time(sensor)
                # case 1 - pull all new data
                if minutes > dataframe_time_diff:
                    self._get_new_data(minutes, [sensor])

                # case 2 - add new data or display already downloaded data
                elif 0 < current_time_diff < dataframe_time_diff:
                    # pull new data from db
                    print(
                        f"pulling new data: {current_time_diff} | {dataframe_time_diff}"
                    )
                    data = self.sensor_api.get_sensor_data(current_time_diff, [sensor])
                    extracted = data["data"].get(str(sensor))
                    new_data = pd.DataFrame(
                        extracted, columns=["date", "temp", "moisture"]
                    )
                    new_data["date"] = pd.to_datetime(new_data["date"])

                    # update cached data
                    self.cache_data[sensor] = (
                        self.cache_data[sensor]
                        .append(new_data, ignore_index=True)
                        .sort_values(by="date", ascending=True)
                        .drop_duplicates(["date"], keep="last")
                    )

                    # change the data that is plotted
                    self.sensor_data[sensor] = self.cache_data[sensor].tail(minutes)

    def compare_time(self, sensor_id):
        """Compares the times in the cached data as well as the current time.

        For example - if the minutes requested was 10, but the current time compared to latest entry is just 5 minutes
        then only 5 minutes of data would be pulled.

        Another example - if the minutes requested was 20, and the current cached dataframe contains only 10
        minutes of data, then the data that will be pulled is the full 20 minutes. This is because the API doesn't
        accept date ranges, it only pulls X amount of minutes from the current time.
        """

        # get min and max minutes in dataframe
        latest = max(self.cache_data[sensor_id]["date"])
        earliest = min(self.cache_data[sensor_id]["date"])

        # change timedelta to minutes
        df_time_dff = (latest - earliest).seconds // 60

        # compare minutes requested to current time
        current_time_diff = (datetime.datetime.utcnow() - latest).seconds // 60
        # print(f"Current:{current_time_diff}, DF: {df_time_dff}")
        return current_time_diff, df_time_dff

    def _get_new_data(self, minutes, sensor_ids):
        data = self.sensor_api.get_sensor_data(minutes, sensor_ids)
        for sensor in sensor_ids:
            # TODO handle when there is no data for the sensor
            sensor_data = pd.DataFrame(
                data["data"][str(sensor)], columns=["date", "temp", "moisture"]
            )

            sensor_data["date"] = pd.to_datetime(sensor_data["date"])
            sensor_data.sort_values(by="date", ascending=True, inplace=True)
            self.sensor_data[sensor] = sensor_data
            # shady caching
            self.cache_data[sensor] = sensor_data.copy(deep=True)

    def get_plant_names(self):
        """Gets the plant name and its sensor id to populate the table."""
        plants = []
        good_ids = []
        for idx, s_id in enumerate(self.sensor_ids):
            status, data = self.sensor_api.get_plant_by_id(s_id)
            if status == 200:
                good_ids.append(s_id)
                plants.append(data["data"])
                self.alert_levels[int(s_id)] = data["data"]["alert_level"]
        self.sensor_ids = good_ids
        return plants
