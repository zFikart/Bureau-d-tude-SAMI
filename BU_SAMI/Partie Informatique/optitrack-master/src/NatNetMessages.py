# coding: utf-8

""" Natnet gestion des messages

Auteur : Clement FAUVEL
Date : Janvier 2021
"""

import NatNetDataModel
import struct
from debug import trace


DoubleValue = struct.Struct( '<d' )

class MocapMessage():
    """ Message de type Motion Capture (Mocap)
    
    Ce message contient toutes les informations de localisation transmises dans une frame

    Attributes:
        markerSets (MarkerSet()) : Liste de données pour les groupes de marqueurs
        unlabeledMarkers (unlabeledMarkers()) : Liste de données pour les marqueurs non-étiquetté [A FAIRE]
        markerSets (MarkerSet()) : Liste de données pour les groupes de marqueurs
        rigidBodies (RigidBodies()) : Liste de données pour les corps rigides
        skeletons (Skeletons()) : Liste de données pour les squelettes
        labeledMarkers (LabeledMarkers()) : Liste de données pour les marqueurs [A FAIRE]
        forcePlates (ForcePlates()) : Liste de données pour les capteurs de forces [A FAIRE]
        devices (Devices()) : Liste de données pour les instruments analogiques [A FAIRE]
        timeInfos (TimeInfos()) : Liste de données temporelles
        latencyInfos (LatencyInfos()) : Liste de données pour la latence
        frameParam (FrameParameters()) : Liste de paramètres

    """
    def __init__(self):
        self.frameNumber = -1
        self.numMarkerSets = 0
        self.markerSets = []
        self.numUnLabMrks = 0
        self.unlabeledMarkers = []
        self.numRgb = 0
        self.rigidBodies = []
        self.numSklt = 0
        self.skeletons = []
        self.numLabMrks = 0
        self.labeledMarkers = []
        self.numForcePl = 0
        self.forcePlates = []
        self.numDevices = 0
        self.devices = []
        self.timeInfos = NatNetDataModel.TimeInfos()
        self.latencyInfos = NatNetDataModel.LatencyInfos()
        self.frameParam = NatNetDataModel.FrameParameters()


    def unpackMocapData(self,data):
        """ Décode une trame de type Motion Capture (Mocap)

        Args:
            data (bytes) : le message binaire
        
        Returns:
            offset (int) : l'index du dernier byte décodé
        """ 
        data = memoryview( data )
        offset = 0

        # Frame number
        self.frameNumber = int.from_bytes( data[offset:offset+4], byteorder='little' )
        offset += 4

        # Marker set count
        self.numMarkerSets = int.from_bytes( data[offset:offset+4], byteorder='little' )
        offset += 4
        for i in range( 0, self.numMarkerSets ):
            self.markerSets.append(NatNetDataModel.MarkerSet())
            offset += self.markerSets[i].unpack( data[offset:] )

        # Unlabeled markers
        self.numUnLabMrks = int.from_bytes( data[offset:offset+4], byteorder='little' )
        offset += 4
        for i in range( 0, self.numUnLabMrks ):
            # TODO: Normally, unlabeledMarkersCount == 0 within our testcases
            raise NotImplementedError("The unlabeledMarker object is not implemented yet. Please, remove this options from Motive")
                        
        # Rigid body
        self.numRgb = int.from_bytes( data[offset:offset+4], byteorder='little' )
        offset += 4
        for i in range( 0, self.numRgb ):
            self.rigidBodies.append(NatNetDataModel.RigidBody())
            offset += self.rigidBodies[i].unpack( data[offset:] )

        # Skeleton (Version 2.1 and later)
        self.numSklt = int.from_bytes( data[offset:offset+4], byteorder='little' )
        offset += 4
        for i in range( 0, self.numSklt ):
            # TODO: Normally, skeletonCount == 0 within our testcases
            raise NotImplementedError("The skeleton object is not implemented yet. Please, remove this options from Motive")

        # Labeled markers (Version 2.3 and later)
        self.numLabMrks = int.from_bytes( data[offset:offset+4], byteorder='little' )
        offset += 4
        for i in range( 0, self.numLabMrks ):
            # TODO: Normally, labeledMarkerCount == 0 within our testcases
            raise NotImplementedError("The labeledMarker object is not implemented yet. Please, remove this options from Motive")

        # Force Plate data (version 2.9 and later)
        self.numForcePl = int.from_bytes( data[offset:offset+4], byteorder='little' )
        offset += 4
        for i in range( 0, self.numForcePl ):
            # TODO: Normally, forcePlateCount == 0 within our testcases
            raise NotImplementedError("The ForcePlate object is not implemented yet. Please, remove this options from Motive")

        # Device data (version 2.11 and later)
        self.numDevices = int.from_bytes( data[offset:offset+4], byteorder='little' )
        offset += 4
        for i in range( 0, self.numDevices ):
            # TODO: Normally, forcePlateCount == 0 within our testcases
            raise NotImplementedError("The ForcePlate object is not implemented yet. Please, remove this options from Motive")

        # Timecode            
        offset += self.timeInfos.unpack(data[offset:])

        # Latency informations (Version 3.0 and later)
        offset += self.latencyInfos.unpack(data[offset:])        

        # Frame parameters
        offset += self.frameParam.unpack(data[offset:])        
        
        # Return the current index
        return offset

    def to_string(self):
        logmess = "Message : Motion Capture (FRAMEOFDATA)\n"
        logmess += "Frame #: {}\n".format(self.frameNumber)
        # Collections
        logmess += "Number of collections\n"
        logmess += "\tMarker Set: {} collections\n".format(self.numMarkerSets)
        logmess += "\tUnlabeled Markers: {} collections\n".format(self.numUnLabMrks)
        logmess += "\tRigid bodies: {} collections\n".format(self.numRgb)
        logmess += "\tSkeletons: {} collections\n".format(self.numSklt)
        logmess += "\tLabeled Markers: {} collections\n".format(self.numLabMrks)
        logmess += "\tForce Plates: {} collections\n".format(self.numForcePl)
        logmess += "\tAnalog devices: {} collections\n".format(self.numDevices)
        # Data
        logmess += "Frame of Data:\n"
        for i in range(0,self.numMarkerSets):
                logmess +=self.markerSets[i].to_string()
        for i in range(0,self.numUnLabMrks):
                logmess +=self.unlabeledMarkers[i].to_string()
        for i in range(0,self.numRgb):
                logmess +=self.rigidBodies[i].to_string()
        for i in range(0,self.numSklt):
                logmess +=self.skeletons[i].to_string()
        for i in range(0,self.numLabMrks):
                logmess +=self.labeledMarkers[i].to_string()
        for i in range(0,self.numForcePl):
                logmess +=self.forcePlates[i].to_string()
        for i in range(0,self.numDevices):
                logmess +=self.devices[i].to_string()
        logmess += "Time Informations: \n"
        logmess += self.timeInfos.to_string()
        logmess += "Latency Informations: \n"
        logmess += self.latencyInfos.to_string()
        logmess += "Frame parameters: \n"
        logmess += self.frameParam.to_string()
        return logmess



