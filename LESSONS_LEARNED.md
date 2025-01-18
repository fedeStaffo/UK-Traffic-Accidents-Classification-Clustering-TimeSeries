# Clustering Analysis
## Why does Voronoi plotting seem quite odd?
### Problem
We know that Voronoi lines are drawn as the intersection of axes between each pair of points, that is the k-means centroids. However, if you take a quick look at the images in the [clustering_uk_roads_accidents](/dataset/clustering_uk_roads_accidents.ipynb) notebook, the dashed lines aren't orthogonal to the centroids.


### Solution
That's due to the distorsion of the plot given by two factors:
1. The shape of the figure, which is not a square,
2. The scales of the axes are not uniform.

> More on: [Voronoi Tesselation Issue in Python](https://stackoverflow.com/a/66092805/19815002)

## Why does k-means allow some points to have a negative silhouette score?

### Problem
Silhouette is typically used with density-based algorithms because prototype-based algorithms, such as k-means, cannot misclassify a point in silhouette terms because the Euclidean distance to its centroid is minimized.

### Solution
That's not true at all! There's a subtle difference between the silhouette and the k-means approach: 
- `Silhouette` considers the average distance to points in the same cluster,
- `K-mean` considers the distance to the center of the cluster, namely the centroid,

It is therefore quite possible for some points to cause disagreement between the k-means and the silhouette score.

> More on: [How can silhouette scores be negative?](https://stackoverflow.com/a/66751204/19815002)