# coding: utf-8

""" Fichier contenant des variables et fonctions utiles pour la gestion de la localition

Auteur : Clement FAUVEL, Jean-Luc METZGER
Date : Février 2021
"""

import numpy as np
import math





# Fonctions
def euler_from_quaternion(x, y, z, w):
    """
    Convert a quaternion into euler angles (roll, pitch, yaw)
    roll is rotation around x in radians (counterclockwise)
    pitch is rotation around y in radians (counterclockwise)
    yaw is rotation around z in radians (counterclockwise)
    
    Args:
        A quaternion: q = ix + jy + kz + w

    Source: https://automaticaddison.com/how-to-convert-a-quaternion-into-euler-angles-in-python/
    """
    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    roll_x = math.atan2(t0, t1)
    
    t2 = +2.0 * (w * y - z * x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    pitch_y = math.asin(t2)
    
    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    yaw_z = math.atan2(t3, t4)
    
    return roll_x, pitch_y, yaw_z # in radians


def MROT_X(theta):
    """ Matrice de rotation autours de l'axe x selon l'angle theta

    Args:
        theta (float): angle de rotation exprimé en radian

    Returns:
        MROT_X : une matrice de rotation (numpy)
    """
    return np.array([[1. , 0. , 0.],
                    [0. , np.cos(theta) , -np.sin(theta)],
                    [0. , np.sin(theta) , np.cos(theta)]])


def MROT_Y(theta):
    """ Matrice de rotation autours de l'axe y selon l'angle theta

    Args:
        theta (float): angle de rotation exprimé en radian

    Returns:
        MROT_Y : une matrice de rotation (numpy)
    """
    return np.array([[np.cos(theta) , 0. , np.sin(theta)], \
                    [0. , 1. , 0.], \
                    [-np.sin(theta) , 0. , np.cos(theta)]])

def MROT_Z(theta):
    """ Matrice de rotation autours de l'axe z selon l'angle theta

    Args:
        theta (float): angle de rotation exprimé en radian

    Returns:
        MROT_Z : une matrice de rotation (numpy)
    """
    return np.array([[np.cos(theta) , -np.sin(theta) , 0], \
                    [np.sin(theta) , np.cos(theta) , 0.], \
                    [ 0., 0. , 1.]])


# CONSTANT MATRICES
MROT_X90p = MROT_X(np.pi/2)
MROT_X90n = MROT_X(-np.pi/2)
MROT_X180 = MROT_X(np.pi)

MROT_Y90p = MROT_Y(np.pi/2)
MROT_Y90n = MROT_Y(-np.pi/2)
MROT_Y180 = MROT_Y(np.pi)

MROT_Z90p = MROT_Z(np.pi/2)
MROT_Z90n = MROT_Z(-np.pi/2)
MROT_Z180 = MROT_Z(np.pi)

MROT = MROT_X90p.dot(MROT_Y180)




def position_motive_to_sami(position):
    """ Transforme un vecteur contenant la position depuis le repere Motive vers SAMI

    Args:
        position (vect): vecteur d'euler dans le repère Motive

    Returns:
        npos : le vecteur d'euler dans le repère SAMI
    """
    npos = np.array(position)
    npos = MROT.dot(npos)    # rotation
    npos[0] += 3         # translation de 3m à gauche
    return npos


def orientation_motive_to_sami(orientation):
    """ Transforme un quaternion ou un vecteur contenant les angles d'Euler depuis le repere Motive vers SAMI

    Args:
        orientation (vect): quaternion ou angles d'euler dans le repère Motive

    Returns:
        eul : le vecteur d'euler dans le repère SAMI
    """
    if(len(orientation) == 4): # this is a quaternion
        eul = np.array(euler_from_quaternion(*orientation))
    elif(len(orientation) == 3): # this is a euler vector
        eul = orientation    
    # Apply transformation from Motive frame to SAMI frame
    eul = MROT.dot(eul)    # rotation
    return eul

def yaw_from_orientation(orientation,with_rot=True):
    """ Extrait le yaw depuis un quaternion ou un vecteur contenant les angles d'Euler

    Args:
        orientation (vect): quaternion ou angles d'euler
        with_rot (bool) : applique la rotation entre le repère motive et sami (True par défaut)

    Returns:
        yaw : le yaw après transformation
    """
    if(with_rot is True):
        # Apply transformation from Motive frame to SAMI frame
        eul = orientation_motive_to_sami(orientation)
    yaw = eul[2]
    # Change the yaw following the quadrant
    if(abs(eul[1]) > math.pi/2 ):
        if(eul[2]>0):
            # quadrant 2: [pi/2,0] -> [3*pi/2,2*pi]
            yaw = 2*math.pi - yaw
        if(eul[2]<0):
            # quadrant 3: [-pi/2;0] -> [0,pi/2]
            yaw = -yaw
    else:
        if(eul[2]<0):
            # quadrant 4:  [-pi/2;0] -> [pi/2,pi]
            yaw = math.pi + yaw
        if(eul[2]>0):
            # quadrant 1: [0;pi/2] -> [pi;3*pi/2]
            yaw = math.pi + yaw
    return yaw