class DescriptionMessage():
    """ Message de type Description du modele
    
    Ce message contient la description des entités modélisées sous Motive

    Attributes:
        datasetCount (int) : nombre d'entités / jeux de données
        mrkSetDescription (MarkerSetDescription)
        rgbDescription (RigidBodyDescription)
        skltDescription (SkeletonDescription)
    """
    def __init__(self):
        self.datasetCount = 0
        self.mrkSetDescription =[]
        self.rgbDescription = []
        self.skltDescription = []

    def unpackDescript(self, data):
        """ Décode une trame de type Description du modele

        Args:
            data (bytes) : le message binaire
        
        Returns:
            offset (int) : l'index du dernier byte décodé
        """ 
        offset = 0
        self.datasetCount = int.from_bytes( data[offset:offset+4], byteorder='little' )
        offset += 4

        irgb = 0
        imrkSet = 0
        isklt = 0
        for i in range( 0, self.datasetCount ):
            setType = int.from_bytes( data[offset:offset+4], byteorder='little' )
            offset += 4
            if( setType == 0 ):     # Marker set
                self.mrkSetDescription.append(NatNetDataModel.MarkerSetDescription())
                offset += self.mrkSetDescription[imrkSet].unpack( data[offset:] )
                imrkSet +=1
            elif( setType == 1 ):   # Rigid Body
                self.rgbDescription.append(NatNetDataModel.RigidBodyDescription())
                offset += self.rgbDescription[irgb].unpack( data[offset:] )
                irgb += 1
            elif( setType == 2 ):   #Skeleton
                self.skltDescription.append(NatNetDataModel.SkeletonDescription())
                offset += self.skltDescription[isklt].unpack( data[offset:] )
                isklt += 1
        return offset

    def to_string(self):
        logmess = "Message : Description de modele\n"
        logmess+= "Nombre de donnees: {}\n".format(self.datasetCount)
        for i in range(0,len(self.mrkSetDescription)):
            logmess+= self.mrkSetDescription[i].to_string()        
        for i in range(0,len(self.rgbDescription)):
            logmess+= self.rgbDescription[i].to_string()      
        for i in range(0,len(self.skltDescription)):
            logmess+= self.skltDescription[i].to_string()

        return logmess