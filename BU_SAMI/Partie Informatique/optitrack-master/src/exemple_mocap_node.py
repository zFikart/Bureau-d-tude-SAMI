#! python3
# coding: utf-8
#
# Ce script permet de récupérer Motive et de la sauvegarder dans un fichier en tant que .bin

import sys, os
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'optitrack//src'))

import numpy as np

# Pour interface
import tkinter as tk
# from pannel_V03 import *

import mocap_node as mcn
import Natnet_Client as nnc
from debug import *
from common import euler_from_quaternion
import time
# from NatNetPacket import MessageType as mess

# rom ev3dev2.motor import OUTPUT_B, OUTPUT_C, LargeMotor
# from ev3dev2.motor import SpeedPercent

# for perc in range(0,100,10):
#     print(f"Vitesse {perc}% :" + SpeedPercent(perc))

# m_gauche = LargeMotor(OUTPUT_B)
# m_droite = LargeMotor(OUTPUT_C)

# mdiff = MoveDifferential(OUTPUT_B, OUTPUT_C)


def main():
    # 100.75.155.133
    numPC = 3 # MODIFICATION A CHAQUE FOIS numPC
    #  Remove former logfile
    if os.path.isfile(".trace.txt"):
        os.remove(".trace.txt")

    # Configure fake server
    srvAddr = "100.64.212.160" # MODIFICATION .160
    srvPort  = 1510

    # Configure Natnet client
    cltAddr = "100.64.212.15" + str(numPC) # MODIFICATION  numPC
    cltDataPort = 1511
    multcastaddr = "225.1.1.1"
    cltCmdPort = 0
    natnet_client = nnc.NatnetClient(srvAddr,cltAddr,multcastaddr,srvPort,cltDataPort)

    # # Generate a MocapNode
    mocap_node = mcn.MocapNode("PC" + str(numPC),natnet_client)
    # trace("EXEMPLE - Initialisation du noeud MoCap")
    # trace(mocap_node.to_string() + "--------------\n\n")
    #
    # # Start natnet client in background thread
    mocap_node.run()
    # trace("EXEMPLE - Démarrage du noeud MoCap")
    # trace(mocap_node.to_string() + "--------------\n\n")
    #
    # # Met à jour la description du modele :
    # mocap_node.updateModelInfo()
    # trace("EXEMPLE - Mise à jour du modèle")
    # trace(mocap_node.to_string() + "--------------\n\n")

    # Demande pose Lego 1
    # L1_pos, L1_rot = mocap_node.getPose("Lego1")
    # trace("EXEMPLE - Demande la pose du Lego1")
    # # trace(mocap_node.to_string() + "--------------\n\n")
    # # trace("EXEMPLE - Résultats pour le Lego1")
    # trace("\tPosition: [{},{},{}]".format(*L1_pos))
    # trace("\tRotation: [{},{},{}]".format(*np.degrees(euler_from_quaternion(*L1_rot))) + "--------------\n\n")

    # trace("Positions :\n")
    # trace(L1_pos)

    # trace("Rotation :\n")
    # trace(L1_rot)

    # print(L1_pos)
    # print(L1_rot)

    # Demande pose Lego 2
    # L2_pos, L2_rot = mocap_node.getPose("Lego2")
    # trace("EXEMPLE - Demande la pose du Lego2")
    # # trace(mocap_node.to_string() + "--------------\n\n")
    # # trace("EXEMPLE - Résultats pour le Lego2")
    # trace("\tPosition: [{},{},{}]".format(*L2_pos))
    # trace("\tRotation: [{},{},{}]".format(*np.degrees(euler_from_quaternion(*L2_rot))) + "--------------\n\n")
    #
    # # Demande pose Lego 3
    # root = tk.Tk()
    # app = Application(master = root)
    # app.mainloop()
    # m_gauche.run_timed(speed_sp = 1000, time_sp = 5000)
    # m_droite.run_timed(speed_sp = 1000, time_sp = 5000)
    coord = []
    start = time.time()
    while True:
        L3_pos, L3_rot = mocap_node.getPose("Lego3")
        print(f"{time.time() - start}: {L3_pos}")
        coord.append(L3_pos)
        trace(f"\t{L3_pos}")
        time.sleep(0.1)

    nbre_sec = time.time() - start
    print(nbre_sec)
    # trace("EXEMPLE - Demande la pose du Lego3")
    # # trace(mocap_node.to_string() + "--------------\n\n")
    # # trace("EXEMPLE - Résultats pour le Lego3")
    # trace("\tPosition: [{},{},{}]".format(*L3_pos))
    # trace("\tRotation: [{},{},{}]".format(*np.degrees(euler_from_quaternion(*L3_rot))) + "--------------\n\n")

    # Récupère plusieurs trames
    # file_names = mocap_node.dump("data", 10)

    # Stop threads
    mocap_node.stop()
    # trace("EXEMPLE - Arrêt du noeud MoCap")
    # trace(mocap_node.to_string() + "--------------\n\n")
    print(coord)
    return coord


if __name__ == "__main__":
    temps = main()




