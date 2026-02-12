import tkinter as tk
import threading
import time
import sys
import os
sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'optitrack//src'))
import mocap_node as mcn
import Natnet_Client as nnc
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

class Application(tk.Frame):
    """Création et gestion de l'interface utilisateur"""
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.move_keyboards()
        self.client = TCPClient()
        self.mocap_node = None
        self.positions_thread = None
        self.positions_running = threading.Event()
        self.positions_running.set()
        self.create_mocap_node()
        self.start_positions_thread()

    def create_mocap_node(self):
        srvAddr = "100.64.212.160"
        srvPort = 1510
        numPC = 3
        cltAddr = "100.64.212.15" + str(numPC)
        cltDataPort = 1511
        multcastaddr = "225.1.1.1"
        cltCmdPort = 0
        natnet_client = nnc.NatnetClient(srvAddr, cltAddr, multcastaddr, srvPort, cltDataPort)
        self.mocap_node = mcn.MocapNode("PC" + str(numPC), natnet_client)

    def positions_loop(self):
        while self.positions_running.is_set():
            if self.mocap_node:
                self.mocap_node.run()
                L3_pos, L3_rot = self.mocap_node.getPose("Lego3")
                self.update_coordinates(L3_pos)
                self.mocap_node.stop()
            time.sleep(1)

    def start_positions_thread(self):
        self.positions_thread = threading.Thread(target=self.positions_loop)
        self.positions_thread.daemon = True
        self.positions_thread.start()

    def stop_positions_thread(self):
        self.positions_running.clear()
        self.positions_thread.join()

    def update_coordinates(self, L3_pos):
        self.coord_label.config(text=f"Coordinates: {L3_pos}")

    def move_keyboards(self):
        def up_keyboard(event):
            self.send_command("MOVE")

        def backward_keyboard(event):
            self.send_command("BACKWARD")

        def turn_left_keyboard(event):
            self.send_command("LEFT")

        def turn_right_keyboard(event):
            self.send_command("RIGHT")

        self.master.bind("<Up>", up_keyboard)
        self.master.bind("<Down>", backward_keyboard)
        self.master.bind("<Left>", turn_left_keyboard)
        self.master.bind("<Right>", turn_right_keyboard)

    def create_widgets(self):
        self.master.title("Interface Robot Lego")

        position = tk.Frame(self, bg="blue")
        position.pack(side="bottom")
        self.pos = tk.Button(position, text="position actuelle")
        self.pos.pack()
        self.coord_label = tk.Label(position, text="Coordinates: ")
        self.coord_label.pack()

        self.light = tk.Canvas(self, width=30)
        self.light.pack(side="left")
        x_center, y_center, radius = 15, 15, 10
        self.cercle = self.light.create_oval(
            x_center - radius, y_center - radius,
            x_center + radius, y_center + radius,
            fill="white"
        )

        rowConnect = tk.Frame(self)
        self.connect = tk.Button(rowConnect, text="Connect", command=self.connect_robot)
        self.disconnect = tk.Button(rowConnect, text="Disconnect", command=self.disconnect_robot)
        self.robot = tk.Entry(rowConnect)
        rowConnect.pack(side="top", fill=tk.X, padx=5, pady=5)
        self.connect.pack(side="left")
        self.disconnect.pack(side="left")
        self.robot.pack(side="left", expand=tk.YES, fill=tk.X)

        rowA = tk.Frame(self)
        lab_motorA = tk.Label(rowA, text="Vitesse moteur gauche", anchor='w')
        self.vitesse_motorA = tk.Entry(rowA)
        rowA.pack(side="top", fill=tk.X, padx=5, pady=5)
        lab_motorA.pack(side="left")
        self.vitesse_motorA.pack(side="right", expand=tk.YES, fill=tk.X)

        rowB = tk.Frame(self)
        lab_motorB = tk.Label(rowB, text="Vitesse moteur droit", anchor='w')
        self.vitesse_motorB = tk.Entry(rowB)
        rowB.pack(side="top", fill=tk.X, padx=5, pady=5)
        lab_motorB.pack(side="left")
        self.vitesse_motorB.pack(side="right", expand=tk.YES, fill=tk.X)

        rowTime = tk.Frame(self)
        time_move = tk.Label(rowTime, text="Temps (s)", anchor='w')
        self.time_entry_robot = tk.Entry(rowTime)
        rowTime.pack(side="top", fill=tk.X, padx=5, pady=5)
        time_move.pack(side="left")
        self.time_entry_robot.pack(side="right", expand=tk.YES, fill=tk.X)

        self.move = tk.Button(self, text="MOVE", fg="green", command=self.move_robot)
        self.backward = tk.Button(self, text="BACKWARD", fg="green", command=self.backward_robot)
        self.stop = tk.Button(self, text="STOP", fg="red", command=self.stop_robot)
        self.quit = tk.Button(self, text="QUIT", command=self.quitter)
        self.move.pack(side="left")
        self.backward.pack(side="left")
        self.stop.pack(side="left")
        self.quit.pack(side="right")

        touches = tk.Label(self, text="Utilisez les flèches du clavier pour contrôler le robot")
        touches.pack()

    def send_command(self, command):
        vitesseA = self.vitesse_motorA.get()
        vitesseB = self.vitesse_motorB.get()
        time = self.time_entry_robot.get()
        msg = f"{command} {vitesseA} {vitesseB} {time}"
        self.light.itemconfig(self.cercle, fill="green" if command != "STOP" else "red")
        self.client.send(msg)

    def connect_robot(self):
        robot_addr = self.robot.get()
        print("Le robot s'est bien connecté au serveur !")
        print("L'adresse IP est :", robot_addr)
        self.light.itemconfig(self.cercle, fill="blue")
        self.client.connect(robot_addr, 9999)

    def disconnect_robot(self):
        print("Le robot s'est déconnecté du serveur.")
        self.light.itemconfig(self.cercle, fill="white")
        self.client.fermer()

    def move_robot(self):
        self.send_command("MOVE")

    def backward_robot(self):
        self.send_command("BACKWARD")

    def stop_robot(self):
        self.send_command("STOP")

    def quitter(self):
        self.stop_positions_thread()
        self.client.fermer()
        self.master.destroy()

root = tk.Tk()
app = Application(master=root)
app.mainloop()
