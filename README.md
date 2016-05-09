nyc-taxi
========

Preprocessing so far:

-	Most zeros in the data are originally NaN-vaules. Therefor the zeros are substituted by NaN for the sake of consistency
-	Dropping of irrelevant columns: rate_code, vendor_id, store_and_fwd_flag
-	converting the timestamps to datetime objects (can also be done while import)
-	As expected, total_amount highy correlates with trip_time_in_secs, trip_distance, pfare_amount and tip_amount (of course, because the price is a function of time and distance). Dropping some columns is recommended.
-	Split the raw data to anomaly-dataset and to the dataset to keep
-	Little investigation of anomaly data: Multi-Mode in total_amount at high values -> random or with purpose? Possible fraud? Further exploration can be done.
-	Start verifying the data
	-	trip_time via dropoff_datetime - picku_datetime
	-	sum_revenue < total_amount
	-	valid avg_velocity
	-	valid avg_revenue_per_mile?
