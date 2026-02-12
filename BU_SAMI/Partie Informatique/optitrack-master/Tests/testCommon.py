# coding: utf-8

""" Tests unitaires pour les fonctions utilitaires

Auteur : Clement FAUVEL, Jean-Luc METZGER
Date : Janvier 2021
"""
import unittest
import numpy as np
import sys, os
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'src'))

from common import *



class testNode(unittest.TestCase):

    def test_eulerFromQuart(self):
        quat = [0.00013000886247027665,0.3534943163394928,0.010053183883428574,0.9353827238082886]
        eul = euler_from_quaternion(*quat)
        self.assertAlmostEqual(eul[0],0.0097995)
        self.assertAlmostEqual(eul[1], 0.7225536)
        self.assertAlmostEqual(eul[2], 0.0251974)

    def test_yawFromOrient(self):
        eul = [np.pi,20*np.pi/180,np.pi]
        



if __name__ == '__main__':
        unittest.main(verbosity=2)