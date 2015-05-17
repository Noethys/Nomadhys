# -*- coding: utf-8 -*-
#!/usr/bin/env python

##############################################################
# Application :    Nomadhys, application nomade pour Noethys #
# Site internet :  www.noethys.com                           #
# Auteur:          Ivan LUCAS                                #
# Copyright:       (c) 2010-15 Ivan LUCAS                    #
# Licence:         Licence GNU GPL                           #
##############################################################

from kivy.logger import Logger
import os
import json
import time
import zipfile
import ftplib
import shutil

import UTILS_Config
import UTILS_Cryptage_fichier
import UTILS_Divers
import UTILS_Dates
import GestionDB

from msgbox import MsgBox
from parametres import Popup_parametres

# install_twisted_rector must be called before importing  and using the reactor
from kivy.support import install_twisted_reactor
install_twisted_reactor()
from twisted.internet import reactor, protocol

EXTENSION_CRYPTE = ".nsc"
EXTENSION_DECRYPTE = ".nsd"



def sizeof_fmt(num):
    for unit in ['','Ko','Mo','Go']:
        if abs(num) < 1024.0:
            return "%3.1f%s" % (num, unit)
        num /= 1024.0

def GenerationFichierAenvoyer():
    """ Génération du fichier à envoyer """
    repertoire = UTILS_Divers.GetRepData()
    
    # Recherche des parametres
    config = UTILS_Config.Config()
    IDfichier = config.Lire(section="fichier", option="ID", defaut="")
    cryptage_activer = config.Lire(section="synchronisation", option="cryptage_activer", defaut=0)
    cryptage_mdp = config.Lire(section="synchronisation", option="cryptage_mdp", defaut="")
    config.Close() 
    
    # Génération des noms de fichiers
    nomFichierData = UTILS_Divers.GetRepData() + "actions_%s.dat" % IDfichier
    horodatage = time.strftime('%Y%m%d%H%M%S', time.localtime())
    nomFichierActions = repertoire + "actions_%s_%s%s" % (IDfichier, horodatage, EXTENSION_DECRYPTE)
    
    # Vérifie qu'un fichier Actions existe
    if os.path.isfile(nomFichierData) == False :
        return None
    
    # Compression
    fichierZip = zipfile.ZipFile(nomFichierActions, "w", compression=zipfile.ZIP_DEFLATED)
    fichierZip.write(nomFichierData, "database.dat")
    fichierZip.close()
    
    # Cryptage
    if cryptage_activer == "1" and cryptage_mdp != "" and UTILS_Cryptage_fichier.IMPORT_AES == True :
        nouveauNom = nomFichierActions.replace(EXTENSION_DECRYPTE, EXTENSION_CRYPTE)
        UTILS_Cryptage_fichier.CrypterFichier(nomFichierActions, nouveauNom, cryptage_mdp)
        os.remove(nomFichierActions)
        nomFichierActions = nouveauNom
    
    # Renvoie le nom du fichier
    return nomFichierActions


    
    
    
