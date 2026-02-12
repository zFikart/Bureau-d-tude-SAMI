# coding: utf-8

""" Natnet Data Models

Auteur : Clement FAUVEL
Date : Janvier 2021
"""


import struct
from debug import trace

# Create structs for reading various object types to speed up parsing.
Vector3 = struct.Struct( '<fff' )
Quaternion = struct.Struct( '<ffff' )
FloatValue = struct.Struct( '<f' )
DoubleValue = struct.Struct( '<d' )


class MarkerDescription():
    """ Description des marqueurs

    Attributes:
        name (str) : Nom du marqueur

    """
    def __init__(self,name =""):
        self.name = name

    def unpack(self,data):
        """ Décode le message binaire pour une description de marqueur

        Args:
            data (bytes) : le message
        
        Returns:
            offset (int) : l'index du dernier byte décodé
        """
        offset = 0
        # Nom du marqueur
        self.name, separator, remainder = bytes(data[offset:]).partition( b'\0' )
        offset += len( self.name ) + 1
        return offset
    
    def to_string(self):
        return  "\tMarker Name: {}\n".format(self.name.decode( 'utf-8' ))


class MarkerSetDescription():
    """ Description d'un groupe de marqueurs

    Attributes:
        name (str) : Nom du groupe
        markerCount (int): Nombre de marqueurs dans le groupe
        markers (MarkerDescription()) : Liste des marqueurs

    """
    def __init__(self,name ="", markerCount = 0, markers = None):
        self.name = name
        self.markerCount = markerCount
        if markers is None:
            self.markers = []
        else:
            self.markers = markers
        
    def unpack(self,data):
        """ Décode le message binaire pour une description de groupe de marqueurs

        Args:
            data (bytes) : le message
        
        Returns:
            offset (int) : l'index du dernier byte décodé
        """
        offset = 0
        # Nom du groupe de marqueurs
        self.name, separator, remainder = bytes(data[offset:]).partition( b'\0' )
        offset += len( self.name ) + 1
        # Nombre de marqueurs dans le groupe
        self.markerCount = int.from_bytes( data[offset:offset+4], byteorder='little' )
        offset += 4
        # Décode la description de chaque marqueur
        for i in range( 0, self.markerCount ):            
            self.markers.append(MarkerDescription())
            offset += self.markers[i].unpack(data[offset:])
        return offset
    
    def to_string(self):
        return  "Markerset Name: {}\n".format(self.name.decode( 'utf-8' ))

