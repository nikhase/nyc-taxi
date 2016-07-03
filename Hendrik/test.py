import preprocessing as pp
from sklearn import cross_validation as cv
from sklearn.tree import DecisionTreeRegressor
import pandas as pd
import time
from sklearn.externals import joblib

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

#def train_decision_tree(time_regression_df, test_size, rs, md, export_testset):
#    y = time_regression_df['trip_time']
#    x = time_regression_df.ix[:, 0:6]
#    x_train, x_test, y_train, y_test = cv.train_test_split(x, y, test_size=test_size, random_state=random_state)
#
#    # if export_testset:
#    #    xy_test = pd.concat([x_test, y_test], axis=1)
#    #W    xy_test.to_csv('../data/' + filename_prefix + '_testset.csv')
#
#    tic = time.time()
#
#    regtree = DecisionTreeRegressor(max_depth=md, min_samples_split=3, random_state=rs)
#    regtree = regtree.fit(x_train.dropna(), y_train.dropna())
#    elapsed = time.time() - tic
#    print(elapsed)
#    # export_meta_data(regtree, X_test, y_test, elapsed)
#    target_location = ('../treelib/' + '_tree_depth_' + str(regtree.tree_.max_depth))
#    dump_model(regtree, target_location)
#    return regtree
#    
#def dump_model(decision_model, target_location):
#    joblib.dump(decision_model, (target_location + '.pkl'), protocol=2)
    
# either tree or random forest
test_size = 0.1
random_state = 99
max_depth = 30
export_testset = True

regtree = pp.train_decision_tree(time_regression_df, test_size, random_state, max_depth, export_testset)
# rd_regtree = cleaner.train_random_forest(time_regression_df, test_size , random_state , max_depth , export_testset)