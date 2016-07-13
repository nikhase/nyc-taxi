from sklearn.externals import joblib
import numpy as np
from sklearn.tree import DecisionTreeRegressor

def treeImport():
    regtree = joblib.load('treelib/regtree_depth_10.pkl')
    return regtree

def getEstimatedTime(X):
    regtree = treeImport()
    y_pred = regtree.predict(X)
    return y_pred


treeImport()