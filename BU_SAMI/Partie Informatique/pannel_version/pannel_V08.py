"""
Filename : pannel_V07.py
Date : Th 23.05.2024

Updates :
self.numRobot = numRobot
self.numPC = numPC
self.update_interval_aff_coord = 1          # en s
self.update_interval_interface_coord = 500  # en ms
self.update_interval_animation = 1000       # en ms
self.create_style_ttk()
...
"""

## Modules
import datetime
from os.path import basename

import tkinter as tk
from tkinter import ttk
##
import sys, os
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'optitrack//src'))

import time

import mocap_node as mcn
import Natnet_Client as nnc
from debug import *

from threading import Thread

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation

from PIL import Image, ImageTk, ImageOps
##

# Adresse IP du robot : 100.75.155.134
import socket
class TCPClient:
    """Gere communication réseau"""
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, host, port):
        print("TCPClient : Connexion")
        self.sock.connect((host, port))

    def send(self, msg):
        self.sock.send(msg.encode())

    def receive(self):
        msg_recu = self.sock.recv(1024)
        print(msg_recu.decode())
        return msg_recu

    def fermer(self):
        print("TCPClient : Fermeture")
        self.sock.close()


class Application(ttk.Frame):
    """Création et gestion de l'interface utilisateur"""
    def __init__(self, *, numPC = 3, numRobot = 3, master = None):
        assert isinstance(numPC, int) and 1 <= numPC <= 7, "Numéro du PC non conforme"
        assert isinstance(numRobot, int) and 1 <= numRobot <= 7, "Numéro du du robot non conforme"
        super().__init__(master)
        self.master = master
        self.numRobot = numRobot
        self.numPC = numPC

        self.initialize_coordinates()
        self.initialize_updates_intervals()

        self.pack()
        self.create_style_ttk()
        self.create_widgets()
        self.event_move_keyboards()
        self.client = TCPClient()

        self.mocap_node = None
        self.initialize_mocap_node()
        self.update_coord()

    def initialize_coordinates(self):
        self.L_all_positions = []
        self.L_all_rotations = []
        self.position_tuple = (0., 0.)           # repere SAMI
        self.rotation_tuple = 0.                 # repere SAMI
        # self.position_tuple = (0., 0., 0.)     # repere Motive
        # self.rotation_tuple = (0., 0., 0., 0.) # repere Motive

    def initialize_updates_intervals(self):
        print("initialise_update_interval() ")
        self.update_interval_aff_coord = 0.1          # en s
        self.update_interval_interface_coord = 500  # en ms
        self.update_interval_animation = 0.1       # en ms
##
    def initialize_mocap_node(self):
        """Création de mocap_node de optitrack"""
        # Création de log dans le fichier ".trace.txt"
        # if os.path.isfile(".trace.txt"):
        #     os.remove(".trace.txt")
        # trace("Coordonnées robot : ")

        srvAddr = "100.64.212.160"
        srvPort  = 1510
        cltAddr = f"100.64.212.15{self.numPC}" # numPC 100.64.212.153
        cltDataPort = 1511
        multcastaddr = "225.1.1.1"
        cltCmdPort = 0
        natnet_client = nnc.NatnetClient(srvAddr, cltAddr, multcastaddr, srvPort, cltDataPort, max_buff_len = 3)
        self.mocap_node = mcn.MocapNode(f"PC{self.numPC}", natnet_client)
        self.mocap_node.run()

