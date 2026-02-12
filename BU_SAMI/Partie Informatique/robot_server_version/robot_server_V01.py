import socketserver

# from ev3dev2.motor import OUTPUT_B, OUTPUT_C,
from ev3dev2.motor import OUTPUT_B, OUTPUT_C, LargeMotor
# from ev3dev2.motor import SpeedPercent, MoveDifferential

class Handler_TCPServer(socketserver.BaseRequestHandler):
    def executer_commande(self, msg):
        # Execution du code par le robot
        print("Le message msg est :\n")
        print(msg)

        valeurs = msg.decode("UTF-8").split()
        print(valeurs)

        m_gauche = LargeMotor(OUTPUT_B)
        m_droite = LargeMotor(OUTPUT_C)

        # mdiff = MoveDifferential(OUTPUT_B, OUTPUT_C)
        if valeurs[0] == "MOVE":
            # mdiff.on_for_distance(SpeedPercent(int(valeurs[1]), 200))
            m_gauche.run_timed(speed_sp = int(valeurs[1]), time_sp = valeur[3])
            m_droite.run_timed(speed_sp = int(valeurs[2]), time_sp = valeur[3])

        if valeurs[0] == "BACKWARD":
            # mdiff.on_for_distance(SpeedPercent(int(valeurs[1]), 200))
            m_gauche.run_timed(speed_sp = -int(valeurs[1]), time_sp = valeur[3])
            m_droite.run_timed(speed_sp = -int(valeurs[2]), time_sp = valeur[3])

        if valeurs[0] == "LEFT":
            # mdiff.on_for_distance(SpeedPercent(int(valeurs[1]), 200))
            m_gauche.run_timed(speed_sp = 0, time_sp = valeur[3])
            m_droite.run_timed(speed_sp = int(valeurs[2]), time_sp = valeur[3])

        if valeurs[0] == "RIGHT":
            # mdiff.on_for_distance(SpeedPercent(int(valeurs[1]), 200))
            m_gauche.run_timed(speed_sp = int(valeurs[1]), time_sp = valeur[3])
            m_droite.run_timed(speed_sp = 0, time_sp = 200)


        # just send back ACK for data arrival confirmation
        self.request.sendall("ACK from TCP Server".encode())
        #A compléter


    def handle(self):
        while 1:
            # self.request - TCP socket connected to the client
            data = self.request.recv(1024)
            if not data:
                break
            data.strip()
            print("{} sent:".format(self.client_address[0]))
            self.executer_commande(data)

if __name__ == "__main__":
    HOST, PORT = "100.75.155.134", 9999

    # Init the TCP server object, bind it to the localhost on 9999 port
    tcp_server = socketserver.TCPServer((HOST, PORT), Handler_TCPServer)

    # Activate the TCP server.
    # To abort the TCP server, press Ctrl-C.
    tcp_server.serve_forever()




