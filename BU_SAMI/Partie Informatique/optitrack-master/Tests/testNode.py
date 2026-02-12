# coding: utf-8

""" Tests unitaires pour le noeud Motion Capture

Auteur : Clement FAUVEL
Date : Janvier 2021
"""
import unittest
import socket
import threading
import time
import numpy as np
import sys, os
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'src'))

from NatNetPacket import *
from Natnet_Client import *
from mocap_node import *


class testNode(unittest.TestCase): #OK

    def setUp(self):
        # Configure fake server
        srvAddr = "127.0.0.1"
        srvPort  = 1510
        self.fakeServer = self.__set_fake_server(srvAddr,srvPort)
        self.message_5 = self.__openData("Tests/streamData/sample_5.bin")
        self.message_7 = self.__openData("Tests/streamData/sample_7.bin")


        # Configure Natnet client
        self.cltAddr = "127.0.0.1"
        self.cltDataPort = 1511
        multcastaddr = "225.1.2.3"
        cltCmdPort = 0
        self.natnet_client = NatnetClient(srvAddr,self.cltAddr,multcastaddr,srvPort,self.cltDataPort)

        # Generate a MocapNode
        self.mocap_node = MocapNode("DEFAULT", self.natnet_client)

        # Tests parameters
        self.timeout = 10   # timeout for while functions during tests

        # Start fake server in background thread
        self.server_thread = threading.Thread(target=self.__run_fake_server)
        self.server_thread.start()
        time.sleep(0.1)

        # Start natnet client in background thread
        self.mocap_node.run()
        time.sleep(0.1)


    def tearDown(self):
        # Close sockets and threads
        self.mocap_node.stop()
        # Close server and thread
        self.fakeServer.close()
        self.server_thread.join()

    def __set_fake_server(self,srvAddr,srvPort):
        server_sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((srvAddr, srvPort))
        return server_sock


    def __run_fake_server(self):
    # Run a server
        running = True
        while running:
            try:
                data, addr = self.fakeServer.recvfrom(32768) #32k byte buffer size
                if (len(data) >0):
                    packet = Packet.fromData(data)
                    if (packet.messageId == MessageType().RequestModelDef): # Request model description
                        request = self.message_5
                        naddr = (self.cltAddr,self.natnet_client.cltCmdPort)
                    elif (packet.messageId == MessageType().RequestFrameOfData): # Request frame of data
                        request = self.message_7
                        naddr = (self.cltAddr,self.natnet_client.cltDataPort)
                    elif (packet.messageId == MessageType().Connect):
                        request = "Ping".encode('utf-8')
                        naddr = (self.cltAddr,self.natnet_client.cltCmdPort)

                    # Send data on client data port
                    self.fakeServer.sendto(request,naddr)
            except:
                running = False


    def __openData(self,path):
        fh = open(path,"rb")
        bh = bytes(fh.read())
        fh.close()
        return bh


    def test_sendRequest(self):
        # Generate a command packet then send it to server
        self.mocap_node.sendRequest(MessageType().RequestModelDef)

        # Check if some answer were received
        bufMess = self.mocap_node._MocapNode__wait_for_message("cmd")

        # Check if the received packet correspond to the request
        self.assertEqual(bufMess,self.message_5)


    def test_updateModelInfo(self):
        # Catch (id,idx) for rigid body as tuples, where idx is the rigidbody position in the list
        ModelInfo = self.mocap_node.updateModelInfo()

        # Check if "Lego2" has Id==2 and index == 1 in the list
        self.assertEqual(ModelInfo["Lego2"],(2,1))


    def test_getPose(self):
        # Send a request prior getPose to speed the test
        self.mocap_node.sendRequest(MessageType().RequestFrameOfData)
        pos, rot = self.mocap_node.getPose("Lego2")
        # Check if pos and rot size and type
        self.assertTrue(len(pos)==3 and len(rot)==4)
        self.assertIsInstance(pos[1],float)
        # Check if pos and rot values are closed to the real ones
        Lego2_pos = np.array([0.9228857159614563,0.12074480205774307,0.10839684307575226])
        Lego2_rot = np.array([0.00013000886247027665,0.3534943163394928,0.010053183883428574,0.9353827238082886])
        pos_diff = np.array(pos)-Lego2_pos
        rot_diff = np.array(rot)-Lego2_rot
        self.assertTrue(pos_diff.dot(pos_diff)<0.01)
        self.assertTrue(rot_diff.dot(rot_diff)<0.01)

    def test_getPosition2DandYaw(self):
        # Send a request prior getPose to speed the test
        self.mocap_node.sendRequest(MessageType().RequestFrameOfData)
        pos, yaw = self.mocap_node.getPos2DAndYaw("Lego2")
        # Check if pos and rot size and type
        self.assertTrue(len(pos)==2 and len(yaw)==1)
        self.assertIsInstance(pos[1],float)
        # Check if pos and rot values are closed to the real ones
        Lego2_pos=np.array([-0.9228857159614563,0.10839684307575226])
        Lego2_yaw=np.array([0.7225536104203428])
        pos_diff = np.array(pos)-Lego2_pos
        yaw_diff = np.array(yaw)-Lego2_yaw
        self.assertAlmostEqual(pos_diff.dot(pos_diff),0)
        self.assertAlmostEqual(yaw_diff.dot(yaw_diff),0)

    def test_defaultMocapNode(self):
        mcn = MocapNode()
        self.assertTrue(mcn.natnet_packet is not None)
        mcn.stop()

    def test_startAndStop(self):
        mcn = MocapNode()
        mcn.run()
        self.assertTrue(not mcn.dataThread._is_stopped)
        self.assertTrue(not mcn.natnet_client.dataSocket._closed)
        self.assertTrue(not mcn.commandThread._is_stopped)
        self.assertTrue(not mcn.natnet_client.cmdSocket._closed)
        mcn.stop()
        self.assertTrue(mcn.dataThread._is_stopped)
        self.assertTrue(mcn.natnet_client.dataSocket._closed)
        self.assertTrue(mcn.commandThread._is_stopped)
        self.assertTrue(mcn.natnet_client.cmdSocket._closed)


    def test_dump(self):
        # Request a model description message on command socket:
        self.mocap_node.sendRequest(MessageType().RequestModelDef)
        # Dump the message on command buffer
        filename = self.mocap_node.dump("cmd")
        dump_mess = self.__openData(filename[0])
        # Check if the message is correct
        self.assertEqual(dump_mess,self.message_5)
        # Request a frame of data message on data socket:
        self.mocap_node.sendRequest(MessageType().RequestFrameOfData)
        # Dump the message on data buffer and check if the message is correct
        filename = self.mocap_node.dump("data")
        self.assertEqual(self.__openData(filename[0]),self.message_7)
        # Dump several message and test their contents
        filename = self.mocap_node.dump("data",2)
        self.assertEqual(self.__openData(filename[0]),self.message_7)
        self.assertEqual(self.__openData(filename[1]),self.message_7)

    def test_nodetoString(self):
        # Request a model description message on command socket:
        self.mocap_node.sendRequest(MessageType().RequestModelDef)
        # Request a frame of data message on data socket:
        self.mocap_node.sendRequest(MessageType().RequestFrameOfData)
        # Request pose
        pos, rot = self.mocap_node.getPose("Lego2")
        # Generate and check the log message
        logmess = self.mocap_node.to_string()
        lenmess = trace("Test unitaire --- Motion Capture node to String\n" + logmess + "--------- \n")
        self.assertEqual(len(logmess),5586)

if __name__ == '__main__':
        unittest.main(verbosity=2)
