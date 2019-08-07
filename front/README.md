# ss_front

A simple dashboard built using [Dash](https://plot.ly/products/dash/).

## Dashboard Design

The design of the dashboard is fairly straightforward, containing three main sections:

- First is the sensor selection (upper left) which allows for filtering which sensor data will be plotted.
- Second is the data filtering (lower left). This allows for selecting the number of minutes of data to plot and the number of minutes to use for creating a rolling average[1].
- Third is the plot. This plot has two subplots, one for moisture and one for temperature[2]. It displays both the raw data and the rolling average for each sensor measurement. Each can be turned on/off by selecting it in the legend.

![ss_front_v0](https://storage.googleapis.com/soil-sense-media/soil_sense_020.png)

----

[1] - The sensor data is saved about once per minute and it is rather noisy, hence the rolling average. The save rate should probably be decreased since the moisture (information I'm after) changes slowly over time.

[2] - The temperature sensor is inaccurate, about +/- 2 degrees Celsius.
