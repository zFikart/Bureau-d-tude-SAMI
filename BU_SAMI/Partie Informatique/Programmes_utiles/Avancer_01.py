## Avancer de 20 cm et afficher "J'avance"

from ev3dev2.motor import OUTPUT_B, OUTPUT_C, LargeMotor
from ev3dev2.button import Button
from time import sleep

# Connect two large motors on output ports B and C
# lmotor, rmotor = [LargeMotor(address) for address in (OUTPUT_B ,OUTPUT_C)]

# while not button.enter:
#     for m in (lmotor, rmotor):
#         m.run_timed(speed_sp = 600, time_sp = 100)
#     sleep(0.5)

# Wait 0.5 seconds while motors are rolling

import mocap_node as mcn
import Natnet_Client as nnc
from debug import *
from common import euler_from_quaternion
from time import sleep
# from NatNetPacket import MessageType as mess

rom ev3dev2.motor import OUTPUT_B, OUTPUT_C, LargeMotor
from ev3dev2.motor import SpeedPercent

for perc in range(0,100,10):
    print(f"Vitesse {perc}% :" + SpeedPercent(perc))

m_gauche = LargeMotor(OUTPUT_B)
m_droite = LargeMotor(OUTPUT_C)


def main():
    # 100.75.155.133
    numPC = 3 # MODIFICATION A CHAQUE FOIS numPC
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
    mocap_node.run()

    m_gauche.run_timed(speed_sp = 1000, time_sp = 5000)
    m_droite.run_timed(speed_sp = 1000, time_sp = 5000)
    while True:
        L3_pos, L3_rot = mocap_node.getPose("Lego3")
        print(L3_pos)
        sleep(1)

    mocap_node.stop()

