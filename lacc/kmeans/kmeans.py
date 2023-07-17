# Import the nessecary libraries
import random
import numpy as np
from numpy.random import uniform
import matplotlib.pyplot as plt

def plot_clusters(data, labels, num_clusters, cluster_centers):
  listOfClusterColors = ['blue', 'green', 'magenta', 'brown', 'orange']

  for i in range(num_clusters):
    currentClusterColor = listOfClusterColors[i % len(listOfClusterColors)]
    x1 = []; y1 = []

    # Loop through the dataset
    for j in range(len(data)):
      # Assign the data to the cluster color if its label is in the cluster
      if labels[j] == i:
        x1.append(data[j, 0])
        y1.append(data[j, 1])

    # Plot the data in the cluster
    plt.scatter(x1, y1, c=currentClusterColor)
    plt.scatter([x for x, _ in cluster_centers], [y for _, y in cluster_centers], marker='+', c='black', s=200)


def plot_test_point(X, centers):
  random_point = [random.uniform(min(X[:, 0]), max(X[:, 0])),
                  random.uniform(min(X[:, 1]), max(X[:, 1]))]

  distances = [sum((x - center) ** 2 for x, center in zip(random_point, centers)) ** 0.5 for centers in centers]
  index_of_min_dist = distances.index(min(distances))
  best_centroid = centers[index_of_min_dist]

  plt.scatter(random_point[0], random_point[1], marker='*', color='red', s=200)
  plt.plot([random_point[0], best_centroid[0]], [random_point[1], best_centroid[1]], 'b-')

class KMeans_KEY:
    def __init__(self, n_clusters=3, max_iter=100):
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.centroids = None
        self.labels = None

    def fit(self, X):
        # Initialize centroids randomly
        np.random.seed(42)
        random_indices = np.random.choice(X.shape[0], self.n_clusters, replace=False)
        self.centroids = X[random_indices]

        for _ in range(self.max_iter):
            # Assign each data point to the nearest centroid
            distances = self.calculate_distances(X)
            self.labels = np.argmin(distances, axis=1)

            # Update the centroids
            old_centroids = self.centroids.copy()
            for i in range(self.n_clusters):
                cluster_points = X[self.labels == i]
                if cluster_points.shape[0] > 0:
                    self.centroids[i] = cluster_points.mean(axis=0)

            # Check for convergence
            if np.allclose(old_centroids, self.centroids):
                break

    def calculate_distances(self, X):
        distances = np.zeros((X.shape[0], self.n_clusters))
        for i, centroid in enumerate(self.centroids):
            distances[:, i] = np.linalg.norm(X - centroid, axis=1)
        return distances
    

class KMeans:
  def __init__(self, n_clusters=3, max_iter=100):
    self.n_clusters = n_clusters
    self.max_iter = max_iter
    self.centroids = None
    self.labels = None

    self.fit_function = None

  def set_fit_function(self, code):
    self.fit_function = code

  def set_centriods(self, centroids):
    self.centroids = centroids

  def set_lables(self, labels):
    self.labels = labels

  def fit(self, X):
    return(self.fit_function(X))