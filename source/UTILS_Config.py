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

#runpath = os.path.dirname(os.path.realpath(sys.argv[0]))
#os.chdir(runpath)

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
        self.dirty = True
        
        # Section general
        self.config.add_section("general")
        self.config.set("general", "nom_appareil", "")
        self.config.set("general", "ID_appareil", GenerationIDappareil())
        
        # Section Fichier
        self.config.add_section("fichier")
        self.config.set("fichier", "ID", "")
        
        # Synchronisation
        self.config.add_section("synchronisation")
        self.config.set("synchronisation", "serveur_adresse", "")
        self.config.set("synchronisation", "serveur_port", "")
        self.config.set("synchronisation", "ftp_hote", "")
        self.config.set("synchronisation", "ftp_identifiant", "")
        self.config.set("synchronisation", "ftp_mdp", "")
        self.config.set("synchronisation", "ftp_repertoire", "")
        self.config.set("synchronisation", "cryptage_activer", "")
        self.config.set("synchronisation", "cryptage_mdp", "")
        self.config.set("synchronisation", "type_transfert", "")
    
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
    
def GenerationIDappareil():
    """ Genereation d'un ID pour l'appareil """
    IDappareil = ""
    for x in range(0, 6) :
        IDappareil += random.choice("ABCDEFGH23456789")
    return IDappareil
    
    
    
    
if __name__ == "__main__":
    config = Config() 