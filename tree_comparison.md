Comparison of Regression Trees with different depth
===================================================

#### remember: 2^22 = 4.2E6, i.e. every trip can have it's own leaf (3.25 mio. trips in week 1)!

-	regtree = DecisionTreeRegressor(min_samples_split=20, random_state=99, max_depth=20)

np.percentile(avg_time_dev, q=[5, 50, 75, 90, 95, 97.5, 99]):

array([ 1. , 7.69 , 16.71223452, 37.25502113, 65.48671875, 111.26921296, 216.0168595 ])

-	regtree = DecisionTreeRegressor(min_samples_split=20, random_state=99, max_depth=25)

np.percentile(avg_time_dev, q=[5, 50, 75, 90, 95, 97.5, 99])

array([ 0.59555556, 4.66130178, 10.62809917, 24.62774464, 42.88888889, 72.6875 , 142.17595 ])

-	regtree = DecisionTreeRegressor(min_samples_split=20, random_state=99, max_depth=35)

array([ 0.25 , 2.87109375, 6.75 , 16.16 , 29.63724747, 50.66666667, 100.26999473])

-	regtree = DecisionTreeRegressor(min_samples_split=20, random_state=99, max_depth=50)

array([ 0.25 , 2.359375 , 5.88888889, 14.24 , 25.84 , 45.40484429, 90.25 ])

elapsed = 104sek.

-	regtree = DecisionTreeRegressor(min_samples_split=20, random_state=99, max_depth=75)

array([ 0.25 , 2.35416667, 5.87654321, 14.23268698, 25.83481194, 45.36058333, 90.25 ])

elapsed = 104sek

-	regtree = DecisionTreeRegressor(min_samples_split=20, random_state=99, max_depth=100) -> same as depth = 75

-	regtree = DecisionTreeRegressor(min_samples_split=5, random_state=99, max_depth=100) [remember: 2^100 = 1.26E30]

array([ 0.1875, 0.25 , 1.25 , 4. , 8.6875, 17.25 , 42.25 ])

elapsed = 278.8402895927429
