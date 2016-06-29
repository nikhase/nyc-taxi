import preprocessing as cleaner
import pandas as pd

# Parameters
# Start und End-date festlegen
start_date = pd.to_datetime('2014-05-05')
end_date=pd.to_datetime('2014-05-12')
dataRoot_month_fileloc = 'data/yellow_tripdata_2014-05.csv'
# dataRoot_week_fileloc = ('..data/'.csv')
dataRoot_tree_model = ('..treelib/', cleaner.filename_tree)
upperleft = [40.856406, -74.020642] # Ridgefield ( lat / long )
lowerright = [40.641547, -73.778118] # JFK  ( lat / long )
data_type = 'Bike' # Bike or Taxi

# print dataRoot_week
# print "Hauptdatensatz aus Verzeichnis: " , dataRoot_data
# print "Ausgeschnittene Woche gespeichert in: " , dataRoot_week


data = cleaner.data_import(dataRoot_month_fileloc , data_type)
data = cleaner.slice_data(data , False , start_date , end_date)
data = cleaner.drop_anomaly(data)

# Speichert alle wichtigen Header in Need und alle unwichtigen, die geloescht werden sollen in drop
columns = data.columns.values.tolist()
list_need = ['pickup_datetime' , 'dropoff_datetime', 'pickup_longitude' ,'trip_distance', 'trip_time' ,
             'pickup_latitude' , 'dropoff_longitude' , 'dropoff_latitude']
list_drop = [x for x in columns if x not in list_need]

data = cleaner.drop_overhead(data, list_drop)
data = cleaner.bounding_box(data)

time_regression_df = cleaner.create_tree_dataframe(data)

# either tree or random forest
test_size = 0.1
random_state = 99
max_depth = 30
export_testset = bool(False)

regtree = cleaner.train_decision_tree(time_regression_df , test_size , random_state , max_depth , export_testset)
#rd_regtree = cleaner.train_random_forest(time_regression_df, test_size , random_state , max_depth , export_testset)
cleaner.dump_tree(regtree , dataRoot_tree_model)