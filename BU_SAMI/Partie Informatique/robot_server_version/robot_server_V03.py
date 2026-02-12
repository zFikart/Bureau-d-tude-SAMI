import socketserver

from ev3dev2.motor import OUTPUT_B, OUTPUT_C, LargeMotor
# from ev3dev2.motor import SpeedPercent, MoveDifferential
from ev3dev2.motor import SpeedPercent

class Handler_TCPServer(socketserver.BaseRequestHandler):
    def executer_commande(self, msg):
        # Execution du code par le robot
        print("Le message msg est :", msg)

        valeurs = msg.decode("UTF-8").split()
        print(valeurs)

        # for perc in range(0,100,10):
        #     print(f"Vitesse {perc}% :" + SpeedPercent(perc))

        m_gauche = LargeMotor(OUTPUT_B)
        m_droite = LargeMotor(OUTPUT_C)

        # mdiff = MoveDifferential(OUTPUT_B, OUTPUT_C)
        if valeurs[0] == "MOVE":
            print("MOVE robot_server")
            # mdiff.on_for_distance(SpeedPercent(int(valeurs[1]), 200))
            m_gauche.run_timed(speed_sp = int(valeurs[1]), time_sp = valeurs[3])
            m_droite.run_timed(speed_sp = int(valeurs[2]), time_sp = valeurs[3])

        elif valeurs[0] == "BACKWARD":
            print("BACKWARD robot_server")
            # mdiff.on_for_distance(SpeedPercent(int(valeurs[1]), 200))
            m_gauche.run_timed(speed_sp = -int(valeurs[1]), time_sp = valeurs[3])
            m_droite.run_timed(speed_sp = -int(valeurs[2]), time_sp = valeurs[3])

        elif valeurs[0] == "LEFT":
            print("LEFT robot_server")
            # mdiff.on_for_distance(SpeedPercent(int(valeurs[1]), 200))
            m_gauche.run_timed(speed_sp = 0, time_sp = valeurs[3])
            m_droite.run_timed(speed_sp = int(valeurs[2]), time_sp = valeurs[3])

        elif valeurs[0] == "RIGHT":
            print("RIGHT robot_server")
            # mdiff.on_for_distance(SpeedPercent(int(valeurs[1]), 200))
            m_gauche.run_timed(speed_sp = int(valeurs[1]), time_sp = valeurs[3])
            m_droite.run_timed(speed_sp = 0, time_sp = valeurs[3])
            # .run_forever

        elif valeurs[0] == "STOP":
            print("STOP robot_server")
            m_gauche.stop()
            m_droite.stop()
        # just send back ACK for data arrival confirmation
        self.request.sendall("ACK from TCP Server".encode())
        #A compléter


    def handle(self):
        while True:
            # self.request - TCP socket connected to the client
            data = self.request.recv(1024)
            if not data:
                break
            data.strip()
            print("{} sent:".format(self.client_address[0]))
            self.executer_commande(data)

if __name__ == "__main__":
    numPC = 3
    HOST, PORT = "100.75.155.13" + str(numPC), 9999

    # Init the TCP server object, bind it to the localhost on 9999 port
    tcp_server = socketserver.TCPServer((HOST, PORT), Handler_TCPServer)

    # Activate the TCP server.
    # To abort the TCP server, press Ctrl-C.
    tcp_server.serve_forever()




