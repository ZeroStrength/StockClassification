from sklearn.cluster import KMeans
import numpy as np

# Documentation from
# https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html


# Get array data
X = np.array([[1, 2], [1, 4], [1, 0],
               [10, 2], [10, 4], [10, 0]])

kmeans = KMeans(n_clusters=8, random_state=0, verbose=1).fit(X)


print( kmeans.labels_ )

print( kmeans.predict([[0, 0], [12, 3]]) )

print( kmeans.cluster_centers_ )