class Echo(protocol.Protocol):
    action = "envoyer"
    dictFichierReception = None
    nomFichierAenvoyer = None
    
            
    def connectionMade(self):
        self.screen.EcritLog("Connexion avec l'hôte %s effectuée" % self.transport.getPeer().host)
        
        if self.action == "envoyer" :
            # Recherche le nom de fichier à envoyer
            self.screen.EcritLog("Génération du fichier à envoyer")
            self.nomFichierAenvoyer = GenerationFichierAenvoyer() 
            if self.nomFichierAenvoyer == None :
                self.screen.EcritLog("Erreur : Aucun fichier à générer")
                return
            tailleFichier = os.path.getsize(self.nomFichierAenvoyer) 
            nomFichier = self.nomFichierAenvoyer.replace(UTILS_Divers.GetRepData(), "")
            # Récupération du nom de l'appareil
            config = UTILS_Config.Config()
            nom_appareil = config.Lire(section="general", option="nom_appareil", defaut="")
            config.Close() 
            # Envoi des infos sur le fichier
            self.transport.write(json.dumps({"action":"envoyer", "nom_appareil":nom_appareil, "nom":nomFichier, "taille":tailleFichier}))
        
        if self.action == "recevoir" :
            self.transport.write("recevoir")
            self.screen.EcritLog("Recherche du fichier sur le serveur. Veuillez patientez...")
            
    def Envoyer(self):
        # Envoie le fichier
        self.screen.EcritLog("Envoi en cours...")
        f = open(self.nomFichierAenvoyer, "rb")
        self.transport.write(f.read())
        f.close()
        self.screen.EcritLog("Fin de l'envoi")
        self.screen.EcritLog("", log=False)
        os.remove(self.nomFichierAenvoyer)
        
        # Ferme la connexion
        self.transport.loseConnection()

    def dataReceived(self, data):
        #print("data recue = " + str(len(data)))
        
        # Envoi d'un fichier
        if data == "pret_pour_reception" :
            self.Envoyer()
        
        # Reception d'un fichier
        if self.action == "recevoir" :
            try:
                message = json.loads(data)
                isJson = True
            except :
                isJson = False
            
            if isJson == True :
                # Reception d'un fichier - init
                if message["action"] == "envoyer" :
                    tailleFichier = message["taille"]
                    nomInitial = message["nom"]
                    # Recherche du IDfichier en cours
                    config = UTILS_Config.Config()
                    IDfichier = config.Lire(section="fichier", option="ID", defaut="")
                    config.Close() 
                    if IDfichier not in nomInitial :
                        self.screen.EcritLog("Aucun fichier disponible sur le serveur")
                        return
    
                    nomFinal = UTILS_Divers.GetRepData() + nomInitial
                    self.screen.EcritLog("Ok pour recevoir le fichier %s de taille %s" % (nomInitial, sizeof_fmt(tailleFichier)))
                    fichier = open(nomFinal,"wb")
                    self.transport.write("pret_pour_reception")
                    self.screen.EcritLog("Création du fichier de réception")
                    self.screen.EcritLog("Transfert du fichier en cours...")
                    
                    self.dictFichierReception = {
                        "nom_initial" : nomInitial,
                        "nom_final" : nomFinal,
                        "taille_totale" : tailleFichier,
                        "taille_actuelle" : 0,
                        "fichier" : fichier,
                        }
                    
            else :
                # Reception du fichier
                self.dictFichierReception["fichier"].write(data)

                # Calcule de la taille de la partie telechargee
                self.dictFichierReception["taille_actuelle"] += len(data)
                pourcentage = int(100.0 * self.dictFichierReception["taille_actuelle"] / self.dictFichierReception["taille_totale"])
                self.screen.EcritLog("[" + str(pourcentage) + " %] Transfert en cours...", log=False)
                self.screen.SetValeurProgressbar(pourcentage)
                
                # Envoi un message de fin de reception
                if self.dictFichierReception["taille_actuelle"] == self.dictFichierReception["taille_totale"] :
                    self.transport.write("fin_envoi")
                    
    
    def connectionLost(self, reason):
        if self.dictFichierReception != None:
            self.screen.EcritLog("Clôture du fichier de réception")
            self.dictFichierReception["fichier"].close()
            
            # Vérifie que le fichier a été transféré en intégralité
            if self.dictFichierReception["taille_totale"] == self.dictFichierReception["taille_actuelle"] :
                self.screen.EcritLog("Transfert reussi")
                self.screen.ReceptionFichier(self.dictFichierReception["nom_final"])
            else :
                self.screen.EcritLog("Echec du transfert : le fichier est incomplet !")
            
            self.dictFichierReception = None
            
        self.screen.EcritLog("Fin de la connexion avec %s" % self.transport.getPeer().host)
        self.screen.EcritLog("", log=False)
        
        
        
class EchoFactory(protocol.ClientFactory):
    protocol = Echo
    
    def __init__(self, screen, action=""):
        self.protocol.screen = screen
        self.protocol.action = action

    def clientConnectionLost(self, connector, reason):
        #self.protocol.screen.EcritLog("Connexion perdue", etat=False)
        pass
    
    def clientConnectionFailed(self, connector, reason):
        self.protocol.screen.EcritLog("Echec de la connexion", etat=False)

    def startedConnecting(self, connector):
        self.protocol.screen.EcritLog("Tentative de connexion", etat=False)

        
# --------------------------------- INTERFACE KIVY -------------------------------------------------

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from widgets import BoutonAvecImageLarge_fond_normal

