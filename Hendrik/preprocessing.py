import pandas as pd
import numpy as np

class cleaner:

    def __init__(self):
        self._data = pd.DataFrame()

    def week_import(self, dataRoot_import):
        self._data = pd.read_csv(dataRoot_import)
        self._data['pickup_datetime'] = pd.to_datetime(self._data['pickup_datetime'], format = '%Y-%m-%d %H:%M:%S')
        self._data['dropoff_datetime'] = pd.to_datetime(self._data['dropoff_datetime'], format ='%Y-%m-%d %H:%M:%S')
        return self._data

    def slice_data(self, dataRoot_data, dataRoot_week, start_date, end_date):
        self._data = pd.read_csv(dataRoot_data)
        self._data['pickup_datetime'] = pd.to_datetime(self._data['pickup_datetime'], format='%Y-%m-%d %H:%M:%S')
        self._data['dropoff_datetime'] = pd.to_datetime(self._data['dropoff_datetime'], format='%Y-%m-%d %H:%M:%S')
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        mask = (self._data['pickup_datetime'] >= start_date) & (self._data['pickup_datetime'] < end_date)

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

    def drop_zero_data(self, list_need):
        self._data = self._data.replace(np.float64(0), np.nan)
        self._data.dropna(axis=0, inplace=True)
        anomaly = self._data.loc[(self._data['dropoff_longitude'].isnull()) | (self._data['dropoff_latitude'].isnull()) | (self._data['pickup_longitude'].isnull()) | (self._data['pickup_latitude'].isnull())]
        #anomaly = [self._data for x in list_need if self._data[x].isnull]
        self._data = self._data.drop(anomaly.index)
        return self._data