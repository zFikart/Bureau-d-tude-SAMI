#! python3
# coding: utf-8

""" Tests unitaires pour l'ensemble de la librairie'

Auteur : Clement FAUVEL, Jean-Luc METZGER
Date : Février 2021
"""

# Ajoute les dossiers contenant les librairies au path
import sys, os
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'src'))

# Importe les librairies tierces
import unittest

# Importe les librairies SAMI
import testNatNet

if __name__ == "__main__":
    loader = unittest.TestLoader()
    start_dir = 'Tests/'
    suite = loader.discover(start_dir)

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)