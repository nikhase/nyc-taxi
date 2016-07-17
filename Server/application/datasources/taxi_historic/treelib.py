# Use SKlearn 0.17 Lib for proper import
import pandas
from sklearn.externals import joblib
import numpy
from sklearn.tree import DecisionTreeRegressor

global regtree

# regtree = joblib.load('/Users/larshelin/Documents/PycharmProjects/CEP/nyc-taxi/Server/application/datasources/taxi_historic/treelib/regtree_depth_30_PY27.pkl')
regtree = joblib.load('./application/datasources/taxi_historic/treelib/regtree_depth_25_mss_50_rs_10.pkl')
def getEstimatedTime(X):
    y_pred = regtree.predict(X)
    return y_pred

