# -*- coding: utf-8 -*-
#!/usr/bin/env python

##############################################################
# Application :    Nomadhys, application nomade pour Noethys #
# Site internet :  www.noethys.com                           #
# Auteur:          Ivan LUCAS                                #
# Copyright:       (c) 2010-15 Ivan LUCAS                    #
# Licence:         Licence GNU GPL                           #
##############################################################

import sys
import sqlite3
import os
import time
import UTILS_Config
import UTILS_Divers
import sys


DICO_TABLES = {

    "parametres":[   
        ("IDparametre", "INTEGER PRIMARY KEY AUTOINCREMENT"),
        ("nom", "VARCHAR(400)"),
        ("valeur", "VARCHAR(400)"),
        ],
        
    "consommations":[   
        ("IDconso", "INTEGER PRIMARY KEY AUTOINCREMENT"),
        ("horodatage", "DATE"),
        ("action", "VARCHAR(100)"),
        ("IDindividu", "INTEGER"),
        ("IDactivite", "INTEGER"),
        ("IDinscription", "INTEGER"),
        ("date", "DATE"),
        ("IDunite", "INTEGER"),
        ("IDgroupe", "INTEGER"),
        ("heure_debut", "VARCHAR(50)"),
        ("heure_fin", "VARCHAR(50)"),
        ("etat", "VARCHAR(50)"),
        ("date_saisie", "DATE"),
        ("IDutilisateur", "INTEGER"),
        ("IDcategorie_tarif", "INTEGER"),
        ("IDcompte_payeur", "INTEGER"),
        ("quantite", "INTEGER"),
        ("IDfamille", "INTEGER"),
        ],

    "memo_journee":[      
        ("IDmemo", "INTEGER PRIMARY KEY AUTOINCREMENT"),
        ("horodatage", "DATE"),
        ("action", "VARCHAR(100)"),
        ("IDindividu", "INTEGER"),
        ("date", "DATE"),
        ("texte", "VARCHAR(200)"),
        ],
        
    }

ancien_dict = {
    "actions":[   
        ("IDaction", "INTEGER PRIMARY KEY AUTOINCREMENT"),
        ("horodatage", "DATE"),
        ("IDutilisateur", "INTEGER"),
        ("categorie", "VARCHAR(100)"),
        ("action", "VARCHAR(100)"),
        ("donnees", "VARCHAR(500)"),
        ],
        
    }

def VerifieChampExiste(nomTable="", nomChamp=""):
    for nomChampTemp, typeChamp in DICO_TABLES[nomTable] :
        if nomChampTemp == nomChamp :
            return True
    return False


    