class RigidBodyDescription():
    """ Description des corps rigides

    Attributes:
        name (str) : Nom du corps
        bodyId (int) : Identifiant du corps
        parentId (int) : Identifiant du corps parent (O si nul)
        parentOffset (Vector3()) : Offset entre le pivot du corps et celui de son parent
        markerCount (int) : nombre de marqueurs dans le corps
        markerOffser(Vector3()) : Offset de chaque marqueur par rapport au pivot
        markerActive(Bool) : Etat du marqueur (actif ou non)
    """
    def __init__(self, name = "", bodyId = 0, parentId = 0, parentOffset = [0.,0.,0.], \
                markerCount = 0, markerOffset = None, markerActive = None):
        self.name = name
        self.bodyId = bodyId
        self.parentId = parentId
        self.parentOffset = parentOffset
        self.markerCount = markerCount
        if markerOffset is None:
            self.markerOffset = []
        else:
            self.markerOffset = markerOffset
        if markerActive is None:
            self.markerActive = []
        else:
            self.markerActive = markerActive
        

    def unpack(self,data):
        """ Décode le message binaire pour une description de corps rigide

        Args:
            data (bytes) : le message
        
        Returns:
            offset (int) : l'index du dernier byte décodé
        """
        offset = 0
        # Name (Version 2.0 or higher)
        self.name, separator, remainder = bytes(data[offset:]).partition( b'\0' )
        offset += len( self.name ) + 1
        #Rigid body unique id
        self.bodyId = int.from_bytes( data[offset:offset+4], byteorder='little' )
        offset += 4
        # Id du corp parent
        self.parentId = int.from_bytes( data[offset:offset+4], byteorder='little' )
        offset += 4
        #Décallage par rapport au corps parent
        self.parentOffset = Vector3.unpack( data[offset:offset+12] )
        offset += 12
        # RigidBody markers (Version 3.0 and higher)
        self.markerCount = int.from_bytes( data[offset:offset+4], byteorder='little' ) 
        offset += 4
        # Décalage des marqueurs p/r au pivot + label si actif
        markerCountRange = range( 0, self.markerCount )
        for i in markerCountRange:
            self.markerOffset.append(Vector3.unpack(data[offset:offset+12]))
            offset +=12                
        for i in markerCountRange:
            self.markerActive.append(int.from_bytes(data[offset:offset+4],byteorder = 'little'))
            offset += 4
        return offset

    def to_string(self):
        logmess = "RigidBody Name: {}\n".format(self.name.decode( 'utf-8' ))
        logmess += "\tUnique Id: {}\n".format(self.bodyId)
        logmess += "\tparent ID: {}\n".format(self.parentId)
        logmess += "\tOffset parent: {}\n".format(self.parentOffset)
        logmess +=  "\tMarker Count: {}\n".format(self.markerCount)
        markerCountRange = range( 0, self.markerCount )
        for i in markerCountRange:
            logmess +=  "\t\t MarkerOffset: {}\n".format(self.markerOffset[i])        
        for i in markerCountRange:
            logmess +=  "\t\t ActiveLabel: {}\n".format(self.markerActive[i])
        return logmess

class SkeletonDescription():
    """ Description des corps rigides

    Attributes:
        name (str) : Nom du corps
        skltId (int) : Identifiant du squelette
        rigidBodyCount (int) : nombre de corps dans le squelette
        rigidBodies(rigidBodies()) : Liste d'objet de type rigidBodies()
    """
    def __init__(self,name="",skltId=0, rigidBodyCount=0, rigidBodies = None):
        self.name = name
        self.skltId = skltId
        self.rigidBodyCount = rigidBodyCount
        if rigidBodies is None:
            self.rigidBodies = []
        else:
            self.rigidBodies = rigidBodies

    def unpack(self,data):
        """ Décode le message binaire pour une description de squelette

        Args:
            data (bytes) : le message
        
        Returns:
            offset (int) : l'index du dernier byte décodé
        """
        offset = 0
        # Skeleton name
        self.name, separator, remainder = bytes(data[offset:]).partition( b'\0' )
        offset += len( name ) + 1
        # Skeleton unique ID
        self.skltId = int.from_bytes( data[offset:offset+4], byteorder='little' )
        offset += 4
        # Nombre de corps rigide dans le squelette
        rigidBodyCount = int.from_bytes( data[offset:offset+4], byteorder='little' )
        offset += 4
        # Liste des corps rigides
        for i in range( 0, rigidBodyCount ):
            rbDescript = RigidBodyDescription()
            offset += rbDescript.unpack(data[offset:])            
            self.rigidBodies.append(rbDescript)
        return offset

    def to_string(self):
        logmess =  "Skeleton Name: {}\n".format(self.name.decode('utf-8'))
        logmess += "\tSkeleton Id: {}\n".format(self.name.decode('utf-8')) 
        return logmess

class Marker():
    """ Description des marqueurs

    Les coordonnées sont données dans le repère de Motive

    Attributes:
        x (float) : position en mm sur l'axe x
        y (float) : position en mm sur l'axe y
        z (float) : position en mm sur l'axe z
    """
    def __init__(self,x=0.,y=0.,z=0.):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def unpack(self,data):
        """ Décode le message binaire pour un marqueur

        Args:
            data (bytes) : le message
        
        Returns:
            offset (int) : l'index du dernier byte décodé
        """
        offset = 0
        return offset

    def to_string(self):
        logmess = "\t\tMarker : {},{},{}\n".format(self.x,self.y,self.z)
        return logmess

