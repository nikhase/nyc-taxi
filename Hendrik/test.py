import preprocessing as pp


# Parameters
# Set start-date (included) und End-date (excluded)
start_date = '2013-05-06'
end_date = '2013-05-13'
# The '..' indicate the path to the parent directory
dataRoot_month_fileloc = '../data/yellow_tripdata_2013-05.csv'
upperleft = [40.856406, -74.020642]  # Ridgefield ( lat / long )
lowerright = [40.641547, -73.778118]  # JFK  ( lat / long )
data_type = 'Taxi'  # Bike or Taxi

data = pp.data_import(dataRoot_month_fileloc, data_type)
print(len(data))
data = pp.slice_data(data, True, start_date, end_date)
print(len(data))
data = pp.drop_anomaly(data, True)

# Saves necessary columns in cols_need, infers the unnecessary ones and saves them in cols_drop
columns = data.columns.values.tolist()
cols_need = ['pickup_datetime', 'dropoff_datetime', 'pickup_longitude', 'pickup_latitude',
             'dropoff_latitude', 'dropoff_longitude', 'trip_distance', 'trip_time']
cols_drop = [x for x in columns if x not in cols_need]

data = pp.drop_columns(data, cols_drop)
# Asserts that the pickups and dropoffs per trip are in a given bounding box
data = pp.bounding_box(data, upperleft, lowerright)

time_regression_df = pp.create_tree_df(data)

    
# either tree or random forest
test_size = 0.1
random_state = 99
max_depth = 30
export_testset = True

regtree = pp.train_decision_tree(time_regression_df, test_size, random_state, max_depth, export_testset)
# rd_regtree = cleaner.train_random_forest(time_regression_df, test_size , random_state , max_depth , export_testset)