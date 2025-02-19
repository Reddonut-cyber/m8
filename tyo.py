import numpy as np
import matplotlib.pyplot as plt

def trilateration(anchors, distances):
    n = len(anchors)
    if n < 3:
        raise ValueError("At least three anchors are needed for 2D trilateration.")
    
    x1, y1 = anchors[0]  # Reference anchor
    A = []
    b = []
    
    for i in range(1, n):
        xi, yi = anchors[i]
        A.append([x1 - xi, y1 - yi])
        b.append(0.5 * (distances[0]**2 - distances[i]**2 + xi**2 - x1**2 + yi**2 - y1**2))
    
    A = np.array(A)
    b = np.array(b)
    
    # Solve using least squares
    pos_estimate, _, _, _ = np.linalg.lstsq(A, b, rcond=None)
    return pos_estimate

def refine_position(anchors, distances, estimated_position, iterations=5):
    """Refine position iteratively by minimizing error without scipy."""
    x, y = estimated_position
    for _ in range(iterations):
        errors = np.linalg.norm(anchors - np.array([x, y]), axis=1) - distances
        grad_x = np.sum(2 * (np.linalg.norm(anchors - np.array([x, y]), axis=1) - distances) * (x - anchors[:, 0]))
        grad_y = np.sum(2 * (np.linalg.norm(anchors - np.array([x, y]), axis=1) - distances) * (y - anchors[:, 1]))
        x -= 0.01 * grad_x  # Small learning rate
        y -= 0.01 * grad_y
    return np.array([x, y])

# Define anchor points
anchors = np.array([[0, 0], [5, 0], [5, 5], [0, 5]])

# Define the true position
true_position = np.array([2, 2])

# Compute distances from true position to each anchor
distances = np.linalg.norm(anchors - true_position, axis=1)

# Estimate position
initial_estimate = trilateration(anchors, distances)
refined_estimate = refine_position(anchors, distances, initial_estimate)

print(f"True Position: {true_position}")
print(f"Initial Estimated Position: {initial_estimate}")
print(f"Refined Estimated Position: {refined_estimate}")

# Plot the result
plt.scatter(anchors[:, 0], anchors[:, 1], c='red', marker='o', label='Anchors')
plt.scatter(true_position[0], true_position[1], c='green', marker='x', label='True Position')
plt.scatter(refined_estimate[0], refined_estimate[1], c='blue', marker='s', label='Refined Position')
plt.legend()
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.title("2D Trilateration with Iterative Refinement")
plt.grid(True)
plt.show()