class RigidBody():
    """ Données d'un corps rigide

    Attributes:        
        bodyId (int) : Identifiant du corps
        pos (Vector3) : Position du corps dans le repère de Motive
        rot (Quaternion) : Orientation du corp en quaternion
        markerError (float) : Erreur de localisation
        isTrackingValid (Bool) : Etat de la fonction de suivi sous Motive
    """
    def __init__(self,bodyId=0, pos = [0.,0.,0.], rot = [0.,0.,0.,0.], markerError = 0., isTrackingValid = False):
        self.bodyId = bodyId
        self.pos = pos
        self.rot = rot
        self.markerError = float(markerError)
        self.isTrackingValid = isTrackingValid

    def unpack(self,data):
        """ Décode le message binaire pour un corps rigide

        Args:
            data (bytes) : le message
        
        Returns:
            offset (int) : l'index du dernier byte décodé
        """
        offset = 0

        # ID (4 bytes)
        self.bodyId = int.from_bytes( data[offset:offset+4], byteorder='little' )
        offset += 4

        # Position and orientation
        self.pos = Vector3.unpack( data[offset:offset+12] )
        offset += 12
        self.rot = Quaternion.unpack( data[offset:offset+16] )
        offset += 16

        # Marker error
        self.markerError = FloatValue.unpack( data[offset:offset+4] )
        offset += 4

        # Tracking Valid
        param, = struct.unpack( 'h', data[offset:offset+2] )
        self.isTrackingValid = ( param & 0x01 ) != 0
        offset += 2
        return offset

    def to_string(self):
        logmess =  "\tRigidBody ID: {}\n".format(self.bodyId)
        logmess += "\t\tPosition: {},{},{}\n".format(*self.pos)
        logmess += "\t\tOrientation: {},{},{}\n".format(*self.rot)
        logmess += "\t\tMarker Error: {}\n".format(self.markerError)
        logmess += "\t\tTracking Valid: {}\n".format('True' if self.isTrackingValid else 'False') 
        return logmess

class MarkerSet():
    """ Données d'un groupe de marqueurs

    Attributes:        
        name (str) : nom du groupe
        markerCount(int) : nombre de marqueurs
        marker (Marker) : Liste de marqueurs
    """
    def __init__(self,name = "", markerCount = 0, markers = None):
        self.name = name
        self.markerCount = markerCount
        if markers is None:
            self.markers = []
        else:
            self.markers = markers

    def unpack(self,data):
        """ Décode le message binaire pour un groupe de marqueurs

        Args:
            data (bytes) : le message
        
        Returns:
            offset (int) : l'index du dernier byte décodé
        """
        offset = 0

        # Model name
        self.name, separator, remainder = bytes(data[offset:]).partition( b'\0' )
        offset += len( self.name ) + 1

        # Marker count (4 bytes)
        self.markerCount = int.from_bytes( data[offset:offset+4], byteorder='little' )
        offset += 4

        # Markers
        for j in range( 0, self.markerCount ):
            pos = Vector3.unpack( data[offset:offset+12] )
            self.markers.append(Marker(pos[0],pos[1],pos[2]))
            offset += 12        
        return offset

    def to_string(self):
        logmess =  "\tMarker Set Name: {}\n".format(self.name.decode( 'utf-8' ))
        logmess += "\t\tMarker Count: {}\n".format(self.markerCount)        
        for j in range( 0, self.markerCount ):
            logmess += self.markers[j].to_string()
        return logmess

