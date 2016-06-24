nyc-taxi
========

Preprocessing so far:

-	Most zeros in the data are originally NaN-vaules. Therefor the zeros are substituted by NaN for the sake of consistency
-	Dropping of irrelevant columns: rate_code, vendor_id, store_and_fwd_flag
-	converting the timestamps to datetime objects (cannot be done while import)
-	As expected, total_amount highy correlates with trip_time_in_secs, trip_distance, pfare_amount and tip_amount (of course, because the price is a function of time and distance). Dropping some columns is recommended.
-	Split the raw data to anomaly-dataset and to the dataset to keep
-	Little investigation of anomaly data: Multi-Mode in total_amount at high values -> random or with purpose? Possible fraud? Further exploration can be done.
-	Start verifying the data
	-	trip_time via dropoff_datetime - picku_datetime
	-	sum_revenue < total_amount
	-	valid avg_velocity
	-	valid avg_revenue_per_minute?
-	Trained the model for 2013-05-06 till 12
-	Apply the model for 2014-05-05 till 11
-	filtering: have a look at fare_amount ("static" fares excluded:) sould not be less than 0.5 $ per minute (i.e. the car is not mocing) and Integration of Bike Data ========================

We have the following features:

```
'tripduration', 'starttime', 'stoptime', 'start station id',
'start station longitude', 'end station id', 'end station name',
'end station latitude', 'end station longitude', 'bikeid', 'usertype',
'birth year', 'gender']
```

To use them in the standard pipeline together with the taxidata, the features are renamed to:

```
new_column_names = ['trip_time', 'pickup_datetime', 'dropoff_datetime', 'start_station_id',
       'start_station_name', 'pickup_latitude',
       'pickup_longitude', 'end_station_id', 'end_station_name',
       'dropoff_latitude', 'dropoff_longitude', 'bikeid', 'usertype',
       'birth year', 'gender']
```

In the next step, the times and dates are transformed to *datetime-* and *timedelta-* object, respectively.

We face the situation, that we have distinct start- and endpoints and not arbitrary ones like in the taxi-setting. This means, when calculating the estimated time for taking a bike, one needs to take the way to the start station and the way from the end station into account. As a consequence, we meed to make efforts to extract the "real trips" out of the bike data, i.e. the pure time between two stations. We also need to approximate the distance between two stations to get a feeling for the average velocity of a bike. This will be a filter criterion to select the "pure" trips only.

Todos:
======

-	Zweite Maiwoche ausschneiden (Taxi und Bike)
-	avg_velo ist target bei bike-Daten
-	avg_velo bereinigen: zu kleine und zu große raus
-	wieso sagen wir bei Taxi Zeit statt avg_velo voraus? Aufgrund des Skalierungsfehlers und der leichteren Interpretierbarkeit: lieber "5 min länger gebraucht" statt 10 mp/h vs 12 mp/h
-	Visualize Trees
-	Take into account the distance to the next bike station -> not needed, we only have a look at average velocity
-	Make a better model for the bikes
