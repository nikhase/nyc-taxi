import pandas as pd
import numpy as np
from sklearn import cross_validation as cv
from sklearn.tree import DecisionTreeRegressor
import numpy as np
import matplotlib.pyplot as plt
import time
from sklearn.externals import joblib
from sklearn.ensemble import RandomForestRegressor
import json as js

global filename;


    def data_import(self, dataRoot_import):
        data = pd.read_csv(dataRoot_import) #
        # Parse the datestrings to datetime-objects
        data['pickup_datetime'] = pd.to_datetime(data['pickup_datetime'], format = '%Y-%m-%d %H:%M:%S')
        data['dropoff_datetime'] = pd.to_datetime(data['dropoff_datetime'], format ='%Y-%m-%d %H:%M:%S')
        data['trip_time'] = data.dropoff_datetime - data.pickup_datetime
        return data

    def slice_data(self, dataRoot_data, dataRoot_week, start_date, end_date):
        # Initialize the filename
        filename = ('taxi_from_' + start_date + 'to_' + end_date)
        sdata = pd.read_csv(dataRoot_data)
        data['pickup_datetime'] = pd.to_datetime(self._data['pickup_datetime'], format='%Y-%m-%d %H:%M:%S')
        data['dropoff_datetime'] = pd.to_datetime(self._data['dropoff_datetime'], format='%Y-%m-%d %H:%M:%S')
        date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        mask = (data['pickup_datetime'] >= start_date) & (self._data['pickup_datetime'] < end_date)
        week = pd.DataFrame()
        week = self._data[mask]
        week = week.sort_values('pickup_datetime')
        week.reset_index(drop=True, inplace=True)
        week.to_csv(dataRoot_week)
        self._data = week
        return self._data

    def drop_overhead(self,drop_list):
        for x in drop_list:
            self._data = self._data.drop(str(x), axis=1)
        return self._data

    def drop_anomaly(self):
        lower_bound = 0.5
        upper_bound = 2.5
        self._data['avg_amount_per_minute'] = (data.fare_amount - 2.5) / (data.trip_time / np.timedelta64(1, 'm'))
        self._data = self._data.replace(np.float64(0), np.nan)

        anomaly = self._data.loc[(self._data['dropoff_longitude'].isnull()) | (self._data['dropoff_latitude'].isnull()) | (self._data['pickup_longitude'].isnull()) | (self._data['pickup_latitude'].isnull()) | (self._data['trip_time'].isnull()) | (self._data['trip_distance'].isnull())]
        anomaly = anomaly.append(self._data.loc[(data['avg_amount_per_minute'] > upper_bound) | (data['avg_amount_per_minute'] < lower_bound)])
        self._data = self._data.drop(anomaly.index)
        return self._data

    def bounding_box(upperLeft_ lowerRight):
        #Gesamt-Rahmen in dem die Application stattfinden soll ( Breitengrad / Längengrad lat/long )
        #Zeile 57  Parameter: upperleft , lower_right Koordinaten
        jfk_geodata = (40.641547, -73.778118) #lowerright (lat/long)
        ridgefield_geodata = (40.856406, -74.020642) #upperleft (lat/long)
        self._data = data.loc[(self._data['dropoff_latitude'] > jfk_geodata[0]) &
                               (self._data['dropoff_longitude'] < jfk_geodata[1]) &
                               (self._data['dropoff_latitude'] < ridgefield_geodata[0]) &
                               (self._data['dropoff_longitude'] > ridgefield_geodata[1]) &
                               (self._data['pickup_latitude'] > jfk_geodata[0]) &
                               (self._data['pickup_longitude'] < jfk_geodata[1]) &
                               (self._data['pickup_latitude'] < ridgefield_geodata[0]) &
                               (self._data['pickup_longitude'] > ridgefield_geodata[1])
                               ]
        return self._data


    def train_decision_tree(self, time_regression_df, test_size, random_state, max_depth, export_testset):

        y = time_regression_df["trip_time_in_mins"]
        X = time_regression_df.ix[:, 0:6]
        X_train, X_test, y_train, y_test = cv.train_test_split(X, y, test_size=test_size, random_state=random_state)

        if bool(export_testset) is True:
            Xy_test = pd.concat([X_test, y_test], axis=1)
            Xy_test.to_csv('taxi_tree_test_Xy_20130506-12.csv')

        t = time.time()

        regtree = DecisionTreeRegressor(min_samples_split=3, random_state=random_state, max_depth=max_depth)
        regtree.fit(X_train, y_train)
        elapsed = time.time() - t;
        export_meta_data(regtree, X_test, y_test, elapsed)


    def export_meta_data(tree_model , X_test, y_test, training_duration )
        # Export Meta-File
        # Determine the tree error
        y_pred = tree_model.predict(X_test)
        np.linalg.norm(np.ceil(y_pred) - y_test)
        diff = (y_pred - y_test)
        # plt.figure(figsize=(12,10)) # not needed. set values globally
        plt.hist(diff.values, bins=40)
        error_distribution = ('Perzentile(%): ', [1, 5, 10, 15, 25, 50, 75, 90, 95, 99], '\n',
              np.percentile(diff.values, [1, 5, 10, 15, 25, 50, 75, 85, 90, 95, 99]))
        absolute_deviation = ('Absolute time deviation (in 1k): ', sum(abs(diff)) )
        mean_deviation = absolute_deviation/len(y_pred)
        plt.title('Simple Decision Tree Regressor')
        plt.xlabel('deviation in minutes')
        plt.ylabel('frequency')
        plt.savefig((filename, '_error_plot.png')
        tree_meta_data = {'training_time' : training_duration,
                          'absolute_time_deviation': absolute_deviation,
                          'mean_abs._deviation': mean_deviation,
                          'error_distribition': error_distribution,
                          'max_depth': tree_model.tree_.max_depth,
                          'leaves_number': 'Amount if leaves',
                          'split_distribution': 'Frequency of splits'}
        # dump the metadata dictionary as a JSON-File
        with open((filename,'_tree_metadata.json', 'w')) as fp:
            js.dump(tree_meta_data, fp)


    def train_random_forest(self, time_regression_df, test_size, random_state, max_depth, export_testset):
        y = time_regression_df["trip_time_in_mins"]
        X = time_regression_df.ix[:, 0:6]
        X_train, X_test, y_train, y_test = cv.train_test_split(X, y, test_size=test_size, random_state=random_state)

        if bool(export_testset) is True:
            Xy_test = pd.concat([X_test, y_test], axis=1)
            Xy_test.to_csv('taxi_forest_test_Xy_20130506-12.csv')

        rd_regtree = RandomForestRegressor(n_estimators=20, n_jobs=6, min_samples_split=3, random_state=random_state, max_depth=max_depth)
        rd_regtree.fit(X_train, y_train)

        # Export Meta-File


def create_tree_dataframe(self, data_in_box):
        # Baum DataFrame:
        time_regression_df = pd.DataFrame([
            self._data['pickup_datetime'].dt.dayofweek,
            self._data['pickup_datetime'].dt.hour,
            self._data['pickup_latitude'],
            self._data['pickup_longitude'],
            self._data['dropoff_latitude'],
            self._data['dropoff_longitude'],
            np.ceil(self._data['trip_time'] / np.timedelta64(1, 'm')),
        ]).T

        time_regression_df.columns = [
            'pickup_datetime_dayofweek', 'pickup_datetime_hour',
            'pickup_latitude', 'pickup_longitude', 'dropoff_latitude', 'dropoff_longitude',
            'trip_time_in_mins']

        return time_regression_df

    def dump_tree(self, decision_model):
        joblib.dump(decision_model , 'treelib/regtree_depth_30_PY27.pkl', protocol=2)

