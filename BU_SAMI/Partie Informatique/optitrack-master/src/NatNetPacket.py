# coding: utf-8

""" Natnet Packets

Auteur : Clement FAUVEL
Date : Janvier 2021
"""

from debug import trace
from NatNetMessages import MocapMessage, DescriptionMessage


class Packet():
    """ Image d'un paquet codifié selon le protocole Natnet

    Attributes:
        messageId (int) : Identifiant du type de message
        packetSize (int) : taille du paquet incluant les 4 premiers bytes
        data (bytes) : message transporté

    """
    def __init__(self,messageId=-1,packetSize=0,data=b''):
        self.messageId = messageId
        self.packetSize = packetSize
        self.data = data
        self.status = 0
        self.missingBytes = 0

    @classmethod
    def fromData(cls,data):
        """ Construit un paquet à partir d'une trame binaire

        Args:
            data (bytes) : la trame en binaire
        
        Returns:
            packet (Packet) : l'objet paquet
        """
        messageId = int.from_bytes( data[0:2], byteorder='little' )
        packetSize = int.from_bytes( data[2:4], byteorder='little' )
        data = data[4:]
        return cls(messageId,packetSize,data)

    @classmethod
    def getCmdPacket(cls,messageId,CmdStr = ""):
        """ Construit un paquet requête à partir de son identifiant et d'un message optionnel

        Args:
            messageId (MessageType) : l'identifiant du message
            CmdStrg [""] : un message (optionnel)
        
        Returns:
            packet (Packet) : le paquet requete
        """
        if (messageId == MessageType().RequestFrameOfData 
            or messageId == MessageType().RequestModelDef):
            data = "".encode('utf-8')
        elif (messageId == MessageType().Request):
            data = CmdStr.encode('utf-8')
        elif (messageId == MessageType().Connect):
            data = "Ping".encode('utf-8')
        else:
            raise ValueError("This message id does not exist or have not been implemented yet")
        data += b"\0"
        return cls(messageId,len(data)+4,data)        


    def isPacket(self):
        """ Teste si le paquet est bien de type natnet [A REVOIR]

            Returns:
                isPacket (Bool)
        """
        return (len(self.data)==self.packetSize-4) & (self.data[-1:] == b"\x00")

    def resize(self,max_length):
        """ Redimensionne le message d'un paquet

        Args:
            max_length : nombre maximale de bytes que doit contenir le message

        Returns:
            newPacket (Packet) : le paquet redimensionné
        """
        data = self.data[0:self.packetSize-4]
        return Packet(self.messageId, self.packetSize,data)

    def packetToData(self):
        """ Gènere une trame binaire à partir d'un objet Packet()

        Returns:
            data (bytes) : la trame binaire
        """
        if not self.isPacket():
            trace('[packetToData] : This packet is not a truely Packet object: Check data size')

        data = self.messageId.to_bytes(2,byteorder='little')
        data += self.packetSize.to_bytes(2,byteorder='little')
        data += self.data
        return data

    def decode(self):
        """ Décode le message contenu dans un paquet

        Returns:
            message (NatNetMessage) : le message Natnet décodé
            offset (int) : l'index du dernier byte décodé
        """
        try:
            offset = 4
            # unpack Mocap data
            if(self.messageId == MessageType().FrameOfData):
                # unpack Mocap data
                message = MocapMessage()
                offset += message.unpackMocapData(self.data)
            elif(self.messageId == MessageType().ModelDef):
                # update data model
                message = DescriptionMessage()
                offset += message.unpackDescript(self.data)
        except:
            self.status = -1
        # Check if packet is fully or partially decoded        
        self.missingBytes = self.packetSize -  offset   
        if(self.missingBytes == 0):     
            self.status = 2 # Packet has been correctly decoded
        else:
            self.status = 1 # Packet has not been completly decoded            
        return message, offset

    def to_string(self):
        logmess = "Message ID: {}\n".format(self.messageId)
        logmess += "Packet Size: {}\n".format(self.packetSize)
        logmess += "Packet status: "
        if(self.status == 2): logmess += "Fully decoded\n"
        if(self.status == 1): logmess += "Partially decoded\n"
        if(self.status == 0): logmess += "Not been decoded yet\n"
        if(self.status == -1): logmess += "Error\n"
        logmess += "Decoded Bytes: {}/{}\n".format(self.packetSize-self.missingBytes,self.packetSize)
        return logmess


class MessageType():
    """ Classe portant les types de message Natnet et leur identifiant

    Attributes: 
        Connect : Request for server info
        ServerInfo : Motive version, NatNet version, clock frequency, data port, and multicast address
        Request : Request server to immediately respond with its current time (used for clock sync)
        Response : Current server time (and time contained in EchoRequest message)
        RequestModelDef : equest for model definitions
        ModelDef : List of definitions of rigid bodies, markersets, skeletons etc
        RequestFrameOfData : ???
        FrameOfData : Frame of motion capture data
        MessageString : ???
        Disconnect : ???
        UnrecognizedRequest : Uncorrect message has been received by server
        Undefined = 999999 : ???
    """
    def __init__(self):
        self.Connect = 0
        self.ServerInfo = 1
        self.Request = 2
        self.Response = 3
        self.RequestModelDef = 4
        self.ModelDef = 5
        self.RequestFrameOfData = 6
        self.FrameOfData = 7
        self.MessageString = 8
        self.Disconnect = 9
        self.UnrecognizedRequest = 100
        self.Undefined = 999999

def getMessageDefinition(id=None):
    """ Récupère le nom d'un attribut à partir d'un identifiant de message

    Lorsqu'aucun identifiant est donné en argument, 
    la méthode renvoit la liste des attributs et leur valeur 
    sous la forme d'un dictionnaire

    Returns:
        key : le nom de l'attribut ou le dictionnaire

    """
    messDict = vars(MessageType())
    if id is None:
        return messDict
    else:   
        for key, value in messDict.items():
            if id == value:
                return key
    return 'Key is not found'

def printMessageDefinition():
    """ Affiche la liste des attributs et leurs valeurs dans la console
    """
    messDict = getMessageDefinition()
    print(''.join("(%s: %s)\n" % item for item in messDict.items()))





