import tkinter as tk
import socket
from PIL import Image,ImageTk

# Se renseigner sur le module socket
class TCPClient:
    """Gere communication réseau"""
    def __init__(self):
        self.sock = socket.socket(
                            socket.AF_INET, socket.SOCK_STREAM)

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


class Application(tk.Frame):
    """Création et gestion de l'interface utilisateur"""
    def __init__(self, master = None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.move_keyboards()
        self.create_widgets()       # methode creee
        self.client = TCPClient()   # objet de classe

    def move_keyboards(self):
        """Fonctions qui lient les touches au mouvements"""
        def up_keyboard(event):
            """Fonction associée au bouton Up"""
            print("up")
            vitesseA = self.vitesse_motorA.get()
            vitesseB = self.vitesse_motorB.get()
            msg = "MOVE " + vitesseA + " " + vitesseB
            self.client.send(msg)
        def backward_keyboard(event):
            """Fonction associée au bouton Down"""
            print("down")
        def turn_left_keyboard(event):
            """Fonction associée au bouton Left"""
            print("left")
        def turn_right_keyboard(event):
            """Fonction associée au bouton Right"""
            print("right")


    def create_widgets(self):
        self.master.title("Interface Robot Lego")
        rowConnect = tk.Frame(self)
        self.connect = tk.Button(rowConnect)
        self.connect["text"] = "Connect"
        self.connect["command"] = self.connect_robot    # connect_robot est une fonction

        self.robot = tk.Entry(rowConnect)   # saisi
        rowConnect.pack(side = "top", fill = tk.X, padx = 5, pady = 5)
        self.connect.pack(side = "left")                                # pack le bouton a gauche
        self.robot.pack(side = "left", expand = tk.YES, fill = tk.X)    # pack la saisi a droite

        # Make motors
        rowA = tk.Frame(self)
        lab_motorA = tk.Label(rowA,text = "Vitesse moteur gauche", anchor = 'w')
        self.vitesse_motorA = tk.Entry(rowA)
        rowA.pack(side = "top",fill = tk.X, padx = 5, pady = 5)
        lab_motorA.pack(side = "left")
        self.vitesse_motorA.pack(side = "right", expand = tk.YES, fill = tk.X)

        rowB = tk.Frame(self)
        lab_motorB = tk.Label(rowB,text = "Vitesse moteur droit",anchor='w')
        self.vitesse_motorB = tk.Entry(rowB)
        rowB.pack(side= "top",fill = tk.X, padx = 5, pady = 5)
        lab_motorB.pack(side = "left")
        self.vitesse_motorB.pack(side = "right", expand = tk.YES, fill = tk.X)

        rowTime=tk.Frame(self)
        time_move=tk.Label(rowTime, text = "Temps",anchor='w')
        self.time_entry_robot=tk.Entry(rowTime)
        rowTime.pack(side = "top",fill = tk.X, padx= 5, pady = 5)
        time_move.pack(side = "left")
        self.time_entry_robot.pack(side = "right", expand = tk.YES, fill = tk.X)

        # Make move and stop buttons
        self.move = tk.Button(self.master, text = "MOVE", fg = "green")
        self.move["command"] = self.move_robot
        self.move.pack(side = "left")

        self.backward = tk.Button(self.master, text = "BACKWARD", fg = "green")
        self.backward["command"] = self.backward_robot
        self.backward.pack(side = "left")

        self.stop = tk.Button(self.master, text = "STOP", fg = "red")
        self.stop["command"] = self.stop_robot
        self.stop.pack(side = "left")

        self.quit = tk.Button(self.master, text = "QUIT")
        self.quit["command"] = self.quitter
        self.quit.pack(side = "left")

        # Make keyboards usefull
        touches=tk.Label(self.master,text="Utilisez les flèches du clavier pour contrôler le robot")
        touches.pack()

        def up_keyboard(event):
            """Fonction associée au bouton Up"""
            print("up")
            vitesseA = self.vitesse_motorA.get()
            vitesseB = self.vitesse_motorB.get()
            msg = "MOVE " + vitesseA + " " + vitesseB
            self.client.send(msg)

        def backward_keyboard(event):
            """Fonction associée au bouton Down"""
            print("down")
            vitesseA = self.vitesse_motorA.get()
            vitesseB = self.vitesse_motorB.get()
            msg = "BACKWARD " + vitesseA + " " + vitesseB
            self.client.send(msg)

        def turn_left_keyboard(event):
            """Fonction associée au bouton Left"""
            print("left")
            vitesseA = self.vitesse_motorA.get()
            msg = "LEFT " + vitesseA
            self.client.send(msg)

        def turn_right_keyboard(event):
            """Fonction associée au bouton Right"""
            print("right")
            vitesseB = self.vitesse_motorB.get()
            msg = "RIGHT " + vitesseB
            self.client.send(msg)

        self.master.bind("<Up>",up_keyboard)
        self.master.bind("<Down>",backward_keyboard)
        self.master.bind("<Left>",turn_left_keyboard)
        self.master.bind("<Right>",turn_right_keyboard)


    def connect_robot(self):
        """Fonction associée au bouton Connect"""
        robot_addr = self.robot.get() # recupere Entry str
        print("Le robot s'est bien connecté au serveur !")
        print("L'adresse IP est :", robot_addr)
        self.client.connect(robot_addr, 9999)

    def move_robot(self):
        """Fonction associée au bouton Move"""
        vitesseA = self.vitesse_motorA.get()
        vitesseB = self.vitesse_motorB.get()
        time=self.time_entry_robot.get()
        msg = "MOVE " + vitesseA + " " + vitesseB + " " + time
        self.client.send(msg)

    def backward_robot(self):
        """Fonction associée au bouton Move"""
        vitesseA = self.vitesse_motorA.get()
        vitesseB = self.vitesse_motorB.get()
        time=self.time_entry_robot.get()
        msg = "BACKWARD " + vitesseA + " " + vitesseB + " " + time
        self.client.send(msg)

    def stop_robot(self):
        """Fonction associée au bouton STOP"""
        msg = "STOP"
        self.client.send(msg)

    def quitter(self):
        """Fonction associée au bouton QUIT"""
        self.client.fermer()
        self.master.destroy()

    # def move_keyboard(self,event):
    #     """Fonction associée au bouton Up"""
    #     print("up")
    # def backward_keyboard(self,event):
    #     """Fonction associée au bouton Down"""
    #     print("down")
    # def turn_left_keyboard(self,event):
    #     """Fonction associée au bouton Left"""
    #     print("left")
    # def turn_right_keyboard(self, event):
    #     """Fonction associée au bouton Right"""
    #     print("right")
    #


# Programme principale
root = tk.Tk()
app = Application(master=root)
app.mainloop()



