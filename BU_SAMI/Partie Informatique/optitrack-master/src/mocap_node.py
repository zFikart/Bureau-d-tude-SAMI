# coding: utf-8

""" Motion Capture (MoCap) Node

Auteur : Clement FAUVEL
Date : Janvier 2021
"""

from NatNetPacket import *
from Natnet_Client import *
import time
import datetime
import math
from debug import *
from common import *



class MocapNode():
    """ Noeud principal qui gère le client et le protocol NatNet
    
    Attributes:
        natnet_client : le client natnet qui communique avec Motive
        timeout : un seuil de temps maximal pour les communications
        modelInfo : un dictionnaire référencant les legos, leur id et leur index
        isUpdated : un drapeau qui est levé lorsque le dictionnaire est à jour    
    """

    def __init__(self, configType = "DEFAULT", natnet_client=None):
        if natnet_client is None:
            # Si aucun client natnet est donné, le noeud démarre un nouveau noeud en se basant sur le fichier de configuration
            self.natnet_client = NatnetClient.fromConfigType(configType)
        else:
            self.natnet_client = natnet_client
        
        self.natnet_packet = Packet()
        self.dataThread = []
        self.commandThread = []
        self.last_mocap_mess = []
        self.last_modef_mess = []
        self.timeout = 10   # timeout for while functions during tests
        self.modelInfo = dict()
        self.isUpdated = False

    def __wait_for_message(self,bufType="data"):
        """ Retourne le dernier message recu dans le buffer sélectionné.

        Args:
            bufType (str) : Choix du buffer ("data" ou "cmd")
        
        Returns:
            bufmess (bytes) : le message en binaire
        """
        t0 = time.time()
        while time.time() < t0 + self.timeout:
            if bufType == "data":
                bufMess = self.natnet_client.getDataBuffer()
            elif bufType == "cmd":
                bufMess = self.natnet_client.getCmdBuffer()
            else:
                raise ValueError
            if(len(bufMess) > 0):
                break
            else:
                time.sleep(0.1)
        return bufMess


    def __wait_for_mocap(self):
        """ Receptionne un packet de type MoCap
        
        Returns:
            mocap_packet (Packet) : un packet de type MoCap
        """
        # We assume here that motive is running and sending mocap_message    
        bufMess = self.__wait_for_message("data")
        mocap_packet = Packet().fromData(bufMess)
        isMocap = (mocap_packet.messageId == MessageType().FrameOfData)
        t0 = time.time()
        while (not isMocap) and (time.time() < t0 + self.timeout):
            self.sendRequest(MessageType().RequestFrameOfData)
            bufMess = self.__wait_for_message("data")
            mocap_packet = Packet().fromData(bufMess)
            isMocap = (mocap_packet.messageId == MessageType().FrameOfData)        
        if not isMocap:
            raise ValueError("No mocap data has been received by the client")

        return mocap_packet

    def sendRequest(self,messType):
        """ Envoi une requète au logiciel Motive

        Args:
            messType (MessageType()) : le type de message à envoyer
        """
        self.natnet_packet = Packet().getCmdPacket(messType)
        self.natnet_client.sendCommand(self.natnet_packet.packetToData())

    def updateModelInfo(self):
        """ Demande la description du modèle au serveur.
        Les informations sont décryptées et stockées dans un dictionnaire. Ce dernier est retourné par le programme.

        Returns:
            modelInfo (dict) : le dictionnaire définissant l'identifiant et l'index mémoire des robots
        """
        isModelDescription = False        
        t0 = time.time()
        while not isModelDescription and time.time() < t0 + self.timeout:
            # Request model description
            self.sendRequest(MessageType().RequestModelDef)
            # Receive and decode message
            bufMess = self.__wait_for_message("cmd")
            self.natnet_packet = Packet().fromData(bufMess)
            if self.natnet_packet.messageId == MessageType().ModelDef:
                isModelDescription = True

        self.last_modef_mess, offset = self.natnet_packet.decode()
         # Update model info store as a dictionary where the key refer to rigid body name,
         # and the value to the tuple (id,idx) with idx the position in the description list
        idx = 0
        for rgb in self.last_modef_mess.rgbDescription:
            self.modelInfo[rgb.name.decode('utf-8')] = (rgb.bodyId, idx)
            idx += 1
        # Check if the model has been updated
        if idx > 0: 
            trace("Model info has been updated with {} new rigid bodies".format(idx+1))
            self.isUpdated = True
        else: trace("Error, the model info has not been updated")
        return self.modelInfo


    def __getMocapMess(self):
        """ Receptionne et décode un packet de type MoCap
        
        Returns:
            mocap_mess : un message mocap decode
            offset : la position de l'offset
        """
        # Check if model info has been updated, otherwise do it
        while not self.isUpdated:
            self.updateModelInfo()
        # Wait for Mocap packet
        self.natnet_packet = self.__wait_for_mocap()
        # Decode packet
        return self.natnet_packet.decode()


    def getPose(self,name:str) -> tuple:
        """ Retourne la pose 3D d'un Lego
        Args:
            name (String) : le nom du Lego
        Returns:
            pos : un vecteur de position en [m]
            rot : un quaternion représentant l'orientation
        """
        # Get a Mocap decoded message
        self.last_mocap_mess, offset = self.__getMocapMess()

        # Get rigidbody position and orientation
        (rgb_id, rgb_idx) = self.modelInfo[name]
        if not rgb_id == self.last_mocap_mess.rigidBodies[rgb_idx].bodyId:
            raise ValueError
        pos = self.last_mocap_mess.rigidBodies[rgb_idx].pos
        rot = self.last_mocap_mess.rigidBodies[rgb_idx].rot

        # Return the pose as a tuple (pos,rot)
        return (pos,rot)


    def getPos2DAndYaw(self,name:str) -> tuple:
        """ Retourne la position 2D et le yaw d'un Lego
        Args:
            name (String) : le nom du Lego
        Returns:
            pos (Float2()): un vecteur de position de  taille 2 en [m]
            yaw (Float1(): un float représentant l'orientation
        """
        # Obtient la pose du Lego avec méthode getPose()
        pos, rot = self.getPose(name)
        # Effectue un changement de repère (facultatif)
        npos = position_motive_to_sami(pos)
        yaw = yaw_from_orientation(rot)
        return ([npos[0],npos[1]],[yaw])
    
    
    def run(self):
        """ Démarre le noeud Mocap

        Il s'agit de la première fonction à appeler une fois l'objet Mocap_node créé.
        Elle démarre le client natnet.
        """
        self.dataThread, self.commandThread = self.natnet_client.startListeningFromSockets()

    def stop(self):
        """ Stop le noeud Mocap
        Cette fonction est appelé en fin de programme. Elle clos les connexions du client avec le serveur.
        """
        self.natnet_client.stopListeningFromSockets(self.dataThread,self.commandThread)


    def dump(self,bufType,n=1,fname="dump_mess"):
        """ Sauvegarde les n dernières trames recues dans des fichiers binaires

        Les fichier sont automatiquement numérotés et nommés en fonction de la date et du type de message prélévé

        Args:
            bufType (str) : Choix du buffer ("data" ou "cmd")
            n (int) : nombre de trames à sauvegarder [n=0]

        Returns:
            filename (str) : liste des noms des fichiers créés
        """
        i=0
        file_name = []
        while i<n:
            # Get the last message in the concerned buffer
            bufMess = self.__wait_for_message(bufType)
            natnet_packet = Packet().fromData(bufMess)
            data = natnet_packet.packetToData()
            # Prepare file name
            ts = time.time()
            sttime = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d - ')    
            file_name.append("{}{}_{}_{}.bin".format(sttime,fname,natnet_packet.messageId,i))
            # Sauvegarde la trame dans le fichier
            fh = open(file_name[i],"wb")
            fh.write(data)
            fh.close()
            # Incremente i
            i += 1
        return file_name

    def to_string(self):
        logmess = ""
        logmess += self.title_center("Informations du socket Natnet", 60, "=") + "\n"
        logmess += " Informations du socket Natnet ".center(60, "=") + "\n"
        logmess += self.natnet_client.to_string()
        logmess += "Processus (thread)\n"
        logmess += "\t Ecoute des donnees : {}\n".format("running" if not self.dataThread == [] and self.dataThread.is_alive() else "stop")
        logmess += "\t Ecoute des commandes : {}\n".format("running" if not self.commandThread == [] and self.commandThread.is_alive() else "stop")
        logmess += "---- Informations contenues dans le paquet ----\n"
        logmess += self.natnet_packet.to_string()
        logmess += "Description du modele : {}a jour\n".format("" if self.isUpdated else "pas ")
        if(self.isUpdated):
            logmess += "Dictionnaire (nom_lego : (id,index)) : \n{}\n".format('\n'.join("(%s: %s)" % item for item in self.modelInfo.items()))
        
        logmess += "---- Dernier message decode de type MODELDEF ----\n"
        if (isinstance(self.last_modef_mess,DescriptionMessage)):
            logmess += self.last_modef_mess.to_string()
        else:        
            logmess += "AUCUN\n"
        logmess += "---- Dernier message decode de type FRAMEOFDATA ----\n"
        if (isinstance(self.last_mocap_mess,MocapMessage)):
            logmess += self.last_mocap_mess.to_string()
        else:        
            logmess += "AUCUN\n"

        return logmess
    
    def title_center(self, title:str, length:int, symbol:str) -> str:
        return f" {title} ".center(length, symbol)
