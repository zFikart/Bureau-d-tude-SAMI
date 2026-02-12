import datetime

## Modules
import tkinter as tk
from tkinter import ttk
##
from PIL import Image, ImageTk

import sys, os
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'optitrack//src'))

import time

import mocap_node as mcn
import Natnet_Client as nnc
from debug import *
from common import euler_from_quaternion
from time import sleep

from threading import Thread

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
##

# Adresse IP du robot : 100.75.155.133
import socket
class TCPClient:
    """Gere communication réseau"""
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, host, port):
        self.sock.connect((host, port))

    def send(self, msg):
        self.sock.send(msg.encode())

    def receive(self):
        msg_recu = self.sock.recv(1024)
        print(msg_recu.decode())
        return msg_recu

    def fermer(self):
        self.sock.close()


class Application(ttk.Frame):
    """Création et gestion de l'interface utilisateur"""
    def __init__(self, master = None):
        super().__init__(master)
        self.master = master
        self.L_pos = []
        self.L_rot = []
        # self.position_tuple = (0., 0., 0.)
        # self.rotation_tuple = (0., 0., 0., 0.)
        self.position_tuple = [0., 0.]
        self.rotation_tuple = []

        self.pack()
        self.create_widgets()       # methode creee
        self.move_keyboards()
        self.client = TCPClient()   # objet de classe

        self.update_interval = 500  # updating coordinates in ms
        self.mocap_node = None
        self.load_mocap_node()
        self.update_coord()
        # self.etat_aff_coord = 0 # gere aff_coord


##
    def load_mocap_node(self):
        # if os.path.isfile(".trace.txt"):
        #     os.remove(".trace.txt")
        # trace("Coordonnées robot : ")

        # Configure fake server
        srvAddr = "100.64.212.160"
        srvPort  = 1510
        numPC = 3
        cltAddr = "100.64.212.15" + str(numPC) # numPC 100.64.212.153
        cltDataPort = 1511
        multcastaddr = "225.1.1.1"
        cltCmdPort = 0
        natnet_client = nnc.NatnetClient(srvAddr,cltAddr,multcastaddr,srvPort,cltDataPort)

        # Generate a MocapNode
        self.mocap_node = mcn.MocapNode("PC" + str(numPC),natnet_client)
        self.mocap_node.run()

