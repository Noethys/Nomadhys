# -*- coding: utf-8 -*-
#!/usr/bin/env python

##############################################################
# Application :    Nomadhys, application nomade pour Noethys #
# Site internet :  www.noethys.com                           #
# Auteur:          Ivan LUCAS                                #
# Copyright:       (c) 2010-15 Ivan LUCAS                    #
# Licence:         Licence GNU GPL                           #
##############################################################

from kivy.app import App
from kivy.logger import Logger

def GetRepData():
    a = App()
    rep = a.user_data_dir + "nomadhys/"
    del a
    return rep

def ConvertStrToListe(texte=None, siVide=[], separateur=";", typeDonnee="entier"):
    """ Convertit un texte "1;2;3;4" en [1, 2, 3, 4] """
    if texte == None or texte == "" :
        return siVide
    listeResultats = []
    temp = texte.split(separateur)
    for ID in temp :
        if typeDonnee == "entier" :
            ID = int(ID)
        listeResultats.append(ID)
    return listeResultats

    
if __name__ == "__main__":
    print GetRepData()