Builder.load_string("""

<Synchronisation>
    log_sync: log_sync
    progress: progress
    ctrl_etat: ctrl_etat
    ctrl_type_transfert: ctrl_type_transfert
    
    BoxLayout:
        orientation: 'vertical'
        
        BoxLayout:
            orientation: 'vertical'
            #cols: 1
            #rows: 4
            padding: 10
            size_hint: 1, 1
            
            Spinner:
                id: ctrl_type_transfert
                text: 'Transfert par serveur Internet/WIFI'
                values: ('Transfert par serveur Internet/WIFI', 'Transfert par FTP', 'Transfert manuel')
                size_hint_y: None
                height: '48dp'
                on_text: root.MemorisationTypeTransfert()
            
            Label:
                height: 10
                size_hint: 1, None
                
            TextInput:
                id: log_sync
                text: ''
                multiline: True
                readonly: True
                size_hint: 1, 1
            
            ProgressBar:
                id: progress
                max: 100
                size_hint: 1, None
                height: 5
            
            Label:
                height: 10
                size_hint: 1, None
                        
            BoxLayout:
                orientation: 'horizontal' if root.width > 350 else 'vertical'
                size_hint: 1, None
                height: 60 if self.orientation == 'horizontal' else 180

                BoutonAvecImageLarge_fond_normal:
                    texte: 'Envoyer'
                    chemin_image: 'images/envoyer.png'
                    size_hint: 1, None
                    height: 60
                    on_release: root.OnBoutonEnvoyer() 
                    
                BoutonAvecImageLarge_fond_normal:
                    texte: 'Recevoir'
                    chemin_image: 'images/recevoir.png'
                    size_hint: 1, None
                    height: 60
                    on_release: root.OnBoutonRecevoir() 

                BoutonAvecImageLarge_fond_normal:
                    texte: 'Paramètres'
                    chemin_image: 'images/parametres.png'
                    size_hint: 1, None
                    height: 60
                    on_release: root.OnBoutonParametres() 
                
        GridLayout:
            cols: 3
            rows: 1
            row_force_default: True
            row_default_height: 30
            spacing: 5, 5
            padding: 10
            size_hint: 1, None
            height: 50

            canvas.before:
                Color:
                    rgb: 0.128, 0.128, 0.128, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
                   
            Label:
                id: ctrl_etat
                text: ''
                markup: True
                font_size: 14
                size_hint: 1, None
                v_align: 'middle'
                text_size: (self.size[0], None)

            
""")
            