##

    def threading_coord(self):
        thread = Thread(target = self.aff_coord)
        thread.start()
        # self.etat_aff_coord += 1

    def aff_coord(self, time_aff = 0.1):
        if self.mocap_node:
            # print("etat : ", self.etat_aff_coord)
            # if (self.etat_aff_coord % 2 == 0):
            start = time.time()
            while True:
                # self.position_tuple, self.rotation_tuple = self.mocap_node.getPose("Lego3")
                self.position_tuple, self.rotation_tuple = self.mocap_node.getPos2DAndYaw("Lego3")
                # print(self.position_tuple)
                # trace(f"\t{self.position_tuple}")
                nb_sec = time.time() - start
                print(f"Temps : {nb_sec} ; pos : {self.position_tuple}")

                self.L_pos.append(self.position_tuple)
                self.L_rot.append(self.rotation_tuple)
                sleep(time_aff)


    def update_coord(self):
        self.coord_pos["text"] = str(self.position_tuple)
        self.coord_rot["text"] = str(self.rotation_tuple)
        #self.aff_coord()
        self.after(self.update_interval, self.update_coord)

    def update_graph(self, i):
        """Met à jour la position du point sur le graphique."""
        x, y = self.position_tuple
        self.point.set_data(x, y)
        self.ax.set_title(f"Position: ({x}, {y})")
        self.canvas.draw()

    def move_keyboards(self):
        """Fonctions qui lient les touches au mouvements"""
        def up_keyboard(event):
            """Fonction associée au bouton Up"""
            print("Up")
            vitesseA = self.vitesse_motorA.get()
            vitesseB = self.vitesse_motorB.get()
            msg = "MOVE " + vitesseA + " " + vitesseB
            self.light.itemconfig(self.cercle, fill = "green")
            self.client.send(msg)
            # self.aff_coord()

        def backward_keyboard(event):
            """Fonction associée au bouton Down"""
            print("Down")
            vitesseA = self.vitesse_motorA.get()
            vitesseB = self.vitesse_motorB.get()
            msg = "BACKWARD " + vitesseA + " " + vitesseB
            self.light.itemconfig(self.cercle, fill = "green")
            self.client.send(msg)
            # self.aff_coord()

        def turn_left_keyboard(event):
            """Fonction associée au bouton Left"""
            print("Left")
            vitesseA = self.vitesse_motorA.get()
            msg = "LEFT " + vitesseA
            self.light.itemconfig(self.cercle, fill = "green")
            self.client.send(msg)
            # self.aff_coord()

        def turn_right_keyboard(event):
            """Fonction associée au bouton Right"""
            print("Right")
            vitesseB = self.vitesse_motorB.get()
            msg = "RIGHT " + vitesseB
            self.light.itemconfig(self.cercle, fill = "green")
            self.client.send(msg)
            # self.aff_coord()

        self.master.bind("<Up>", up_keyboard)
        self.master.bind("<Down>", backward_keyboard)
        self.master.bind("<Left>", turn_left_keyboard)
        self.master.bind("<Right>", turn_right_keyboard)

    def create_widgets(self):
        bg_choisi, fg_choisi = "#B7FFFF", "#080087"
        self.master.title("Interface Robot Lego")
        self.master["background"] = bg_choisi
        self["style"]="Custom.TFrame"

        style = ttk.Style()
        style.theme_use("xpnative")
        style.configure("Custom.TLabel", background = bg_choisi, fg = fg_choisi)
        style.configure("Custom.TButton", background = bg_choisi, fg = fg_choisi)
        style.configure("C.TButton", bg = "red", fg = "green")
        style.configure("Custom.TFrame", background = bg_choisi, fg = fg_choisi)


        frame_light = ttk.Frame(self, width = 30, style = "Custom.TFrame")
        self.light = tk.Canvas(frame_light, width = 30, height=32, bg = bg_choisi)
        self.light["highlightthickness"] = 0
        x_center, y_center, radius = 15,15, 10
        self.cercle = self.light.create_oval(
            x_center - radius, y_center - radius,  # x0, y0
            x_center + radius, y_center + radius,  # x1, y1
            fill = "white"
        )

        frame_left = tk.Frame(self, bg = "green")

        ##
        # self.frame_right = tk.Frame(self, bg = "red")
        #
        # self.coordinates = [(0, 0), (1, 2), (2, 3), (3, 5), (4, 7), (5, 8), (6, 6), (7, 4), (8, 3), (9, 1), (10, 0)]
        # self.fig = Figure(figsize = (8, 6), dpi = 100)
        # self.ax = self.fig.add_subplot(111)
        # self.ax.set_xlim(0, 10)
        # self.ax.set_ylim(0, 10)
        # self.point, = self.ax.plot([], [], 'ro') # BUG
        #
        # # Intégration de la figure dans Tkinter
        # self.canvas = FigureCanvasTkAgg(self.fig, master = self.frame_right)
        # self.canvas.draw() # equivalent de .pack()
        # self.canvas.get_tk_widget().pack(fill = tk.BOTH, expand = True)
        #
        # self.ani = animation.FuncAnimation(self.fig, self.update_graph, frames = 1000, interval = 1000, repeat = False)
        ##

        position_frame = ttk.Frame(frame_left,style = "Custom.TFrame")
        self.coord_button = ttk.Button(position_frame, text = "Coordonnées actuelle", style = "Custom.TButton")
        self.coord_button["command"] = self.threading_coord
        self.coord_pos = ttk.Label(position_frame, text = str(self.position_tuple), style = "Custom.TLabel")
        self.coord_rot = ttk.Label(position_frame, text = str(self.rotation_tuple), style = "Custom.TLabel")



        rowConnect = ttk.Frame(frame_left ,style = "Custom.TFrame")
        self.connect = ttk.Button(rowConnect, style="Custom.TButton")
        self.connect["text"] = "Connect"
        self.connect["command"] = self.connect_robot

        self.disconnect = ttk.Button(rowConnect,style="Custom.TButton")
        self.disconnect["text"] = "Disconnect"
        self.disconnect["command"] = self.disconnect_robot

        self.robot = tk.Entry(rowConnect)
        rowConnect.pack(side = "top", fill = tk.X, padx = 5, pady = 5)
        self.connect.pack(side = "left")
        self.disconnect.pack(side = "left")
        self.robot.pack(side = "left", expand = tk.YES, fill = tk.X)

        # Make motors
        rowA = ttk.Frame(frame_left, style = "Custom.TFrame")
        lab_motorA = ttk.Label(rowA,text = "Vitesse moteur gauche", anchor = 'w', style = "Custom.TLabel")
        self.vitesse_motorA = tk.Entry(rowA)
        rowA.pack(side = "top",fill = tk.X, padx = 5, pady = 5)
        lab_motorA.pack(side = "left")
        self.vitesse_motorA.pack(side = "right", expand = tk.YES, fill = tk.X)

        rowB = ttk.Frame(frame_left, style = "Custom.TFrame")
        lab_motorB = ttk.Label(rowB,text = "Vitesse moteur droit",anchor='w', style = "Custom.TLabel")
        self.vitesse_motorB = tk.Entry(rowB)
        rowB.pack(side= "top",fill = tk.X, padx = 5, pady = 5)
        lab_motorB.pack(side = "left")
        self.vitesse_motorB.pack(side = "right", expand = tk.YES, fill = tk.X)

        rowTime = ttk.Frame(frame_left, style = "Custom.TFrame")
        time_move = ttk.Label(rowTime, text = "Temps (s)",anchor='w', style = "Custom.TLabel")
        self.time_entry_robot = tk.Entry(rowTime)
        rowTime.pack(side = "top",fill = tk.X, padx= 5, pady = 5)
        time_move.pack(side = "left")
        self.time_entry_robot.pack(side = "right", expand = tk.YES, fill = tk.X)

        # Make move and stop buttons
        rowMenu = ttk.Frame(frame_left, style = "Custom.TFrame")
        self.move = ttk.Button(rowMenu, text = "MOVE",style = "Custom.TButton")
        self.move["command"] = self.move_robot

        self.backward = ttk.Button(rowMenu, text = "BACKWARD", style = "Custom.TButton")
        self.backward["command"] = self.backward_robot

        self.stop = ttk.Button(rowMenu, text = "STOP",style = "Custom.TButton")
        self.stop["command"] = self.stop_robot

        # Make keyboards usefull
        touches = ttk.Label(rowMenu,text = "Utilisez les flèches du clavier pour contrôler le robot",style = "Custom.TLabel")
        self.quit = ttk.Button(rowMenu, text = "QUIT",style = "Custom.TButton")

        self.quit["command"] = self.quitter


        rowTitle = ttk.Frame(frame_left, style = "Custom.TFrame")
        label_title = ttk.Label(rowTitle, text = "Samijote", style = "Custom.TLabel") # fg = "#080087" couleur de l'ecriture
        label_title["font"] = ("Bauhaus 93", 25)

        # def order_pack()
        # Ordre .pack()
        frame_light.pack(side = "left", fill = tk.Y)
        self.light.pack(side = "top")

        frame_left.pack(side = "left", fill = tk.Y)
        tk.Label(frame_left, text = "LEFT").pack()

        # self.frame_right.pack(side = "right", fill = tk.Y)
        # tk.Label(self.frame_right, text = "RIGHT").pack()


        rowMenu.pack(side = "top",fill = tk.X, padx = 5, pady = 5)
        self.move.pack(side = "left")
        self.backward.pack(side = "left")
        self.stop.pack(side = "left")
        touches.pack(side = "left")
        self.quit.pack(side = "right")

        position_frame.pack(side = "top",fill = tk.X, padx = 5, pady = 5)
        self.coord_button.pack(side = "top")
        self.coord_pos.pack(side = "top")
        self.coord_rot.pack(side = "top")

        rowTitle.pack(side = "bottom",fill = tk.X, padx = 5, pady = 5)
        label_title.pack(side = "left")


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

    def get_vitesse_time_robot(self) -> tuple:
        vitesseA = self.vitesse_motorA.get()
        vitesseB = self.vitesse_motorB.get()
        time_robot = self.time_entry_robot.get()
        return vitesseA, vitesseB, time_robot

    def move_robot(self) -> None:
        """Fonction associée au bouton Move"""
        print("MOVE pannel")
        # vitesseA, vitesseB, time_robot = self.get_vitesse_time_robot()
        # vitesseA = self.vitesse_motorA.get()
        # vitesseB = self.vitesse_motorB.get()
        # time = self.time_entry_robot.get()
        msg = "MOVE " + str(1000) + " " + str(1000) + " " + str(5)
        self.light.itemconfig(self.cercle, fill = "green")
        self.client.send(msg)
        # self.aff_coord()

    def backward_robot(self) -> None:
        """Fonction associée au bouton Move"""
        print("BACKWARD pannel")
        # vitesseA, vitesseB, time_robot = self.get_vitesse_time_robot()
        vitesseA = self.vitesse_motorA.get()
        vitesseB = self.vitesse_motorB.get()
        time = self.time_entry_robot.get()
        msg = "BACKWARD " + vitesseA + " " + vitesseB + " " + time
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
        print("Fermeture du programme.")
        self.mocap_node.stop()
        self.client.fermer()
        self.master.destroy()



# Programme principale
root = tk.Tk()
app = Application(master = root)
app.mainloop()



