# coding: utf-8

""" Tests unitaires pour le protocole Natnet (message, paquet, description)

Auteur : Clement FAUVEL
Date : Janvier 2021
"""

import unittest
import sys, os
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'src'))
from NatNetPacket import *
from debug import *


class TestMessageType(unittest.TestCase):
    def test_messageType(self):
        self.assertEqual(MessageType().Connect,0)
        self.assertEqual(MessageType().RequestModelDef,4)
        self.assertEqual(MessageType().ModelDef,5)
        self.assertEqual(MessageType().FrameOfData,7)


    def test_getmessageDefinition(self):
            allDef = getMessageDefinition()
            self.assertIsInstance(allDef,dict)
            ConnectDef = getMessageDefinition(0)
            self.assertEqual(ConnectDef,'Connect')
            ModelDef = getMessageDefinition(5)
            self.assertEqual(ModelDef,'ModelDef')
            ErrIdDef = getMessageDefinition(12)
            self.assertEqual(ErrIdDef,'Key is not found')


class TestPacket(unittest.TestCase):
    def setUp(self):
        self.data = self.__openData("Tests/streamData/RigidBody20210112.bin")
        self.packet = Packet.fromData(self.data)
        self.resizePacket = self.packet.resize(self.packet.packetSize)

    def __openData(self,path):
        fh = open(path,"rb")
        bh = bytes(fh.read())
        fh.close()
        return bh

    def test_PacketFromData(self):
        self.assertEqual(self.packet.messageId,7)
        self.assertEqual(self.packet.packetSize,192)
        self.assertIsInstance(self.packet.data,bytes)

    def test_PacketToData(self):
        data = self.resizePacket.packetToData()
        self.assertEqual(data,self.data[0:192])

    def test_resizePacket(self):
        status = self.packet.isPacket()
        self.assertFalse(status)
        status = self.resizePacket.isPacket()
        self.assertTrue(status)

    

    
class TestDecodeMessages(unittest.TestCase):
    def setUp(self):
        self.data = self.__openData("Tests/streamData/RigidBody20210112.bin")
        self.packet = Packet.fromData(self.data).resize(192)

    def __openData(self,path):
        fh = open(path,"rb")
        bh = bytes(fh.read())
        fh.close()
        return bh

    def test_decodePacket(self):
        data = self.__openData("Tests/streamData/RigidBody20210112.bin")
        packet = Packet.fromData(self.data).resize(192)
        message, offset = packet.decode()
        # On vérifie que le pointer a parcouru toute la trame
        self.assertEqual(offset,self.packet.packetSize)

    def test_unpackMocap(self):
        data = self.__openData("Tests/streamData/sample_7.bin")
        packet = Packet.fromData(data)        
        message, offset = packet.decode()       
        # Check if the message contains 3 rigidbodies
        self.assertEqual(len(message.rigidBodies),3)
        # Check if the second rigidbody has correct values
        rigidBody = message.rigidBodies[1]
        self.assertEqual(rigidBody.bodyId,2)
        self.assertTrue(rigidBody.isTrackingValid)

    def test_unpackDescription(self):
        data = self.__openData("Tests/streamData/sample_5.bin")
        packet = Packet.fromData(data)        
        message, offset = packet.decode()
        # Check if rigidbody description is correct
        rgbDescript = message.rgbDescription[1]
        self.assertEqual(rgbDescript.name,b"Lego2") 
        self.assertEqual(rgbDescript.bodyId,2)
        # Check if marker set description is correct
        mrkSetDescript = message.mrkSetDescription[3]
        self.assertEqual(mrkSetDescript.name,b"all")
        self.assertEqual(mrkSetDescript.markers[0].name,b"Lego3_1")        
        
    def test_getCmdPacket(self):
        packet = Packet.getCmdPacket(MessageType().RequestModelDef,"Wrong instruction")
        self.assertEqual(packet.messageId,4)
        self.assertEqual(packet.packetSize, 5)
        self.assertEqual(packet.data, b"\0")
        packet = Packet.getCmdPacket(MessageType().Request,"Instruction")
        self.assertEqual(packet.messageId,2)
        self.assertEqual(packet.packetSize, 16)
        self.assertEqual(packet.data, b"Instruction\0")
        packet = Packet.getCmdPacket(MessageType().Connect)
        self.assertEqual(packet.messageId,0)
        self.assertEqual(packet.packetSize, 9)
        self.assertEqual(packet.data, b"Ping\0")

    def test_ModelDescriptiontoString(self):
        # Charge un message de type description de modèles
        data = self.__openData("Tests/streamData/sample_5.bin")
        packet = Packet.fromData(data)        
        message, offset = packet.decode()
        # Gènere et vérifie partiellement la chaine de caractères produite par les méthodes to_string()
        logmess = message.mrkSetDescription[0].to_string()
        self.assertEqual(logmess[0:],"Markerset Name: Lego3\n")
        logmess = message.mrkSetDescription[0].markers[0].to_string()
        self.assertEqual(logmess[0:],"\tMarker Name: Marker1\n")
        logmess = message.rgbDescription[0].to_string()
        self.assertEqual(logmess[0:21],"RigidBody Name: Lego3")
        # Vérifie la chaine de caractère complete
        logmess = message.to_string()
        lenmess = trace("Test unitaire --- Model Description to String\n" + logmess + "--------- \n")
        self.assertEqual(len(logmess),1698)

    def test_MocaptoString(self):
        # Charge un message de type FRAMEOFDATA
        data = self.__openData("Tests/streamData/sample_7.bin")
        packet = Packet.fromData(data)        
        message, offset = packet.decode()
        # Gènere et vérifie partiellement la chaine de caractères produite par les méthodes to_string()
        logmess = message.rigidBodies[0].to_string()
        self.assertEqual(logmess[0:16],"\tRigidBody ID: 3")       
        logmess = message.markerSets[0].to_string()
        self.assertEqual(logmess[0:23],"\tMarker Set Name: Lego3")
        logmess = message.markerSets[0].markers[0].to_string()
        self.assertEqual(logmess[0:10],"\t\tMarker :")
        logmess = message.timeInfos.to_string()
        self.assertEqual(logmess[0:10],"\tTimeCode:")  
        logmess = message.latencyInfos.to_string()
        self.assertEqual(logmess[0:29],"\tstampCamExpo: 9309248849218\n")
        logmess = message.frameParam.to_string()
        self.assertEqual(logmess[0:20],"\tis recording: False")
        # Vérifie la chaine de caractère complete
        logmess = message.to_string()
        lenmess = trace("Test unitaire --- Mocap to String\n" + logmess + "--------- \n")
        self.assertEqual(len(logmess),3105)

    def test_PackettoString(self):
        # Charge un message (quelconque)
        data = self.__openData("Tests/streamData/sample_7.bin")
        packet = Packet.fromData(data)
        # Gènere et vérifie la chaine de caractères produite
        logmess = packet.to_string()
        self.assertEqual(logmess,"Message ID: 7\nPacket Size: 518\nPacket status: Not been decoded yet\nDecoded Bytes: 518/518\n")
        # Vérifie que le status change après decodage 
        message, offset = packet.decode()
        logmess = packet.to_string()
        self.assertEqual(logmess,"Message ID: 7\nPacket Size: 518\nPacket status: Fully decoded\nDecoded Bytes: 518/518\n")
        lenmess = trace("Test unitaire --- Packet to String\n" + logmess + "--------- \n")
        


if __name__ == '__main__':
        unittest.main(verbosity=2)