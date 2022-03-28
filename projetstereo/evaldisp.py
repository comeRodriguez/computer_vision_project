#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Petit code d'évaluation des disparités, avec gestion des occlusions.
"""

import sys
import numpy as np
#import matplotlib.pyplot as plt
from skimage import io

def evaldisp(GT, occl, disp):
    # mise à l'échelle pixellique normale des disparités et de la vérité
    GT = GT / 4.
    disp = disp / 4.
    # occlusions passées en type binaire
    occl = occl > 0

    # mesures d'erreur des disparités estimées

    nbpts_nonoccl = np.count_nonzero(occl)
    abserrmap = np.absolute(GT-disp) * occl
    #plt.figure()
    #plt.imshow(abserrmap, cmap='jet')

    # mesure de l'erreur moyenne des disparités
    errmoy = np.sum(abserrmap) / nbpts_nonoccl

    # mesure du pourcentage de points de disparité > seuil
    s1 = 1
    s2 = 2

    s1map = abserrmap > s1
    #plt.figure()
    #plt.imshow(s1map, cmap='gray')
    s2map = abserrmap > s2
    #plt.figure()
    #plt.imshow(s2map, cmap='gray')

    ps1 = np.count_nonzero(s1map) / nbpts_nonoccl
    ps2 = np.count_nonzero(s2map) / nbpts_nonoccl
    
    return errmoy, ps1, ps2
    

def main(fgt, foccl, fdisp):
    GT = io.imread(fgt)
    occl = io.imread(foccl) # occlusions point de vue image gauche
    disp = io.imread(fdisp)

    assert GT.shape == occl.shape == disp.shape, "Les images de cartes de disparité et d'occlusions d'entrée n'ont pas les mêmes dimensions !"


    errmoy, ps1, ps2 = evaldisp(GT, occl, disp)
    
    print("Erreur moyenne des disparités estimées = {:.2f} px".format(errmoy))
    print("Pourcentage de disparités dont l'erreur est > à 1 px = {:.2f} %".format(ps1*100.))
    print("Pourcentage de disparités dont l'erreur est > à 2 px = {:.2f} %".format(ps2*100.))


if __name__ == '__main__':
    # arguments
    assert len(sys.argv) == 4, "Il faut 3 arguments : evaldisp.py disparite_verite.png occlusions_verite.png disparite_estimee.png"
    
    main(sys.argv[1], sys.argv[2], sys.argv[3])