##

    def threading_coord(self):
        thread = Thread(target = self.aff_coord)
        thread.start()

    def aff_coord(self):
        if self.mocap_node:
            start = time.time()
            while True:
                # self.position_tuple, self.rotation_tuple = self.mocap_node.getPose(f"Lego{self.numRobot}")
                self.position_tuple, self.rotation_tuple = self.mocap_node.getPos2DAndYaw(f"Lego{self.numRobot}" )
                # print(self.position_tuple)
                # trace(f"\t{self.position_tuple}")
                nb_sec = time.time() - start
                print(f"Temps : {nb_sec:10.7f} ; pos : ({self.position_tuple[0]:.5f}, {self.position_tuple[0]:.5f}) ; rot : {self.rotation_tuple:.8f}")
                # print(f"Temps : {nb_sec:10.7f} ; pos : ({self.position_tuple[0]:.5f}, {self.position_tuple[0]:.5f}) ; rot : {self.rotation_tuple}")
                # print(f"Temps : {nb_sec:10.7f} ; pos : ({self.position_tuple[0]:.5f}, {self.position_tuple[0]:.5f})")

                self.L_all_positions.append(self.position_tuple)
                self.L_all_rotations.append(self.rotation_tuple)
                time.sleep(self.update_interval_aff_coord)


    def update_coord(self):
        self.lab_coord_pos.config(text = f"({self.position_tuple[0]:.5f}, {self.position_tuple[0]:.5f})")
        self.lab_coord_rot.config(text = f"{self.rotation_tuple}")
        self.after(self.update_interval_interface_coord, self.update_coord)

    def update_graph(self, i):
        """Met à jour la position du point sur le graphique."""
        x, y = self.position_tuple
        theta = self.rotation_tuple
        self.point.set_data([x], [y])
        self.ax.set_title(f"Position: ({x:.5f}, {y:.5f})\nTheta : {theta:.8f}")
        # self.ax.set_title(f"Position: ({x:.5f}, {y:.5f})")
        self.canvas.draw()

    def event_move_keyboards(self):
        """Fonctions qui lient les touches au mouvements"""
        def up_keyboard(event):
            """Fonction associée au bouton Up"""
            print("Up")
            vitesseA = self.vitesse_motorA.get()
            vitesseB = self.vitesse_motorB.get()
            msg = f"MOVE {vitesseA} {vitesseB} {2000}"
            # msg = f"MOVE {vitesseA} {vitesseB} {time_deplacement}"
            self.light.itemconfig(self.cercle, fill = "green")
            self.client.send(msg)
            # self.aff_coord()

        def backward_keyboard(event):
            """Fonction associée au bouton Down"""
            print("Down")
            vitesseA = self.vitesse_motorA.get()
            vitesseB = self.vitesse_motorB.get()
            msg = f"BACKWARD {vitesseA} {vitesseB} {2000}"
            # msg = "BACKWARD " + vitesseA + " " + vitesseB
            self.light.itemconfig(self.cercle, fill = "green")
            self.client.send(msg)
            # self.aff_coord()

        def turn_left_keyboard(event):
            """Fonction associée au bouton Left"""
            print("Left")
            vitesseA = self.vitesse_motorA.get()
            msg = f"LEFT {vitesseA} {0} {2000}"
            # msg = "LEFT " + vitesseA
            self.light.itemconfig(self.cercle, fill = "green")
            self.client.send(msg)
            # self.aff_coord()

        def turn_right_keyboard(event):
            """Fonction associée au bouton Right"""
            print("Right")
            vitesseB = self.vitesse_motorB.get()
            msg = f"RIGHT {0} {vitesseB} {2000}"
            # msg = "RIGHT " + vitesseB
            self.light.itemconfig(self.cercle, fill = "green")
            self.client.send(msg)
            # self.aff_coord()

        self.master.bind("<Up>", up_keyboard)
        self.master.bind("<Down>", backward_keyboard)
        self.master.bind("<Left>", turn_left_keyboard)
        self.master.bind("<Right>", turn_right_keyboard)

    def create_style_ttk(self):
        """Création des styles ttk"""
        bg_choisi, fg_choisi = "#B7FFFF", "#080087"
        style = ttk.Style()
        style.theme_use("xpnative")
        style.configure("Custom.TLabel", background = bg_choisi, fg = fg_choisi)
        style.configure("Custom.TButton", background = bg_choisi, fg = fg_choisi)
        style.configure("C.TButton", bg = "red", fg = "green")
        style.configure("Custom.TFrame", background = bg_choisi, fg = fg_choisi)

    def create_widgets(self):
        """Création des widgets tk et ttk"""
        bg_choisi, fg_choisi = "#B7FFFF", "#080087"
        self.master.title("Interface Robot Lego")
        self.master["background"] = bg_choisi
        self["style"]="Custom.TFrame"


        light_frame = ttk.Frame(self, width = 30, style = "Custom.TFrame")
        self.light = tk.Canvas(light_frame, width = 30, height=32, bg = bg_choisi)
        self.light["highlightthickness"] = 0
        x_center, y_center, radius = 15,15, 10
        self.cercle = self.light.create_oval(
            x_center - radius, y_center - radius,  # x0, y0
            x_center + radius, y_center + radius,  # x1, y1
            fill = "white"
        )

        left_frame = tk.Frame(self, bg = "green")

        ##
        self.right_frame = tk.Frame(self, bg = "red")

        self.coordinates = [(0, 0), (1, 2), (2, 3), (3, 5), (4, 7), (5, 8), (6, 6), (7, 4), (8, 3), (9, 1), (10, 0)]
        self.fig = Figure(figsize = (8, 6), dpi = 100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlim(0, 3)
        self.ax.set_ylim(0, 3)
        self.point, = self.ax.plot([], [], 'ro') # BUG

        # Intégration de la figure dans Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master = self.right_frame)
        self.canvas.draw() # equivalent de .pack()
        self.canvas.get_tk_widget().pack(fill = tk.BOTH, expand = True)


        # self.ani = animation.FuncAnimation(self.fig, self.update_graph, frames = 1000, interval = 1000, repeat = False)
        self.ani = animation.FuncAnimation(self.fig, self.update_graph, frames = 10_000_000, \
        interval = self.update_interval_animation, repeat = False)
        ##

        light_frame.pack(side = "left", fill = tk.Y)
        self.light.pack(side = "top")

        left_frame.pack(side = "left", fill = tk.Y)
        tk.Label(left_frame, text = "LEFT").pack(side = "top")

        self.right_frame.pack(side = "right", fill = tk.Y)
        tk.Label(self.right_frame, text = "RIGHT").pack(side = "top")


        # Première ligne : connexion
        rowConnect = ttk.Frame(left_frame ,style = "Custom.TFrame")
        self.connect = ttk.Button(rowConnect, text = "Connect", style="Custom.TButton")
        self.connect["command"] = self.connect_robot
        self.disconnect = ttk.Button(rowConnect, text = "Disconnect", style="Custom.TButton")
        self.disconnect["command"] = self.disconnect_robot
        self.robot = tk.Entry(rowConnect)

        rowConnect.pack(side = "top", fill = tk.X, padx = 5, pady = 5)
        self.connect.pack(side = "left")
        self.disconnect.pack(side = "left")
        self.robot.pack(side = "left", expand = tk.YES, fill = tk.X)


        # Deuxième ligne : motor gauche
        rowA = ttk.Frame(left_frame, style = "Custom.TFrame")
        lab_motorA = ttk.Label(rowA,text = "Vitesse moteur gauche", anchor = 'w', style = "Custom.TLabel")
        self.vitesse_motorA = tk.Entry(rowA)

        rowA.pack(side = "top",fill = tk.X, padx = 5, pady = 5)
        lab_motorA.pack(side = "left")
        self.vitesse_motorA.pack(side = "right", expand = tk.YES, fill = tk.X)


        # Troisième ligne : motor droit
        rowB = ttk.Frame(left_frame, style = "Custom.TFrame")
        lab_motorB = ttk.Label(rowB,text = "Vitesse moteur droit",anchor='w', style = "Custom.TLabel")
        self.vitesse_motorB = tk.Entry(rowB)

        rowB.pack(side= "top",fill = tk.X, padx = 5, pady = 5)
        lab_motorB.pack(side = "left")
        self.vitesse_motorB.pack(side = "right", expand = tk.YES, fill = tk.X)


        # Quatrième ligne : temps de déplacement
        rowTime = ttk.Frame(left_frame, style = "Custom.TFrame")
        time_move = ttk.Label(rowTime, text = "Temps (s)",anchor='w', style = "Custom.TLabel")
        self.time_entry_robot = tk.Entry(rowTime)

        rowTime.pack(side = "top",fill = tk.X, padx= 5, pady = 5)
        time_move.pack(side = "left")
        self.time_entry_robot.pack(side = "right", expand = tk.YES, fill = tk.X)


        # Cinquième ligne : Boutons menu
        rowMenu = ttk.Frame(left_frame, style = "Custom.TFrame")
        self.move = ttk.Button(rowMenu, text = "MOVE",style = "Custom.TButton")
        self.move["command"] = self.move_robot
        self.backward = ttk.Button(rowMenu, text = "BACKWARD", style = "Custom.TButton")
        self.backward["command"] = self.backward_robot
        self.stop = ttk.Button(rowMenu, text = "STOP",style = "Custom.TButton")
        self.stop["command"] = self.stop_robot
        keyboard_indic = ttk.Label(rowMenu, text = "Utilisez les flèches du clavier pour contrôler le robot", style = "Custom.TLabel")
        self.quit = ttk.Button(rowMenu, text = "QUIT", style = "Custom.TButton")
        self.quit["command"] = self.quitter

        rowMenu.pack(side = "top", fill = tk.X, padx = 5, pady = 5)
        self.move.pack(side = "left")
        self.backward.pack(side = "left")
        self.stop.pack(side = "left")
        keyboard_indic.pack(side = "left")
        self.quit.pack(side = "right")


        # Sixième ligne : Position
        position_frame = ttk.Frame(left_frame,style = "Custom.TFrame")
        coord_button_while = ttk.Button(position_frame, text = "Cliquez une seule fois afficher les coordonnées", style = "Custom.TButton")
        coord_button_while["command"] = self.threading_coord

        coord_button_unique = ttk.Button(position_frame, text = "Coord enregistrées", style = "Custom.TButton")
        coord_button_unique["command"] = self.threading_coord

        self.lab_coord_pos = ttk.Label(position_frame, text = str(self.position_tuple), style = "Custom.TLabel")
        self.lab_coord_rot = ttk.Label(position_frame, text = str(self.rotation_tuple), style = "Custom.TLabel")

        position_frame.pack(side = "top",fill = tk.X, padx = 5, pady = 5)
        coord_button_while.pack(side = "left")
        coord_button_unique.pack(side = "right")
        self.lab_coord_pos.pack(side = "top")
        self.lab_coord_rot.pack(side = "top")


        # Dernière ligne : Titre Samijote
        rowTitle = ttk.Frame(left_frame, style = "Custom.TFrame")
        lab_title = ttk.Label(rowTitle, text = "Samijote", font = ("Bauhaus 93", 25), style = "Custom.TLabel") # fg = "#080087"
        rowTitle.pack(side = "bottom", fill = tk.X, padx = 5, pady = 5)
        lab_title.pack(side = "left")



    def connect_robot(self) -> None:
        """Fonction associée au bouton Connect"""
        robot_addr = self.robot.get()
        print("Le robot s'est bien connecté au serveur !")
        print("L'adresse IP est :", robot_addr)
        self.light.itemconfig(self.cercle, fill = "blue")
        self.client.connect(robot_addr, 9999)

    def disconnect_robot(self) -> None:
        """Fonction associée au bouton Disconnect"""
        print("Fermeture de la connexion")
        self.light.itemconfig(self.cercle, fill = "white")
        self.client.fermer()

    def get_vitesse_time_deplacement(self) -> tuple:
        vitesseA = self.vitesse_motorA.get()
        vitesseB = self.vitesse_motorB.get()
        time_deplacement = self.time_entry_robot.get()
        return vitesseA, vitesseB, time_deplacement

    def move_robot(self) -> None:
        """Fonction associée au bouton Move"""
        print("MOVE pannel")
        vitesseA, vitesseB, time_deplacement = self.get_vitesse_time_deplacement()
        msg = f"MOVE {vitesseA} {vitesseB} {time_deplacement}"
        # msg = "MOVE " + str(1000) + " " + str(1000) + " " + str(5)
        self.light.itemconfig(self.cercle, fill = "green")
        self.client.send(msg)
        # self.aff_coord()

    def backward_robot(self) -> None:
        """Fonction associée au bouton Move"""
        print("BACKWARD pannel")
        vitesseA, vitesseB, time_deplacement = self.get_vitesse_time_deplacement()
        # msg = "BACKWARD " + vitesseA + " " + vitesseB + " " + time_deplacement
        msg = f"BACKWARD {vitesseA} {vitesseB} {time_deplacement}"
        self.light.itemconfig(self.cercle, fill = "green")
        self.client.send(msg)
        # self.aff_coord()

    def stop_robot(self) -> None:
        """Fonction associée au bouton STOP"""
        msg = "STOP"
        print("Le robot se stop.")
        self.light.itemconfig(self.cercle, fill = "red")
        self.client.send(msg)
        # self.aff_coord()

    def quitter(self) -> None:
        """Fonction associée au bouton QUIT"""
        print("Fermeture de l'application")
        self.mocap_node.stop()
        self.client.fermer()
        self.master.destroy()


if __name__ == "__main__":
    # Programme principale
    print("Filename :", basename(__file__))
    print(f"Date : {datetime.date.today().strftime('%A')[:2]} {datetime.date.today().strftime('%d.%m.20%y')}\n")

    root = tk.Tk()
    app = Application(master = root,  numPC = 3, numRobot = 4)
    app.mainloop()





