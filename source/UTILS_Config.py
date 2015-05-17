# -*- coding: utf-8 -*-
#!/usr/bin/env python

##############################################################
# Application :    Nomadhys, application nomade pour Noethys #
# Site internet :  www.noethys.com                           #
# Auteur:          Ivan LUCAS                                #
# Copyright:       (c) 2010-15 Ivan LUCAS                    #
# Licence:         Licence GNU GPL                           #
##############################################################

import os
import ConfigParser
import os
import sys
import random
import UTILS_Divers
from kivy.logger import Logger

#runpath = os.path.dirname(os.path.realpath(sys.argv[0]))
#os.chdir(runpath)


def GenerationIDappareil():
    """ Generation d'un ID pour l'appareil """
    IDappareil = ""
    for x in range(0, 6) :
        IDappareil += random.choice("ABCDEFGH23456789")
    return IDappareil

    
LISTE_VALEURS = (
    ("general", "nom_appareil", ""),
    ("general", "ID_appareil", GenerationIDappareil()),
    
    ("fichier", "ID", ""),
    
    ("utilisateur", "memoriser_code", ""),
    ("utilisateur", "code", ""),
    
    ("synchronisation", "serveur_adresse", ""),
    ("synchronisation", "serveur_port", ""),
    ("synchronisation", "ftp_hote", ""),
    ("synchronisation", "ftp_identifiant", ""),
    ("synchronisation", "ftp_mdp", ""),
    ("synchronisation", "ftp_repertoire", ""),
    ("synchronisation", "cryptage_activer", ""),
    ("synchronisation", "cryptage_mdp", ""),
    ("synchronisation", "type_transfert", ""),
    )
    
class Config():
    def __init__(self):
        rep = UTILS_Divers.GetRepData()
        self.nomFichier = rep + "config.cfg"
        self.config = ConfigParser.ConfigParser()
        self.dirty = False
        # Ouverture du fichier
        if self.config.read(self.nomFichier) == [] :
            self.Creation() 

    def Creation(self):
        """ Création du fichier si n'existe pas """
        for section, option, valeur in LISTE_VALEURS : 
            self.Ecrire(section, option, valeur)
    
    def Verification(self):
        """ Verifie si toutes les valeurs ont ete crees """
        for section, option, valeur in LISTE_VALEURS : 
            self.Lire(section, option, valeur)
    
    def Close(self):
        """ Sauvegarde du fichier """
        if self.dirty == True :
            self.config.write(open(self.nomFichier, 'w'))
    
    def Ecrire(self, section="", option="", valeur=""):
        self.dirty = True
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, option, valeur)
    
    def Lire(self, section="", option="", defaut="", typeValeur=str):
        # Vérifie que l'option existe, sinon la crée avec la valeur défaut
        if not self.config.has_section(section) :
            self.Ecrire(section, option, defaut)
        else :
            if not self.config.has_option(section, option) :
                self.Ecrire(section, option, defaut)
        # Lecture de la valeur
        if typeValeur == int :
            valeur = self.config.getint(section, option)
        elif typeValeur == float :
            valeur = self.config.getfloat(section, option)
        elif typeValeur == bool :
            valeur = self.config.getboolean(section, option)
        else :
            valeur = self.config.get(section, option)
        return valeur
    
    
    
    
    
    
if __name__ == "__main__":
    config = Config() 