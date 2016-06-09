# Use SKlearn 0.17 Lib for proper import
import pandas
from sklearn.externals import joblib
import numpy as np
from sklearn.tree import DecisionTreeRegressor

global regtree

def treeImport():
    regtree = joblib.load('treelib/regtree_depth_10.pkl')
    return regtree

def getEstimatedTime(X):
    y_pred = regtree.predict(X)
    return y_pred
