## Modules
import socketserver

from ev3dev2.motor import OUTPUT_B, OUTPUT_C, LargeMotor
# Adresse IP du robot : 100.75.155.133

class Handler_TCPServer(socketserver.BaseRequestHandler):
    def executer_commande(self, msg):
        # just send back ACK for data arrival confirmation
        self.request.sendall("ACK from TCP Server".encode())
        # Execution du code par le robot
        m_gauche = LargeMotor(OUTPUT_B)
        m_droite = LargeMotor(OUTPUT_C)

        msg_split = msg.decode("UTF-8").split()
        print(msg)
        print(msg_split)

        if len(msg_split) == 4:
            action, left_speed_motor_str, right_speed_motor_str, time_deplacement_s = msg_split
            left_speed_motor_int = int(float(left_speed_motor_str))
            right_speed_motor_int = int(float(right_speed_motor_str))
            time_deplacement_ms = int(1000*float(time_deplacement_s))
            print(left_speed_motor_int, right_speed_motor_int, time_deplacement_ms)
            print("int done")


        if msg_split[0] == "DEPLACER":
            print("DEPLACER robot_server")
            print(type(left_speed_motor_int), type(right_speed_motor_int))
            m_gauche.run_timed(speed_sp = left_speed_motor_int, time_sp = time_deplacement_ms)
            m_droite.run_timed(speed_sp = right_speed_motor_int, time_sp = time_deplacement_ms)
            print()


        elif msg_split[0] == "MOVE":
            print("MOVE robot_server")
            m_gauche.run_timed(speed_sp = left_speed_motor_int, time_sp = time_deplacement_ms)
            m_droite.run_timed(speed_sp = right_speed_motor_int, time_sp = time_deplacement_ms)


        elif msg_split[0] == "BACKWARD":
            print("BACKWARD robot_server")
            m_gauche.run_timed(speed_sp = -left_speed_motor_int, time_sp = time_deplacement_ms)
            m_droite.run_timed(speed_sp = -right_speed_motor_int, time_sp = time_deplacement_ms)

        elif msg_split[0] == "LEFT":
            print("LEFT robot_server")
            m_gauche.run_timed(speed_sp = 0, time_sp = time_deplacement_ms)
            m_droite.run_timed(speed_sp = right_speed_motor_int, time_sp = time_deplacement_ms)

        elif msg_split[0] == "RIGHT":
            print("RIGHT robot_server")
            m_gauche.run_timed(speed_sp = left_speed_motor_int, time_sp = time_deplacement_ms)
            m_droite.run_timed(speed_sp = 0, time_sp = time_deplacement_ms)

        elif msg_split[0] == "STOP":
            print("STOP robot_server")
            m_gauche.stop()
            m_droite.stop()


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
    numRobot = 3
    HOST, PORT = "100.75.155.13" + str(numRobot), 9999

    # Init the TCP server object, bind it to the localhost on 9999 port
    tcp_server = socketserver.TCPServer((HOST, PORT), Handler_TCPServer)

    # Activate the TCP server.
    # To abort the TCP server, press Ctrl-C.
    tcp_server.serve_forever()




