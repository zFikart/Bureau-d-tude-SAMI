"""
Filename : input_points_position
Date : Sa 25.05.2024
"""

from os.path import basename
from time import perf_counter
import matplotlib.pyplot as plt


def input_points_position(file_path:str, *, space = 60) -> list:
    assert isinstance(file_path, str), "filename_path must be a str."
    assert isinstance(space, int), "space must be a int."
    Pos = []

    print(f"{'Début du traitement ':-<{space}}")
    try:
        with open(file_path, mode = 'r', encoding = "UTF-8") as file:
            line:str = file.readline()
            print(f"Nom du fichier : {basename(file_path)}\n")
            for line in file:
                processed_line = tuple(map(float, line.strip().split("\t")))
                Pos.append(processed_line)
                # print(processed_line)

    except (FileNotFoundError, IsADirectoryError, PermissionError): raise
    else:
        print(f"Il y a : {len(Pos)} point(s).")
        print(f"Liste des positions des points :\n{Pos}\n")
        print(f"{'Traitement réussi ':-<{space}}")
    finally: print(f"{f'Fin du traitement des positions des points ':-<{space}}")
    return Pos


def processing_straight_line(line:str) -> tuple:
    """Temps :  1.1895554 ; pos : (0.21986, 0.21986) ; rot : 0.01399526"""
    assert isinstance(line, str), "line must be str."
    # line = "Temps :  1.1895554 ; pos : (0.21986, 0.21986) ; rot : 0.01399526"
    # print(line, end = '')
    try:
        time_str, pos_str, rot_str = map(lambda elem : elem.split(" : ")[1], line.split(" ; "))
        pos = tuple(map(lambda z: float(z)*10, pos_str[1:-1].split(", ")))
        time, rot = float(time_str.strip()), float(rot_str)
        return time, pos, rot
    except (ValueError, IndexError): raise


def open_file_straight_line_robot(file_path:str, *, mode = 'r', space = 70) -> tuple:
    assert isinstance(file_path, str), "file_path must be a str"
    assert isinstance(mode, str), "mode must be a str"
    Time, Pos, Rot = [], [], []
    starting_point, starting_point_0 = False, True
    time0, pos0, rot0 = 0., (0., 0.), 0.

    start_time_processing = perf_counter()
    print(f"{'Début du traitement ':-<{space}}")
    try:
        with open(file_path, mode, encoding = "UTF-8") as file:
            print(f"Nom du fichier : {basename(file_path)}\n")
            for line in file:
                if "stop" in line or "STOP" in line:
                    print("Fermeture du fichier")
                    break
                elif line.startswith(("MOVE", "BACKWARD", "LEFT", "RIGHT")):
                    starting_point = True

                elif line.startswith("Temps") and starting_point:
                    time, pos, rot = processing_straight_line(line)
                    if starting_point_0: # in because True is the default value
                        time0, pos0, rot0 = time, pos, rot
                        starting_point_0 = False # if condition will never be execute
                    Time.append(time - time0)
                    Pos.append(tuple(posj - pos0j for posj, pos0j in zip(pos, pos0)))
                    Rot.append(rot - rot0)


    except (FileNotFoundError, IsADirectoryError, PermissionError): raise
    else:
        print(f"\nIl y a : {len(Pos)} point(s).")
        # print(f"Liste des positions des points :\n{Pos}\n")
        print(f"{'Traitement réussi ':-<{space}}")
    finally:
        print(f"{f'Fin du traitement {perf_counter() - start_time_processing: .6f}s ':-<{space}}")
        return Time, Pos, Rot


def graph_straight_line(Time:list, *Args:tuple) -> None:
    assert isinstance(Time,list), "Time must be a list"
    assert isinstance(Args,tuple), "Time must be a list"
    n = len(Args)
    yLabel = ["x (cm)", "y (cm)", "$\Theta$"] + [""]*(n-3)
    Marker = ["bo-", "rd-", "g*-"] + [""]*(n-3)

    import tkinter as tk
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight() - 200
    root.destroy()

    fig = plt.figure(figsize = [screen_width / 100, screen_height / 100], dpi = 100)
    # fig = plt.figure(figsize = [14.80, 9.40])
    Axes = fig.subplots(n, 1, sharex = True)
    for i in range(n):
        Axes[i].plot(Time, Args[i], Marker[i])
        Axes[i].axhline(max(Args[i]), label = f"max : {max(Args[i]):.3f}", c = "orange", ls = ":", lw = 3)
        Axes[i].set_ylabel(yLabel[i], fontsize = 18, labelpad = 20)
        Axes[i].tick_params(labelsize = 15)
        Axes[i].grid()
        if i!= 2:
            Axes[i].set_ylim(-0.5,3)
        # Axes[i].legend()
    Axes[-1].set_xlabel("Temps (s)", fontsize = 20, labelpad = 20)
    fig.suptitle("Coordonnées du robot Lego", fontsize = 22)
    fig.legend(loc = "upper right", fontsize = 18)
    fig.show()
    print("Le graphe s'affiche.")


def main() -> list:
    file_path = "parcours_SAMI_17.txt"
    # input_points_position(file_path)
    file_straight_line = r"D:\Documents\Travail\S6\UE_BE_Bureau_detude\straight_line_robot.txt"
    Time, Pos, Rot = open_file_straight_line_robot(file_straight_line)
    PosX, PosY = list(map(list, zip(*Pos)))
    graph_straight_line(Time, PosX, PosY, Rot)



if __name__ == "__main__":
    main()


