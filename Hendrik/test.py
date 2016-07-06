import preprocessing as pp


# Parameters
# Set start-date (included) und End-date (excluded)
start_date = '2014-05-06'
end_date = '2014-05-13'
# The '..' indicate the path to the parent directory
dataRoot_month_fileloc = '../data/2014-05 - Citi Bike trip data.csv'
upperleft = [40.856406, -74.020642]  # Ridgefield ( lat / long )
lowerright = [40.641547, -73.778118]  # JFK  ( lat / long )
data_type = 'Bike'  # Bike or Taxi

data = pp.data_import(dataRoot_month_fileloc, data_type)
print(len(data))
data = pp.slice_data(data, True, start_date, end_date)
print(len(data))
data = pp.drop_anomaly(data, True , data_type)

# Saves necessary columns in cols_need, infers the unnecessary ones and saves them in cols_drop
columns = data.columns.values.tolist()
cols_need = ['pickup_datetime', 'dropoff_datetime', 'pickup_longitude', 'pickup_latitude',
             'dropoff_latitude', 'dropoff_longitude', 'trip_distance', 'trip_time']
cols_drop = [x for x in columns if x not in cols_need]

data = pp.drop_columns(data, cols_drop)
# Asserts that the pickups and dropoffs per trip are in a given bounding box
data = pp.bounding_box(data, upperleft, lowerright)

time_regression_df = pp.create_tree_df(data ,data_type)

    
# either tree or random forest
test_size = 0.1
random_state = 99
max_depth = 15
n_estimators = 20
export_testset = True


regtree = pp.train_decision_tree(time_regression_df= time_regression_df, test_size=test_size, random_state=random_state,
                                 max_depth=max_depth, export_testset=export_testset)
# rd_regtree = pp.train_random_forest(time_regression_df=time_regression_df, test_size=test_size ,
#                                    random_state=random_state , max_depth=max_depth,n_estimators=n_estimators,
#                                    export_testset=export_testset)


# Set True if you want to visualize the tree
tree_to_pdf = False

if tree_to_pdf:
    # do not export for depth = 30. It's too complex!
    from sklearn import tree

    tree.export_graphviz(regtree, out_file='figures/tree_d15.dot', feature_names=time_regression_df.ix[:, 0:6].columns,class_names=time_regression_df.columns[6])