class Synchronisation(Screen):
    log_sync = ObjectProperty()
    progress = ObjectProperty() 
    ctrl_etat = ObjectProperty() 
    ctrl_type_transfert = ObjectProperty() 
    
    def __init__(self, *args, **kwargs):
        self.app = kwargs.get("app", None)
        super(Screen, self).__init__(*args, **kwargs)	
        self.ctrl_etat.text = ""
        
        # Récupération du type de transfert préféré
        config = UTILS_Config.Config()
        type_transfert = config.Lire(section="synchronisation", option="type_transfert", defaut="")
        config.Close() 
        if type_transfert == "ftp" : self.ctrl_type_transfert.text = "Transfert par FTP"
        if type_transfert == "manuel" : self.ctrl_type_transfert.text = "Transfert manuel"
    
    def MAJ(self):
        pass
        
    def MemorisationTypeTransfert(self):
        type_transfert = self.GetTypeTransfert() 
        config = UTILS_Config.Config()
        config.Ecrire(section="synchronisation", option="type_transfert", valeur=type_transfert)
        config.Close() 
    
    def GetTypeTransfert(self):
        if "serveur" in self.ctrl_type_transfert.text : return "serveur"
        if "FTP" in self.ctrl_type_transfert.text : return "ftp"
        if "manuel" in self.ctrl_type_transfert.text : return "manuel"
        
    def OnBoutonEnvoyer(self):
        # Vérifie que le nom de l'appareil a bien été renseigné avant
        config = UTILS_Config.Config()
        nom_appareil = config.Lire(section="general", option="nom_appareil", defaut="")
        ID_appareil = config.Lire(section="general", option="ID_appareil", defaut="")
        config.Close()
        if nom_appareil == "" :
            MsgBox.info(text="Vous devez obligatoirement renseigner le nom de l'appareil ! \n(Menu principal > Paramètres > Généralités)", title="Erreur", size_hint=(0.6, 0.6))
            return
            
        DB = GestionDB.DB(typeFichier="actions")
        req = """SELECT IDparametre, nom, valeur
        FROM parametres;"""
        DB.ExecuterReq(req)
        listeTemp = DB.ResultatReq()
        dictTemp = {}
        for IDparametre, nom, valeur in listeTemp :
            dictTemp[nom] = IDparametre
        
        if dictTemp.has_key("nom_appareil") :
            DB.ReqMAJ("parametres", [("nom", "nom_appareil"), ("valeur", nom_appareil)], "IDparametre", dictTemp["nom_appareil"])
        else :
            DB.ReqInsert("parametres", [("nom", "nom_appareil"), ("valeur", nom_appareil)])
        if dictTemp.has_key("ID_appareil") :
            DB.ReqMAJ("parametres", [("nom", "ID_appareil"), ("valeur", ID_appareil)], "IDparametre", dictTemp["ID_appareil"])
        else :
            DB.ReqInsert("parametres", [("nom", "ID_appareil"), ("valeur", ID_appareil)])

        DB.Close() 
            
        # Lancement du transfert
        typeTransfert = self.GetTypeTransfert() 
        if typeTransfert == "serveur" : self.StartServer(action="envoyer")
        if typeTransfert == "ftp" : self.StartFTP(action="envoyer")
        if typeTransfert == "manuel" : self.StartManuel(action="envoyer")  
            
    def OnBoutonRecevoir(self):
        typeTransfert = self.GetTypeTransfert() 
        if typeTransfert == "serveur" : self.StartServer(action="recevoir")
        if typeTransfert == "ftp" : self.StartFTP(action="recevoir")
        if typeTransfert == "manuel" : self.StartManuel(action="recevoir")

    def OnBoutonParametres(self):
        popup = Popup_parametres(pages=["synchronisation"])
        popup.open() 
        
    def StartServer(self, action="envoyer"):
        # Récupération des paramètres de connexion dans le config
        config = UTILS_Config.Config()
        adresse = config.Lire(section="synchronisation", option="serveur_adresse", defaut="")
        port = config.Lire(section="synchronisation", option="serveur_port", defaut="")
        config.Close() 
        # Connexion au serveur
        try :
            reactor.connectTCP(adresse, int(port), EchoFactory(self, action=action), timeout=5)
        except Exception, err:
            self.EcritLog("Echec de la connexion : Verifiez les paramètres !")
            MsgBox.info(text="Verifiez les paramètres de connexion !", title="Echec de la connexion", size_hint=(0.6, 0.6))
    
    def StartFTP(self, action="envoyer"):
        # Récupération des paramètres dans le config
        config = UTILS_Config.Config()
        IDfichier = config.Lire(section="fichier", option="ID", defaut="")
        ftp_hote = config.Lire(section="synchronisation", option="ftp_hote", defaut="")
        ftp_identifiant = config.Lire(section="synchronisation", option="ftp_identifiant", defaut="")
        ftp_mdp = config.Lire(section="synchronisation", option="ftp_mdp", defaut="")
        ftp_repertoire = config.Lire(section="synchronisation", option="ftp_repertoire", defaut="")
        config.Close() 
        
        if ftp_hote == "" or ftp_identifiant == "" or ftp_mdp == "" :
            self.EcritLog("Erreur de connexion : Vérifiez les paramètres FTP !")
            return
            
        # Transfert : Envoyer
        if action == "envoyer" :
            self.EcritLog("Génération du fichier à envoyer")
            nomFichier = GenerationFichierAenvoyer()
            if nomFichier == None :
                self.EcritLog("Erreur : Aucun fichier à générer")
                return
            try :
                ftp = ftplib.FTP(ftp_hote, ftp_identifiant, ftp_mdp)
                ftp.cwd(ftp_repertoire)
                fichier = open(nomFichier, "rb")
                ftp.storbinary("STOR %s" % os.path.basename(nomFichier), fichier)
                fichier.close()
                # Vérifie la taille du fichier envoyé
                if ftp.size(os.path.basename(nomFichier)) == os.path.getsize(nomFichier) :
                    self.EcritLog("Fichier transféré avec succès")
                    self.EcritLog("", log=False)
                else :
                    self.EcritLog("Transfert du fichier incomplet")
                ftp.quit()
                os.remove(nomFichier)
            except Exception, err :
                self.EcritLog("Erreur dans l'envoi du fichier par FTP : " + err)
                
        # Transfert : Recevoir
        if action == "recevoir" :
            listeFichiersRecus = []
            self.EcritLog("Recherche de fichiers dans le répertoire FTP")
            try :
                ftp = ftplib.FTP(ftp_hote, ftp_identifiant, ftp_mdp)
                ftp.cwd(ftp_repertoire)
            except :
                self.EcritLog("Erreur de connexion : Vérifiez les paramètres FTP !")
                return
            # Récupère la liste des fichiers de synchronisation présents sur le répertoire FTP
            for nomFichier in ftp.nlst() :
                if nomFichier.startswith("data_%s" % IDfichier) and (nomFichier.endswith(EXTENSION_CRYPTE) or nomFichier.endswith(EXTENSION_DECRYPTE)) :
                    tailleFichier = ftp.size(nomFichier) 
                    nomFichierFinal = self.app.user_data_dir + nomFichier
                    ftp.retrbinary("RETR %s" % nomFichier, open(nomFichierFinal, "wb").write) 
                    listeFichiersRecus.append((nomFichierFinal, tailleFichier))
            ftp.quit()
            if len(listeFichiersRecus) == 0 :
                self.EcritLog("Aucun fichier dans le répertoire FTP")
                return
            for nomFichierFinal, tailleFichier in listeFichiersRecus :
                if os.path.getsize(nomFichierFinal) != tailleFichier :
                    self.EcritLog("Transfert du fichier '%s' incomplet" % nomFichierFinal)
                else :
                    self.EcritLog("Fichier réceptionné avec succès")
                    self.ReceptionFichier(nomFichierFinal)
                
                
    def StartManuel(self, action="envoyer"):
        # Transfert : Envoyer
        if action == "envoyer" :
            self.EcritLog("Génération du fichier à envoyer", etat=False)
            nomFichierAenvoyer = GenerationFichierAenvoyer() 
            if nomFichierAenvoyer == None :
                self.EcritLog("Erreur : Aucun fichier à générer")
                return
            self.EcritLog("Choix du chemin de destination", etat=False)
            from selection_fichier import SelectionFichier
            popup = SelectionFichier(title="Sélectionnez un répertoire de sauvegarde", nomFichier=nomFichierAenvoyer, callback=self.SauverFichier, chemin=UTILS_Divers.GetRepData(), size_hint=(0.8, 0.8))
            popup.open()  
            
        # Transfert : Recevoir
        if action == "recevoir" :
            self.EcritLog("Choix du fichier à importer", etat=False)
            from selection_fichier import SelectionFichier
            popup = SelectionFichier(title="Sélectionnez un fichier à importer", callback=self.ChargerFichier, chemin=UTILS_Divers.GetRepData(), size_hint=(0.8, 0.8))
            popup.open()  

    def ChargerFichier(self, chemin="", nomFichier=""):
        """ Recevoir un fichier manuel """
        # Recherche du IDfichier en cours
        config = UTILS_Config.Config()
        IDfichier = config.Lire(section="fichier", option="ID", defaut="")
        config.Close() 
        # Vérification du fichier
        if "data_%s" % IDfichier not in nomFichier :
            MsgBox.info(text="Récuperation impossible : Le fichier doit commencer par 'data_%s' ! " % IDfichier, title="Echec de la recuperation", size_hint=(0.6, 0.6))
            return
        self.ReceptionFichier(nomFichier)
    
    def SauverFichier(self, chemin="", nomFichier=""):
        nouveauFichier = chemin + nomFichier.replace(UTILS_Divers.GetRepData(), "")
        if nouveauFichier != nomFichier :
            shutil.copyfile(nomFichier, nouveauFichier)
            self.EcritLog("Fichier copie avec succès vers '%s'" % chemin)
        
    def ReceptionFichier(self, nomFichier):
        """ Analyse du fichier recu """
        config = UTILS_Config.Config()
        cryptage_mdp = config.Lire(section="synchronisation", option="cryptage_mdp", defaut="")
        IDfichier = config.Lire(section="fichier", option="ID", defaut="")
        ID_appareil = config.Lire(section="general", option="ID_appareil", defaut="")
        config.Close() 

        # Décryptage du fichier
        if nomFichier.endswith(EXTENSION_CRYPTE) :
            fichierCrypte = True
            self.EcritLog("Décryptage du fichier")
            if cryptage_mdp == "" :
                self.EcritLog("Erreur : Décryptage impossible. Vous devez saisir le mot de passe dans les paramètres.")
                os.remove(nomFichier)
                return
            if UTILS_Cryptage_fichier.IMPORT_AES == False :
                self.EcritLog("Erreur : Décryptage impossible. Le module de décryptage n'est pas disponible.")
                os.remove(nomFichier)
                return
            nouveauCheminFichier = nomFichier.replace(EXTENSION_CRYPTE, EXTENSION_DECRYPTE)
            resultat = UTILS_Cryptage_fichier.DecrypterFichier(nomFichier, nouveauCheminFichier, cryptage_mdp)
            os.remove(nomFichier)
        else :
            fichierCrypte = False
            nouveauCheminFichier = nomFichier
            
        # Décompression du fichier
        if zipfile.is_zipfile(nouveauCheminFichier) == False :
            self.EcritLog("Erreur : Le fichier '%s' n'est pas une archive valide" % nouveauCheminFichier)
            if fichierCrypte == True :
                self.EcritLog("Vérifiez que le mot de passe de cryptage est exact dans les paramètres de synchronisation")
            return False        
        
        fichierZip = zipfile.ZipFile(nouveauCheminFichier, "r")
        buffer = fichierZip.read("database.dat")
        nomFichierFinal = nouveauCheminFichier.replace(EXTENSION_DECRYPTE, ".dat")
        #nomFichierFinal = nomFichierFinal.replace("temp/", "data/")
        
        f = open(nomFichierFinal, "wb")
        f.write(buffer)
        f.close()
        fichierZip.close()
        os.remove(nouveauCheminFichier)
        self.EcritLog("Fichier reçu installé avec succès")
        
        # Suppression des fichiers d'actions obsolètes
        DB = GestionDB.DB()
        req = """SELECT IDarchive, nom_fichier, ID_appareil, date FROM nomade_archivage;"""
        DB.ExecuterReq(req)
        listeArchives = DB.ResultatReq()
        DB.Close()
        
        DB = GestionDB.DB(typeFichier="actions")
        for IDarchive, nom_fichier_archive, ID_appareil_archive, date in listeArchives :
            # Recherche si c'est bien un fichier de sync genere par cet appareil et pour le fichier actuel
            if nom_fichier_archive.startswith("actions_%s" % IDfichier) and ID_appareil_archive == ID_appareil :
                horodatage = nom_fichier_archive.split("_")[2]
                horodatage = UTILS_Dates.HorodatageEnDatetime(horodatage)
                horodatage_str = horodatage.strftime('%Y-%m-%d-%H-%M-%S')
                
                # Suppression de toutes les actions antérieures à l'horodatage """
                for nom_table in ("consommations", "memo_journee") :
                    req = """DELETE FROM %s WHERE horodatage<'%s';""" % (nom_table, horodatage_str)
                    DB.ExecuterReq(req)
                DB.Commit()
        DB.Close()
         
    def EcritLog(self, texte="", etat=True, log=True):
        # Affiche dans l'état
        if etat == True :
            self.ctrl_etat.text = texte
        
        # Affichage dans le log
        if log == True :
            horodatage = time.strftime("%d/%m/%y %H:%M:%S", time.localtime())
            texte = "[%s] %s\n" % (horodatage, texte)
            self.log_sync.text = self.log_sync.text.decode("utf-8") + texte.decode("utf-8")
        
    def SetValeurProgressbar(self, valeur):
        self.progress.value = valeur




        
        
class MyApp(App):
    def build(self):
        screen = Synchronisation(title="Envoi du fichier", app=self)
        return screen
    
    def test(self):
        print("ok")
        


if __name__ == '__main__':
    MyApp().run()