# -*- coding: utf-8 -*-
#!/usr/bin/env python

##############################################################
# Application :    Nomadhys, application nomade pour Noethys #
# Site internet :  www.noethys.com                           #
# Auteur:          Ivan LUCAS                                #
# Copyright:       (c) 2010-15 Ivan LUCAS                    #
# Licence:         Licence GNU GPL                           #
##############################################################

import GestionDB
import time
import datetime
import json


def AjouterAction(nomTable="", typeAction="", dictAction={}):
    # Préparation des données
    dictAction["horodatage_action"] = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())
    dictAction["type_action"] = typeAction
    
    listeDonnees = []
    for nomChamp, valeur in dictAction.iteritems() :
        if GestionDB.VerifieChampExiste(nomTable, nomChamp) :
            listeDonnees.append((nomChamp, valeur))
    
    # Sauvegarde de l'action
    DB = GestionDB.DB(typeFichier="actions")
    DB.ReqInsert(nomTable, listeDonnees)
    DB.Close() 
        
    
    
def MemoriserActions(listeActions=[]):
    """ listeActions = [(categorie, action, donnees, ...] """
    listeValeurs = []
    for categorie, action, donnees in listeActions :
        horodatage = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())
        IDutilisateur = None
        # Conversion des données en json
        for key, valeur in donnees.iteritems() :
            if type(valeur) == datetime.date :
                donnees[key] = str(valeur)
        donneesjson = json.dumps(donnees)
        listeValeurs.append((horodatage, IDutilisateur, categorie, action, donneesjson))
    
    DB = GestionDB.DB(typeFichier="actions")
    req = "INSERT INTO actions (horodatage, IDutilisateur, categorie, action, donnees) VALUES (?, ?, ?, ?, ?)"
    DB.Executermany(req, listeValeurs, commit=False)
    DB.Commit()
    DB.Close()             

def FiltrerDict(dictDonnees={}, listeKeys=[]):
    """ Pour conserver uniquement certaines valeurs d'un dictionnaire """
    dictTemp = {}
    for key, valeur in dictDonnees.iteritems() :
        if key in listeKeys :
            dictTemp[key] = valeur
    return dictTemp
    
    
    
     
    
    
    
if __name__ == "__main__":
    pass