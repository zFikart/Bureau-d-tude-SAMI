import numpy as np
import matplotlib.pyplot as plt

def generer_random_points(num_points):
    return np.random.rand(num_points, 2)

def calculate_distances(points):
    num_points = len(points)
    dist_matrix = np.zeros((num_points, num_points))
    for i in range(num_points):
        for j in range(num_points):
            if i != j:
                dist_matrix[i][j] = np.sqrt(sum((points[i][k] - points[j][k]) ** 2 for k in range(len(points[i]))))
            else:
                dist_matrix[i][j] = np.inf
    return dist_matrix

def prim_algorithm(dist_matrix):
    num_points = len(dist_matrix)
    in_arbre = [False] * num_points
    min_arete = [np.inf] * num_points
    parent = [-1] * num_points
    min_arete[0] = 0
    arbre_aretes = []

    for _ in range(num_points):
        u = min((i for i in range(num_points) if not in_arbre[i]), key=lambda x: min_arete[x])
        in_arbre[u] = True
        if parent[u] != -1:
            arbre_aretes.append((parent[u], u))
        for v in range(num_points):
            if dist_matrix[u][v] < min_arete[v] and not in_arbre[v]:
                min_arete[v] = dist_matrix[u][v]
                parent[v] = u

    return arbre_aretes

def transforme_arbre_en_cycle(arbre, num_points, start_noeud=0):
    graph = {i: [] for i in range(num_points)}
    for i, j in arbre:
        graph[i].append(j)
        graph[j].append(i)

    visited = []
    stack = [start_noeud]
    while stack:
        noeud = stack.pop()
        if noeud not in visited:
            visited.append(noeud)
            stack.extend([v for v in graph[noeud] if v not in visited])
    visited.append(start_noeud)
    return visited

def two_opt(route, dist_matrix):
    improvement = True
    while improvement:
        improvement = False
        for i in range(1, len(route) - 2):
            for j in range(i + 1, len(route)):
                if j - i == 1: continue
                new_route = route[:i] + route[i:j][::-1] + route[j:]
                if route_cost(new_route, dist_matrix) < route_cost(route, dist_matrix):
                    route = new_route
                    improvement = True
                    break
            if improvement:
                break
    return route

def route_cost(route, dist_matrix):
    return sum(dist_matrix[route[i]][route[i + 1]] for i in range(len(route) - 1))

def plot_graphs(points, route, title):
    plt.figure(figsize=(8, 8))
    plt.title(title)
    for i in range(len(route) - 1):
        plt.plot([points[route[i]][0], points[route[i+1]][0]], [points[route[i]][1], points[route[i+1]][1]], 'ro-')
    plt.scatter(points[:, 0], points[:, 1], color='red')
    plt.show()

# Main process
points = generer_random_points(15)
dist_matrix = calculate_distances(points)
arbre_aretes = prim_algorithm(dist_matrix)
cycle = transforme_arbre_en_cycle(arbre_aretes, 15)

# Plotting initial Hamiltonian cycle
plot_graphs(points, cycle, "Cycle non optimisé")

# Applying 2-opt optimization
optimized_cycle = two_opt(cycle, dist_matrix)

# Plotting optimized Hamiltonian cycle
plot_graphs(points, optimized_cycle, "Cycle optimisé")



