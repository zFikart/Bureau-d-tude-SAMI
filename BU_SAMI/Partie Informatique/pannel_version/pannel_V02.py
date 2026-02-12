import tkinter as tk
import socket

# Se renseigner sur le module socket
class TCPClient:
    """Gere communication réseau"""
    def __init__(self):
        self.sock = socket.socket(
                            socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, host, port):
        self.sock.connect((host, port))

    def send(self, msg:str):
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
        self.master.title("Test")
        self.pack()
        self.create_widgets()       # methode creee
        self.client = TCPClient()   # objet de classe

    def create_widgets(self):
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

##
        rowTime = tk.Frame(self)
        time_move = tk.Label(rowTime,text = "Temps",anchor='w')
        self.time_entry_robot = tk.Entry(rowTime)
        rowTime.pack(side= "top",fill = tk.X, padx = 5, pady = 5)
        time_move.pack(side = "left")
        self.time_entry_robot.pack(side = "right", expand = tk.YES, fill = tk.X)

##
        # Make move and stop buttons
        self.move = tk.Button(self.master, text = "MOVE", fg = "green")
        self.move["command"] = self.move_robot
        self.move.pack(side = "left")

        self.backward = tk.Button(self.master, text = "BACK", fg = "blue")
        self.backward["command"] = self.backward_robot
        self.backward.pack(side = "left")

        self.stop = tk.Button(self.master, text = "STOP", fg = "red")
        self.stop["command"] = self.stop_robot
        self.stop.pack(side = "left")

        self.quit = tk.Button(self.master, text = "QUIT")
        self.quit["command"] = self.quitter
        self.quit.pack(side = "left")


    def connect_robot(self):
        """Fonction associée au bouton Connect"""
        robot_addr = self.robot.get() # recupere Entry str
        print("Le robot s'est bien connecté au serveur !")
        print("L'adresse IP est :", robot_addr)
        self.client.connect(robot_addr, 9999)

    def backward_robot(self):
        """Fonction associée au bouton Back"""
        vitesseA = self.vitesse_motorA.get()
        vitesseB = self.vitesse_motorB.get()
        time_move = self.time_entry_robot.get()
        msg = "BACKWARD " + vitesseA + " " + vitesseB + " " + time_move
        self.client.send(msg)

    def move_robot(self):
        """Fonction associée au bouton Move"""
        vitesseA = self.vitesse_motorA.get()
        vitesseB = self.vitesse_motorB.get()
        time_move = self.time_entry_robot.get()
        msg = "MOVE " + vitesseA + " " + vitesseB + " " + time_move
        self.client.send(msg)

    def stop_robot(self):
        """Fonction associée au bouton STOP"""
        msg = "STOP"
        self.client.send(msg)

    def quitter(self):
        """Fonction associée au bouton QUIT"""
        self.client.fermer()
        self.master.destroy()


# Programme principale
root = tk.Tk()
app = Application(master=root)
app.mainloop()



