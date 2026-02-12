from matplotlib import pyplot as plt
from random import randint
from math import atan2, sqrt

def create_points(nbr, min=0, max=50):
    """Génère une liste de 'nbr' points (x, y) avec des valeurs entre 'min' et 'max'."""
    return [[randint(min, max), randint(min, max)] for _ in range(nbr)]

def scatter_plot(coords, env_convex=None):
    """Affiche les points et, si donné, les connecte dans l'ordre de 'env_convex'."""
    xs, ys = zip(*coords)
    plt.scatter(xs, ys)
    if env_convex is not None:
        # Relier les points pour former l'enveloppe convexe
        for i in range(1, len(env_convex) + 1):
            if i == len(env_convex):
                i = 0
            c0, c1 = env_convex[i-1], env_convex[i]
            plt.plot((c0[0], c1[0]), (c0[1], c1[1]), 'r')
    plt.show()

def angle_polaire(p0, p1=None, anchor=None):
    """Calcule l'angle polaire entre deux points, ou entre un point et un point d'ancrage."""
    if p1 is None:
        p1 = anchor
    a = p0[0] - p1[0]
    b = p0[1] - p1[1]
    return atan2(b, a)

def distance(p0, p1=None, anchor=None):
    """Calcule la distance au carré entre deux points ou entre un point et un point d'ancrage."""
    if p1 is None:
        p1 = anchor
    a = p0[0] - p1[0]
    b = p0[1] - p1[1]
    return b**2 + a**2

def det(p1, p2, p3):
    """Calcule le déterminant de trois points pour déterminer leur orientation relative."""
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])

def tri(coords, anchor):
    """Trie les points d'abord par angle polaire puis par distance par rapport à un point d'ancrage."""
    if len(coords) <= 1:
        return coords
    moins, egal, plus = [], [], []
    pivot = coords[randint(0, len(coords) - 1)]
    pivot_angle = angle_polaire(pivot, anchor=anchor)

    for pt in coords:
        pt_angle = angle_polaire(pt, anchor=anchor)
        if pt_angle < pivot_angle:
            moins.append(pt)
        elif pt_angle == pivot_angle:
            egal.append(pt)
        else:
            plus.append(pt)

    # Tri récursif des moins et plus, tri des égaux par distance
    moins = tri(moins, anchor)
    egal = sorted(egal, key=lambda x: distance(x, anchor))
    plus = tri(plus, anchor)
    return moins + egal + plus

def graham_scan(points, show_progress=False):
    """Exécute le balayage de Graham pour trouver l'enveloppe convexe des points donnés."""
    global anchor  # point avec la plus petite valeur y (en cas d'égalité, le plus petit x)
    min_idx = min(range(len(points)), key=lambda i: (points[i][1], points[i][0]))
    anchor = points[min_idx]

    # Tri des points par angle polaire et suppression de l'ancre
    sorted_points = tri(points, anchor)
    sorted_points.remove(anchor)

    # L'ancre et le point avec l'angle polaire le plus petit sont toujours dans l'enveloppe
    hull = [anchor, sorted_points[0]]
    for s in sorted_points[1:]:
        while len(hull) > 1 and det(hull[-2], hull[-1], s) <= 0:
            hull.pop()  # Retirer le dernier point si on tourne à droite
        hull.append(s)
        if show_progress:
            scatter_plot(points, hull)
    return hull

def insertion_optimisee(pts):
    """Insère les points restants dans l'enveloppe pour optimiser la forme globale."""
    hull = graham_scan(pts)
    scatter_plot(pts, hull)
    reste = [pt for pt in pts if pt not in hull]

    for point in reste:
        best_idx = 0
        best_increase = float('inf')
        for i in range(len(hull)):
            next_idx = (i + 1) % len(hull)
            increase = (distance(hull[i], point) + distance(point, hull[next_idx])
                        - distance(hull[i], hull[next_idx]))
            if increase < best_increase:
                best_idx, best_increase = i, increase
        hull.insert(best_idx + 1, point)
        scatter_plot(pts, hull)

    return hull



pts = create_points(15)
final_hull = insertion_optimisee(pts)
print("Points de l'enveloppe convexe finale :", final_hull)