class TimeInfos():
    """ Données temporelles

    Attributes:        
        timecode (int) : temps de référence pour la frame
        timecodeSub (int) : sous-division du temps de référence
        timestamp (double) : temps depuis le démarrage de Motive
    """
    def __init__(self):
        self.timecode = 0
        self.timecodeSub = 0
        self.timestamp = 0

    def unpack(self,data):
        """ Décode le message binaire pour les informations temporels

        Args:
            data (bytes) : le message
        
        Returns:
            offset (int) : l'index du dernier byte décodé
        """
        offset = 0
        # Timecode: Temps de reference pour la frame
        self.timecode = int.from_bytes( data[offset:offset+4], byteorder='little' )
        offset += 4
        # Timecode subdivided: Sous-division du temps de réfence, utile lorsque l'échantillonnage est très grand
        self.timecodeSub = int.from_bytes( data[offset:offset+4], byteorder='little' )
        offset += 4
        # Timestamp (version 2.7 and later): Temps de référence depuis le démarrage de Motive
        self.timestamp, = DoubleValue.unpack( data[offset:offset+8] )
        offset += 8

        return offset

    def to_string(self):
        logmess =  "\tTimeCode: {}\n".format(self.timecode)
        logmess += "\tTimeCode Sub: {}\n".format(self.timecodeSub)
        logmess +=  "\tTimeStamp: {}\n".format(self.timestamp)
        return logmess
    
class LatencyInfos():
    """ Données de latence

    Attributes:        
        stampCameraExposure (int) : Temps du centre de la fenetre d'exposition des caméras
        stampDataReceived (int) : Temps auquel Motive recoit les images des caméras
        stampTransmit (int) : Temps auquel Motive traite les données et les met sur le réseau
    """
    def __init__(self):
        self.stampCameraExposure = 0
        self.stampDataReceived = 0
        self.stampTransmit = 0

    def unpack(self,data):
        """ Décode le message binaire pour la latence

        Args:
            data (bytes) : le message
        
        Returns:
            offset (int) : l'index du dernier byte décodé
        """
        offset = 0
        # Temps du centre de la fenetre d'exposition des caméras
        self.stampCameraExposure = int.from_bytes( data[offset:offset+8], byteorder='little' )
        offset += 8
        # Temps auquel Motive recoit les images des caméras
        self.stampDataReceived = int.from_bytes( data[offset:offset+8], byteorder='little' )
        offset += 8
        # Temps auquel Motive traite les données et les met sur le réseau
        self.stampTransmit = int.from_bytes( data[offset:offset+8], byteorder='little' )
        offset += 8

        return offset

    def to_string(self):
        logmess = "\tstampCamExpo: {}\n".format(self.stampCameraExposure)
        logmess += "\tstampDataRcv: {}\n".format(self.stampDataReceived)
        logmess += "\tstampDataTr: {}\n".format(self.stampTransmit)
        return logmess

class FrameParameters():
    """ Paramètres de la frame

    Attributes:        
        param (int) : Code hexadécimal portant les paramètres
        isRecording (Bool) : Etat de l'enregistrement
        trackedModelsChanged (Bool) : Etat du mode de suivi
    """
    def __init__(self):
        self.param = 0
        self.isRecording = False
        self.trackedModelsChanged = False

    def unpack(self,data):
        """ Décode le message binaire pour les paramètres de la frame

        Args:
            data (bytes) : le message
        
        Returns:
            offset (int) : l'index du dernier byte décodé
        """
        offset = 0
        # Paramètres de contrôle
        self.param, = struct.unpack( 'h', data[offset:offset+2] )
        # Etat de l'enregistrement
        self.isRecording = ( self.param & 0x01 ) != 0
        # Etat du mode de suivi
        self.trackedModelsChanged = ( self.param & 0x02 ) != 0
        offset += 2
        return offset

    def to_string(self):
        logmess = "\tis recording: {}\n".format(self.isRecording)
        logmess += "\thas tracked model changed: {}\n".format(self.trackedModelsChanged)
        return logmess
