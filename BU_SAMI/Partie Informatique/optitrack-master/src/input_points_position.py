"""
Filename : input_points_position
Date : Di 19.05.2024
"""

def main() -> list:
    # filename = input("Nom du fichier :")
    L_pos = []
    number_points = 0

    filename = "parcours_SAMI_17.txt"
    file = open(filename, mode = 'r', encoding = "UTF-8")
    line:str = file.readline()

    print(" Début du traitement des positions des points ".center(60, '='))
    print(f"Nom du fichier : {filename}\n")
    while line:
        processed_line = tuple(map(float, line.strip().split("\t")))
        L_pos.append(processed_line)
        number_points +=1
        # print(processed_line)
        # print()
        line = file.readline()

    file.close()
    print(f"Il y a : {number_points} point(s).")
    print(f"Liste des positions des points :\n{L_pos}")
    print(" Fin du traitement des positions des points ".center(60, '='))
    return L_pos


if __name__ == "__main__":
    L_pos = main()