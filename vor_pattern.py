import numpy as np
from scipy.spatial import Voronoi
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, LineString, Point

num_points = 100 
padding = 0.2
points = np.random.uniform(-padding, 1 + padding, size=(num_points, 2))

vor = Voronoi(points)

boundary_coords = [(0,0), (1,0), (1,1), (0,1)]
boundary = Polygon(boundary_coords)

boundary_points = np.array(boundary_coords)
points = np.vstack([points, boundary_points])

fig, ax = plt.subplots()

boundary_coords_array = np.array(boundary.exterior.coords)
ax.plot(boundary_coords_array[:, 0], boundary_coords_array[:, 1], 'k--', label="Boundary")

for simplex in vor.ridge_vertices:
    simplex = np.asarray(simplex)
    if np.any(simplex < 0):
        continue
    line = LineString([vor.vertices[simplex[0]], vor.vertices[simplex[1]]])
    clipped_line = line.intersection(boundary)
    if not clipped_line.is_empty:
        x, y = clipped_line.xy
        ax.plot(x, y, 'b-')

for vertex in vor.vertices:
    if boundary.contains(Point(vertex)):
        ax.plot(vertex[0], vertex[1], 'go', markersize=3)

ax.plot(points[:, 0], points[:, 1], 'ro', markersize=5, label="Points")

plt.title("Voronoi Tessellation")
plt.legend()
plt.show()

