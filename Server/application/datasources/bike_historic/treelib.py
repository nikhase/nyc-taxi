# Use SKlearn 0.17 Lib for proper import
import pandas
from sklearn.externals import joblib
import numpy
from sklearn.tree import DecisionTreeRegressor

global regtree

# regtree = joblib.load('/Users/larshelin/Documents/PycharmProjects/CEP/nyc-taxi/Server/application/datasources/bike_historic/treelib/bike_regtree_depth_10_PY27.pkl')
regtree = joblib.load('./application/datasources/bike_historic/treelib/bike_regtree_26x_depth_26_mss_2_PY27.pkl')
def getEstimatedTime(X):
    y_pred = regtree.predict(X)
    return y_pred