class DB:
    def __init__(self, typeFichier="data", IDfichier="", modeCreation=False):
        self.echec = 0
        
        # Recherche le fichier actif
        if IDfichier == "" :
            config = UTILS_Config.Config()
            IDfichier = config.Lire(section="fichier", option="ID", defaut="")
            config.Close() 
            if IDfichier != "" :
                repertoire = UTILS_Divers.GetRepData()
                nomFichier = "%s%s_%s.dat" % (repertoire, typeFichier, IDfichier)
            else :
                self.echec = 1
        
        # Ouverture de la base de données
        if self.echec == 0 :
            self.nomFichier = nomFichier
            self.modeCreation = modeCreation
            self.OuvertureFichier(self.nomFichier)
            
    def OuvertureFichier(self, nomFichier):
        """ Version LOCALE avec SQLITE """
        # Vérifie que le fichier sqlite existe bien
        creerTables = False
        if self.modeCreation == False :
            if os.path.isfile(nomFichier) == False :
                if "actions" in nomFichier :
                    creerTables = True
                else :
                    print("Le fichier '%s' n'existe pas" % nomFichier)
                    self.echec = 1
                    return
        
        # Initialisation de la connexion
        try :
            self.connexion = sqlite3.connect(nomFichier.encode('utf-8'))
            self.cursor = self.connexion.cursor()
        except:
            print("La connexion avec la base de donnees SQLITE a echouee :", sys.exc_info()[0])
            self.erreur = err
            self.echec = 1
        else:
            self.echec = 0
        
        # Création des tables automatique
        if creerTables == True :
            self.CreationTables()      
        
    def CreationTables(self):
        for nomTable, listeChamps in DICO_TABLES.iteritems():
            listeChampsTemp = []
            for nomChamp, typeChamp in listeChamps:
                listeChampsTemp.append("%s %s" % (nomChamp, typeChamp))
            req = "CREATE TABLE %s (%s)" % (nomTable, ", ".join(listeChampsTemp))
            self.cursor.execute(req)
            
    def ExecuterReq(self, req):
        if self.echec == 1 : return False
        try :
            self.cursor.execute(req)
        except:
            print("Requete SQL incorrecte :", sys.exc_info()[0])
            return 0
        else:
            return 1

    def ResultatReq(self):
        if self.echec == 1 : return []
        resultat = self.cursor.fetchall()
        return resultat

    def Commit(self):
        if self.connexion:
            self.connexion.commit()

    def Close(self):
        if self.echec == 1 : return
        if self.connexion:
            self.connexion.close()
    
    def Executermany(self, req="", listeDonnees=[], commit=True):
        """ Executemany pour local ou reseau """    
        """ Exemple de req : "INSERT INTO table (IDtable, nom) VALUES (?, ?)" """  
        """ Exemple de listeDonnees : [(1, 2), (3, 4), (5, 6)] """     
        # Adaptation 
        req = req.replace("%s", "?")
        # Executemany
        self.cursor.executemany(req, listeDonnees)
        if commit == True :
            self.connexion.commit()

    def Ajouter(self, table, champs, valeurs):
        # champs et valeurs sont des tuples
        req = "INSERT INTO %s %s VALUES %s" % (table, champs, valeurs)
        self.cursor.execute(req)
        self.connexion.commit()

    def ReqInsert(self, nomTable, listeDonnees):
        """ Permet d'inserer des donnees dans une table """
        # Préparation des données
        champs = "("
        interr = "("
        valeurs = []
        for donnee in listeDonnees:
            champs = champs + donnee[0] + ", "
            interr = interr + "?, "
            valeurs.append(donnee[1])
        champs = champs[:-2] + ")"
        interr = interr[:-2] + ")"
        req = "INSERT INTO %s %s VALUES %s" % (nomTable, champs, interr)
        # Enregistrement
        try:
            self.cursor.execute(req, tuple(valeurs))
            self.Commit()
            self.cursor.execute("SELECT last_insert_rowid() FROM %s" % nomTable)
            newID = self.cursor.fetchall()[0][0]
        except :
            print("Requete sql d'INSERT incorrecte :", sys.exc_info()[0])
        return newID
    
    def InsertPhoto(self, IDindividu=None, blobPhoto=None):
        sql = "INSERT INTO photos (IDindividu, photo) VALUES (?, ?)"
        self.cursor.execute(sql, [IDindividu, sqlite3.Binary(blobPhoto)])
        self.connexion.commit()
        self.cursor.execute("SELECT last_insert_rowid() FROM Photos")
        newID = self.cursor.fetchall()[0][0]
        return newID

    def MAJPhoto(self, IDphoto=None, IDindividu=None, blobPhoto=None):
        sql = "UPDATE photos SET IDindividu=?, photo=? WHERE IDphoto=%d" % IDphoto
        self.cursor.execute(sql, [IDindividu, sqlite3.Binary(blobPhoto)])
        self.connexion.commit()
        return IDphoto

    def MAJimage(self, table=None, key=None, IDkey=None, blobImage=None, nomChampBlob="image"):
        """ Enregistre une image dans les modes de reglement ou emetteurs """
        sql = "UPDATE %s SET %s=? WHERE %s=%d" % (table, nomChampBlob, key, IDkey)
        self.cursor.execute(sql, [sqlite3.Binary(blobImage),])
        self.connexion.commit()

    def ReqMAJ(self, nomTable, listeDonnees, nomChampID, ID, IDestChaine=False):
        """ Permet d'inserer des donnees dans une table """
        # Préparation des données
        champs = ""
        valeurs = []
        for donnee in listeDonnees:
            champs = champs + donnee[0] + "=?, "
            valeurs.append(donnee[1])
        champs = champs[:-2]
        if IDestChaine == False :
            req = "UPDATE %s SET %s WHERE %s=%d" % (nomTable, champs, nomChampID, ID)
        else:
            req = "UPDATE %s SET %s WHERE %s='%s'" % (nomTable, champs, nomChampID, ID)

        # Enregistrement
        try:
            self.cursor.execute(req, tuple(valeurs))
            self.Commit()
        except :
            print("Requete sql de mise a jour incorrecte :", sys.exc_info()[0])
        
    def ReqDEL(self, nomTable, nomChampID, ID):
        """ Suppression d'un enregistrement """
        req = "DELETE FROM %s WHERE %s=%d" % (nomTable, nomChampID, ID)
        try:
            self.cursor.execute(req)
            self.Commit()
        except :
            print("Requete sql de suppression incorrecte :", sys.exc_info()[0])
            
    def IsTableExists(self, nomTable=""):
        """ Verifie si une table donnee existe dans la base """
        tableExists = False
        for (nomTableTmp,) in self.GetListeTables() :
            if nomTableTmp == nomTable :
                tableExists = True
        return tableExists
                        
    def GetListeTables(self):
        req = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"
        self.ExecuterReq(req)
        listeTables = self.ResultatReq()
        return listeTables

    def GetListeChamps(self):
        """ Affiche la liste des champs de la precedente requete effectuee """
        liste = []
        for fieldDesc in self.cursor.description:
            liste.append(fieldDesc[0])
        return liste

    def GetListeChamps2(self, nomTable=""):
        """ Affiche la liste des champs de la table donnees """
        listeChamps = []
        req = "PRAGMA table_info('%s');" % nomTable
        self.ExecuterReq(req)
        listeTmpChamps = self.ResultatReq()
        for valeurs in listeTmpChamps :
            listeChamps.append( (valeurs[1], valeurs[2]) )
        return listeChamps
    
        

# ---------------------------------------------------------------------------------------------------------------------------------------

def GetChampsTable(nomTable=""):
    for dictTables in (Tables.DB_DATA, Tables.DB_PHOTOS, Tables.DB_DOCUMENTS) :
        if dictTables.has_key(nomTable) :
            listeChamps = []
            for nom, typeTable, info in dictTables[nomTable] :
                listeChamps.append(nom)
            return listeChamps
    return []

    

if __name__ == "__main__":
    # Test
    DB = DB()
    DB.Close() 
    
    