# coding: utf-8

""" Natnet Client socket

Auteur : Clement FAUVEL
Date : Janvier 2021
"""

import socket
from threading import Thread
import queue
import configparser


class NatnetClient():
    """ Client Natnet ouvrant la communication avec le serveur Motive

    Attributes:
        serverIPAddress (str) : adresse du serveur
        localIPAddress (str) : adresse local du client
        multicastAddress (str) : adresse du multicast
        srvCmdPort (int) : port du serveur pour les requètes
        cltDataPort (int) : port du client pour les données
        cltCmdPort (int) : port du client pour les requètes (envoi et reception)
        cmd_queue (queue) : buffer contenant les dernières trames reçues sur le port de requete
        data_queue (queue) : buffer contenant les dernières trames reçues sur le port de donnée
        max_buff_len (int) : nombre maximal de messages conservé dans la queue
    """

    # Construct a NatnetClient object
    def __init__( self, serverIPAddress = "100.64.212.150",\
        localIPAddress = "100.64.212.156", multicastAddress = "225.1.1.1", \
        srvCmdPort = 1510, cltDataPort = 1511, max_buff_len = 2):
        # Change this value to the IP address of the NatNet server.
        self.serverIPAddress = serverIPAddress
        # Change this value to the IP address of your local network interface
        self.localIPAddress = localIPAddress
        # This should match the multicast address listed in Motive's streaming settings.
        self.multicastAddress = multicastAddress
        # NatNet Command channel
        self.srvCmdPort = srvCmdPort        
        # NatNet Data channel
        self.cltDataPort = cltDataPort
        # Use any available port for command socket
        self.cltCmdPort = 0
        # Declare queues to stock cmd and data messages
        self.cmd_queue = queue.Queue(max_buff_len)
        self.data_queue = queue.Queue(max_buff_len)
        self.max_buff_len = max_buff_len
        # Setup sockets
        self.__initSockets()


    @classmethod
    def fromConfigType(cls,configType):
        config = configparser.ConfigParser()
        config.read("config.ini")
        srvAddr = config[configType].get('srvaddr')
        srvPort  = config[configType].getint('srvport')
        cltAddr = config[configType].get('cltaddr')
        cltDataPort = config[configType].getint('cltdataport')
        multcastaddr = config[configType].get('multcastaddr')
        cltCmdPort = config[configType].getint('cltcmdport')
        return cls(srvAddr,cltAddr,multcastaddr,srvPort,cltDataPort)

    
    def __createCommandSocket( self ):
        """Create a command socket to attach to the broadcast stream

        Returns:
            cmdSocket (socket) : le socket pour communiquer les requètes
        """
        self.cmdSocket = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )        
        # Set command socket options:
        self.cmdSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)        
        # Bind to any free port on localhost and store its value as class attribute
        self.cmdSocket.bind( ('', self.cltCmdPort) )
        self.cltCmdPort = self.cmdSocket.getsockname()[1]
        # Allow broadcast
        self.cmdSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        return self.cmdSocket

    
    def __createDataSocket( self, port ):
        """Create a data socket to attach to the broadcast stream

        Args:
            port (int) : le numéro de port pour le socket de donnée

        Returns:
            cmdSocket (socket) : le socket pour communiquer les requètes
        """
        # Open a socket
        self.dataSocket = socket.socket( socket.AF_INET,     # Internet
                              socket.SOCK_DGRAM,
                              socket.IPPROTO_UDP)    # UDP
        # Allow reuse of IP
        self.dataSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Subscribe to the multicast channel       
        self.dataSocket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(self.multicastAddress) + socket.inet_aton(self.localIPAddress))
        # Bind to local IP Address on the data port
        self.dataSocket.bind( (self.localIPAddress, port) )
        return self.dataSocket

    def __processMessage(self, socket, data):
        """ Méthode appelée lorsqu'un message est reçu

        Stocke la trame reçue dans le buffer correpondant

        Args:
            socket (socket): le socket ayant reçu la trame
            data (bytes): la trame
        """
        socket_port = socket.getsockname()[1]
        if(socket_port==self.cltCmdPort):
            if self.cmd_queue.full() :
                self.cmd_queue.get()            
            self.cmd_queue.put(data)
        elif (socket_port==self.cltDataPort):
            if self.data_queue.full() :
                self.data_queue.get()
            self.data_queue.put(data)
        pass

    def __dataThreadFunction( self, socket ):
        """ Processus d'écoute pour un socket
        Args:
            socket (socket) : le socket auquel le processus est attaché
        """
        while True:
            # Block for input
            try:
                data, addr = socket.recvfrom( 32768 ) # 32k byte buffer size
                if( len( data ) > 0 ):
                    self.__processMessage( socket, data )
            except:
                break

    def __initSockets(self):
        """ Initiate the command and data sockets
        """
        # Create the command socket
        self.commandSocket = self.__createCommandSocket()
        if( self.commandSocket is None ):
            print( "Could not open command channel" )
            exit

        # Create the command socket
        self.dataSocket = self.__createDataSocket( self.cltDataPort )
        if( self.dataSocket is None ):
            print( "Could not open command channel" )
            exit
        

    
    def __closeSockets(self):
        """ Try to close sockets
        """
        try:
            self.commandSocket.close()
        except AttributeError:
            pass
        try:
            self.dataSocket.close()
        except AttributeError:
            pass

    def startListeningFromSockets(self):
        """ Initialise puis démarre l'écoute pour le socket de donnée et de requète

        Cette fonction est appelée en première lors de l'usage d'un client natnet

        Returns:
            dataThread (thread) : le processus attaché au socket de donnée
            commandThread (thread) : le proccessus attaché au socket de requète
        """
        # Create a separate thread for receiving data packets
        dataThread = Thread( target = self.__dataThreadFunction, args = (self.dataSocket, ))
        dataThread.start()

        # Create a separate thread for receiving command packets
        commandThread = Thread( target = self.__dataThreadFunction, args = (self.commandSocket, ))
        commandThread.start()

        # Return threads
        return dataThread, commandThread

    def stopListeningFromSockets(self, dataThread, commandThread):
        """ Termine proprement le socket de donnée et celui de commande

        Débranche les sockets puis termine les processus

        Args:
            dataThread (thread) : le processus attaché au socket de donnée
            commandThread (thread) : le proccessus attaché au socket de requète
        """
        # Close sockets
        self.__closeSockets()
        #Terminate threads
        if isinstance(dataThread,Thread):
            dataThread.join()
        if isinstance(commandThread,Thread):
            commandThread.join()


    def sendCommand(self,data, socket=None, address=None):
        """ Envoi une requète au serveur

        Args:
            socket (socket): le socket à partir duquel envoyé la demande.
                     Par défaut, il s'agira du socket de requète
            address (tuple) : l'adresse du serveur.
                     Par défaut, il utilise l'adresse et le port en attribut
        """
        # Set default parameter from attributs
        if socket is None:
            socket = self.cmdSocket
        if address is None:
            address = (self.serverIPAddress,self.srvCmdPort)
        # Encode data then send
        socket.sendto(data,address)

    def getCmdBuffer(self,idx = 0):
        """ Retourne la trame contenu dans le buffer de requètes

        Args:
            idx [=0] (int) : index du message dans la queue, le premier étant idx=0
        
        Returns:
            data (bytes) : le message
        """
        list_mess = list(self.cmd_queue.queue)
        if idx > len(list_mess)-1:
            return b''
        else:
            return list_mess[-1-idx]

    def getDataBuffer(self,idx = 0):
        """ Retourne la trame contenu dans le buffer de données

        Args:
            idx [=0] (int) : index du message dans la queue, le premier étant idx=0
        
        Returns:
            data (bytes) : le message
        """
        list_mess = list(self.data_queue.queue)
        if idx > len(list_mess)-1:
            return b''
        else:
            return list_mess[-1-idx]


    def to_string(self):
        logmess = ""
        logmess += "Serveur Natnet (Motive)\n"
        logmess += "\tAdresse : {}\n".format(self.serverIPAddress)
        logmess += "\tMulticast : {}\n".format(self.multicastAddress)
        logmess += "\tPort de commande : {}\n".format(self.srvCmdPort)
        logmess += "Client Natnet (PC)\n"
        logmess += "\tAdresse : {}\n".format(self.localIPAddress)
        logmess += "\tSocket de donnees (status, port): ({}, {})\n".format("ferme" if self.dataSocket._closed else "ouvert",self.cltDataPort)
        logmess += "\tSocket de commande (status, port): ({}, {})\n".format("ferme" if self.commandSocket._closed else "ouvert",self.cltCmdPort)
        logmess += "Etat des queues (taille / taille_max)\n"
        logmess += "\tDonnee : ({}/{})\n".format(self.data_queue.unfinished_tasks , self.max_buff_len)
        logmess += "\tCommande : ({}/{})\n".format(self.cmd_queue.unfinished_tasks , self.max_buff_len)
        return logmess

