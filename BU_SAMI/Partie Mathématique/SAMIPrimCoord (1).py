import numpy as np
import matplotlib.pyplot as plt

background_image_path='Map.png'

def generer_random_points(num_points):
    # Générer des points aléatoires dans un espace 2D
    return np.random.rand(num_points, 2)

def calcule_distances(points):
    # Calculer la matrice des distances entre les points
    num_points = len(points)
    dist_matrix = np.zeros((num_points, num_points))
    for i in range(num_points):
        for j in range(num_points):
            if i != j:
                dist_matrix[i][j] = np.sqrt(sum((points[i][k] - points[j][k]) ** 2 for k in range(len(points[i]))))
            else:
                # distance infini
                dist_matrix[i][j] = np.inf
    return dist_matrix

def prim_algorithm(dist_matrix):
    # Implémenter l'algorithme de Prim pour obtenir l'Arbre Couvrant Minimal
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
    # Convertir l'arbre couvrant minimal en cycle hamiltonien en utilisant le parcours en profondeur pour obtenir un ordre de visite
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

def plot_graphs(points, arbre_aretes, cycle):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

    # Tracer l'Arbre couvrant minimal
    ax1.set_title('Arbre Couvrant Minimal')
    for i, j in arbre_aretes:
        ax1.plot([points[i][0], points[j][0]], [points[i][1], points[j][1]], 'bo-')
    ax1.scatter(points[:, 0], points[:, 1], color='blue')

    # Tracer le cycle hamiltonien
    ax2.set_title('Cycle Hamiltonien')
    for i in range(len(cycle) - 1):
        ax2.plot([points[cycle[i]][0], points[cycle[i+1]][0]],
                [points[cycle[i]][1], points[cycle[i+1]][1]], 'ro-')
    ax2.scatter(points[:, 0], points[:, 1], color='red')

    plt.show()

# Processus principal
points = generer_random_points(15)
dist_matrix = calcule_distances(points)
arbre_aretes = prim_algorithm(dist_matrix)
cycle = transforme_arbre_en_cycle(arbre_aretes, 15)
plot_graphs(points, arbre_aretes, cycle)

# Extraction des points ordonnés selon le cycle hamiltonien
ordered_points = points[cycle[:-1]]  # Ignore le dernier point car il est répété pour fermer le cycle

# Afficher ou retourner les points ordonnées
print("Points ordonnés selon le chemin hamiltonien:")
print(ordered_points)