# coding: utf-8

""" Tests unitaires pour le client Natnet

Auteur : Clement FAUVEL
Date : Janvier 2021
"""

import unittest
import threading
import time

# Import for udp client methods
import socket
import sys, os
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'src'))
from Natnet_Client import *



class TestNatnetClient(unittest.TestCase):
    def setUp(self):
        # Configure server / client
        self.srvAddr = "127.0.0.1"
        self.multcastaddr = "225.1.2.3"
        self.cltAddr = "127.0.0.1"
        self.cltDataPort = 1511
        self.cltCmdPort = 0
        self.srvCmdPort  = 1510
        self.fakeServer = self.__set_fake_server()
        self.rcvMess = ""
        self.udpClient = NatnetClient(self.srvAddr,self.cltAddr,self.multcastaddr,self.srvCmdPort,self.cltDataPort)   
        self.timeout = 10   # timeout for while functions during tests
        self.counter = 0

    def tearDown(self):      
        self.fakeServer.close() 
        self.__closeSockets() 


    def __closeSockets(self):
        try:
            self.udpClient.commandSocket.close()
        except AttributeError:
            pass
        try:
            self.udpClient.dataSocket.close()
        except AttributeError:
            pass        


    def __set_fake_server(self):
            server_sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
            server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  
            server_sock.bind((self.srvAddr, self.srvCmdPort))
            return server_sock

    def __run_fake_server(self):
            # Run a server to listen for a connection and then close it 
            while True:
                    data, addr = self.fakeServer.recvfrom(32768) #32k byte buffer size
                    if (len(data) >0):
                        self.rcvMess = data
                        if (self.rcvMess == b"ping_data"):
                            addr = (self.cltAddr,self.cltDataPort)
                        if(self.rcvMess == b"ping_cmd"):
                            addr = (self.cltAddr,self.cltCmdPort)
                        if(self.rcvMess == b"count"):
                            self.counter += 1
                            data = str(self.counter).encode('utf-8')
                        self.fakeServer.sendto(data,addr)
                        break


    def test_NatnetClient(self):
        self.assertEqual(self.udpClient.serverIPAddress,self.srvAddr,"")
        self.assertEqual(self.udpClient.localIPAddress,self.cltAddr,"")
        self.assertEqual(self.udpClient.multicastAddress,self.multcastaddr,"")
        self.assertEqual(self.udpClient.srvCmdPort,self.srvCmdPort,"")
        self.assertEqual(self.udpClient.cltDataPort,self.cltDataPort,"")


    def test__initSockets(self):
        self.udpClient._NatnetClient__initSockets()
        # Check if sockets exist
        self.assertTrue(type(self.udpClient.commandSocket),'socket')
        self.assertTrue(type(self.udpClient.dataSocket),'socket')

    def test_startListeningFromSockets(self):
        self.dataThread, self.commandThread = self.udpClient.startListeningFromSockets()
        # Check if thread are running
        self.assertTrue(self.dataThread.is_alive())
        self.assertTrue(self.commandThread.is_alive())

    def test_stoptListeningFromSockets(self):
        self.dataThread, self.commandThread = self.udpClient.startListeningFromSockets()
        self.udpClient.stopListeningFromSockets(self.dataThread,self.commandThread)
        # Check if thread are not running
        self.assertFalse(self.dataThread.is_alive())
        self.assertFalse(self.commandThread.is_alive())


    def test_sendCommand(self):
        # Start command socket and thread
        self.dataThread, self.commandThread = self.udpClient.startListeningFromSockets()
        self.cltCmdPort = self.udpClient.cltCmdPort

        # Start fake server in background thread
        server_thread = threading.Thread(target=self.__run_fake_server)
        server_thread.start()
        
        # Send command to server
        cmdStr = "Ping".encode('utf-8')
        self.udpClient.sendCommand(cmdStr,self.udpClient.commandSocket,(self.srvAddr,self.srvCmdPort))
               
        # Check if the command message has been received
        server_thread.join()
        self.assertEqual(self.rcvMess,cmdStr,"")


    def test_rcvCmd(self):
        # Start data socket and thread
        self.dataThread, self.commandThread = self.udpClient.startListeningFromSockets()
        self.cltCmdPort = self.udpClient.cltCmdPort
        
        # Start fake server in background thread
        server_thread = threading.Thread(target=self.__run_fake_server)
        server_thread.start()

        # Ask server to ping client on command port
        cmdStr = "ping_cmd".encode('utf-8')
        self.udpClient.sendCommand(cmdStr,self.udpClient.commandSocket,(self.srvAddr,self.srvCmdPort))
        
        # Check if the ping message has been received
        t0 = time.time()
        while time.time() < t0 + self.timeout:
            bufMess = self.udpClient.getCmdBuffer()
            if(len(bufMess) > 0):
                self.assertEqual(bufMess,cmdStr)
                break
            else:
                time.sleep(0.1)


    def test_rcvData(self):
        # Start data socket and thread
        self.dataThread, self.commandThread = self.udpClient.startListeningFromSockets()
        self.cltCmdPort = self.udpClient.cltCmdPort
        
        # Start fake server in background thread
        server_thread = threading.Thread(target=self.__run_fake_server)
        server_thread.start()

        # Ask server to ping client on data port
        cmdStr = "ping_data".encode('utf-8')
        self.udpClient.sendCommand(cmdStr,self.udpClient.commandSocket,(self.srvAddr,self.srvCmdPort))
        
        # Check if the ping message has been received
        t0 = time.time()
        while time.time() < t0 + self.timeout:
            bufMess = self.udpClient.getDataBuffer()
            if(len(bufMess) > 0):
                self.assertEqual(bufMess,cmdStr)
                break
            else:
                time.sleep(0.1)

        
    def test_getBuf(self):
        # Start data socket and thread
        self.dataThread, self.commandThread = self.udpClient.startListeningFromSockets()
        self.cltCmdPort = self.udpClient.cltCmdPort        

        # Ask server to count 3 times on cmd portcmdStr = "ping_data"            
        for i in range(0,3):            
            server_thread = threading.Thread(target=self.__run_fake_server)
            server_thread.start()
            time.sleep(0.1)

            cmdStr = "count".encode('utf-8')
            self.udpClient.sendCommand(cmdStr,self.udpClient.commandSocket,(self.srvAddr,self.srvCmdPort))
        
        # Check if the behaviour of getCmdBuffer(idx=0) and the contents of the buffer
        time.sleep(0.1)
        bufMess = self.udpClient.getCmdBuffer(0)
        self.assertEqual(bufMess,b'3')
        bufMess = self.udpClient.getCmdBuffer(1)
        self.assertEqual(bufMess,b'2')
        bufMess = self.udpClient.getCmdBuffer(2)
        self.assertEqual(bufMess,b'')



if __name__ == '__main__':
        unittest.main(verbosity=2)