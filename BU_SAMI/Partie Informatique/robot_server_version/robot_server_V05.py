## Modules
import socketserver

from ev3dev2.motor import OUTPUT_B, OUTPUT_C, LargeMotor
from ev3dev2.motor import SpeedPercent
# Adresse IP du robot : 100.75.155.133

class Handler_TCPServer(socketserver.BaseRequestHandler):
    def executer_commande(self, msg):
        # Execution du code par le robot
        m_gauche = LargeMotor(OUTPUT_B)
        m_droite = LargeMotor(OUTPUT_C)
        # mdiff = MoveDifferential(OUTPUT_B, OUTPUT_C)

        # print(f"Terminal Putty 'msg' : {msg}")

        msg_split = msg.decode("UTF-8").split()
        # print(f"Terminal Putty 'msg_split' : {msg_split}")
        # print(f"{msg = }")
        # print(f"{msg_split = }")
        print(msg)
        print(msg_split)

        # for perc in range(0,100,10):
        #     print(SpeedPercent(perc))

        # if len(msg_split) == 4:
        #     print("in")
        #     action, left_speed_motor_str, right_speed_motor_str, time_deplacement_s = msg_split
        #     left_speed_motor_int = int(left_speed_motor_str)
        #     right_speed_motor_int = int(right_speed_motor_str)
        #     time_deplacement_ms = 1000*time_deplacement_s

        if msg_split[0] == "MOVE":
            print("MOVE robot_server")
            # mdiff.on_for_distance(SpeedPercent(int(msg_split[1]), 200))
            m_gauche.run_timed(speed_sp = int(msg_split[1]), time_sp = int(msg_split[3])*1000)
            m_droite.run_timed(speed_sp = int(msg_split[2]), time_sp = int(msg_split[3])*1000)

        # if action == "MOVE":
        #     print("MOVE robot_server")
        #     # mdiff.on_for_distance(SpeedPercent(int(msg_split[1]), 200))
        #     m_gauche.run_timed(speed_sp = left_speed_motor_int, time_sp = time_deplacement_ms)
        #     m_droite.run_timed(speed_sp = right_speed_motor_int, time_sp = time_deplacement_ms)

        elif msg_split[0] == "BACKWARD":
            print("BACKWARD robot_server")
            # mdiff.on_for_distance(SpeedPercent(int(msg_split[1]), 200))
            m_gauche.run_timed(speed_sp = -int(msg_split[1]), time_sp = int(msg_split[3])*1000)
            m_droite.run_timed(speed_sp = -int(msg_split[2]), time_sp = int(msg_split[3])*1000)

        elif msg_split[0] == "LEFT":
            print("LEFT robot_server")
            # mdiff.on_for_distance(SpeedPercent(int(msg_split[1]), 200))
            m_gauche.run_timed(speed_sp = 0, time_sp = int(msg_split[3]))
            m_droite.run_timed(speed_sp = int(msg_split[2]), time_sp = int(msg_split[3]))


        elif msg_split[0] == "RIGHT":
            print("RIGHT robot_server")
            # mdiff.on_for_distance(SpeedPercent(int(msg_split[1]), 200))
            m_gauche.run_timed(speed_sp = int(msg_split[1]), time_sp = int(msg_split[3]))
            m_droite.run_timed(speed_sp = 0, time_sp = int(msg_split[3]))
            # .run_forever

        elif msg_split[0] == "STOP":
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
    numRobot = 4
    HOST, PORT = "100.75.155.13" + str(numRobot), 9999

    # Init the TCP server object, bind it to the localhost on 9999 port
    tcp_server = socketserver.TCPServer((HOST, PORT), Handler_TCPServer)

    # Activate the TCP server.
    # To abort the TCP server, press Ctrl-C.
    tcp_server.serve_forever()




