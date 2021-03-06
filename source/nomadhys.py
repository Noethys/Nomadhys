﻿# -*- coding: utf-8 -*-
#!/usr/bin/env python

##############################################################
# Application :    Nomadhys, application nomade pour Noethys #
# Site internet :  www.noethys.com                           #
# Auteur:          Ivan LUCAS                                #
# Copyright:       (c) 2010-15 Ivan LUCAS                    #
# Licence:         Licence GNU GPL                           #
##############################################################

# Logger.info('Application: This is a info message.')
# logging levels : trace, debug, info, warning, error and critical


import time
HEURE_CHARGEMENT = time.time() 

from kivy.app import App
from kivy.logger import Logger
from os.path import dirname, join
from kivy.properties import NumericProperty, StringProperty, BooleanProperty, ListProperty, DictProperty, ObjectProperty
from kivy.clock import Clock
from kivy.core.window import Window
#Window.softinput_mode = "pan"

from msgbox import MsgBox
from saisie_mdp import SaisieMdp

try :
    from Crypto.Hash import SHA256
    IMPORT_SHA256 = True
except:
    Logger.warning('Application: Crypto.Hash.SHA256 non disponible')
    IMPORT_SHA256 = False

import GestionDB
import UTILS_Images
import UTILS_Config
import UTILS_Divers
import os
import sys
import shutil

runpath = os.path.dirname(os.path.realpath(sys.argv[0]))
os.chdir(runpath)

# Definition de l'icon app
from kivy.config import Config
Config.set('kivy', 'window_icon', 'icon.png')

from page_accueil import PageAccueil
from liste_individus import ListeIndividus
from grille import Grille
from synchronisation import Synchronisation
from parametres import Popup_parametres
from aide import Aide
            
		
class Nomadhys(App):
    pages_spinner = ListProperty([])
    higherarchy = ListProperty([])
    icon = "icon.png"
    dictPhotos = DictProperty({})
    fichier_valide = BooleanProperty(False) 
    IDfichier = StringProperty() 
    IDutilisateur = NumericProperty(0)
    nomUtilisateur = StringProperty() 
    mdpUtilisateur = StringProperty() 
    
    def build(self):
        self.title = "Nomadhys"
        Logger.info('Application: Repertoire user_data_dir = %s' % self.user_data_dir)
        
        # Deplacement de fichiers si besoin
        for fichier in os.listdir(self.user_data_dir):
            for prefixe in ("nomadhysactions", "nomadhysconfig", "nomadhysdata"):
                if fichier.startswith(prefixe):
                    nouveaufichier = os.path.join(UTILS_Divers.GetRepData(), fichier.replace("nomadhys", ""))
                    Logger.info("Deplacement du fichier %s -> %s" % (fichier, nouveaufichier))
                    shutil.move(os.path.join(self.user_data_dir, fichier), nouveaufichier)

        # Config
        config = UTILS_Config.Config()
        
        # Verifie si fichier de config bien genere
        config.Verification()
        
        # Importe le code utilisateur si besoin
        memoriser_code = config.Lire(section="utilisateur", option="memoriser_code", defaut="")
        code_utilisateur = config.Lire(section="utilisateur", option="code", defaut="")
        if memoriser_code == "1" and code_utilisateur != "" :
            self.VerifieMdp(mdp=code_utilisateur, silencieux=True)

        config.Close() 
        
        # Init pages
        self.ctrl_multipages = self.root.ids.ctrl_multipages
        self.dict_pages = {
            "menu_principal" : {"label" : "Menu principal", "page" : PageAccueil(app=self)},
            "liste_individus" : {"label" : "Individus", "page" : ListeIndividus(app=self)},
            "consommations" : {"label" : "Consommations", "page" : Grille(app=self)},
            "synchronisation" : {"label" : "Synchronisation", "page" : Synchronisation(app=self)},
            "aide" : {"label" : "Aide", "page" : Aide()},
            }

        # Init spinner de l'actionBar
        self.pages_spinner = [
            "menu_principal",
            "liste_individus",
            "consommations",
            "synchronisation",
            "aide"
            ]
        
        # Affichage du menu principal
        self.code_page = ""
        self.Afficher_page("menu_principal")
        
        # Binds
        Window.bind(on_keyboard=self.OnKey)
        
        TEMPS_CHARGEMENT = time.time() - HEURE_CHARGEMENT
        Logger.info('Application: Temps de chargement = %s' % TEMPS_CHARGEMENT )

    def Afficher_page(self, code_page="", label_page="", direction='left'):
        if self.code_page == "consommations" :
            self.dict_pages["consommations"]["page"].On_leave()
        
        if code_page == "parametres" :
            popup = Popup_parametres(callback=self.MAJ_page)
            popup.open() 
            return
            
        # Chargement d'une page depuis son label
        if label_page != "" :
            for code_page, dictPage in self.dict_pages.items() :
                if dictPage["label"] == label_page : 
                    break
        # Chargement d'une page depuis son code
        if self.code_page == code_page :
            return
        
        # Vérifications avant chargement page
        if code_page in ("liste_individus", "consommations") :
            # Vérifie qu'un fichier de données est chargé
            if self.fichier_valide == False :
                MsgBox.info(text="Action impossible : Aucun fichier n'est chargé !", title="Erreur", size_hint=(0.6, 0.6))
                return
            # Vérifie que l'utilisateur est identifié
            if self.IDutilisateur == 0 :
                popup = SaisieMdp(title="Saisissez votre mot de passe utilisateur", callback=self.VerifieMdp, code_page=code_page)
                popup.open()    
                return
                
        # Chargement de la page
        self.Charger_page(code_page, direction=direction)
    
    def VerifieMdp(self, mdp="", code_page=None, silencieux=False):
        # Vérification du mot de passe utilisateur
        if IMPORT_SHA256 :
            mdpcrypt = SHA256.new(mdp.encode('utf-8')).hexdigest()
        else :
            mdpcrypt = ""
        DB = GestionDB.DB()
        req = "SELECT IDutilisateur, nom, prenom FROM utilisateurs WHERE mdp='%s' or mdp='%s';" % (mdpcrypt, mdp)
        DB.ExecuterReq(req)
        listeDonnees = DB.ResultatReq()
        DB.Close() 
        if len(listeDonnees) > 0 :
            self.IDutilisateur, nom, prenom = listeDonnees[0]
            self.nomUtilisateur = "%s %s" % (nom, prenom)
            self.mdpUtilisateur = mdp
        else :
            self.IDutilisateur == 0
            self.nomUtilisateur = ""
            self.mdpUtilisateur = ""
        
        if self.IDutilisateur == 0 and silencieux == False :
            MsgBox.info(text="Le mot de passe utilisateur n'est pas valide !", title="Accès refusé", size_hint=(0.6, 0.6))
            return
            
        # Chargement de la page souhaitée
        if code_page != None :
            self.Charger_page(code_page)
    
    def MAJ_page(self, code_page="menu_principal"):
        self.dict_pages[code_page]["page"].MAJ()
        
    def AfficherPageFromObjet(self, ctrl=None):
        self.Afficher_page(code_page=ctrl.id)
    
    def Charger_page(self, code_page="", direction='left'):
        # Recherche de la page
        page = self.dict_pages[code_page]["page"]
        
        # Actualisation de l'affichage
        self.dict_pages[code_page]["page"] = page
        self.code_page = code_page
        page.MAJ() 
        self.ctrl_multipages.switch_to(page, direction=direction)
        
        return page

    def go_higherarchy_previous(self):
        ahr = self.higherarchy
        if len(ahr) == 1:
            return
        if ahr:
            ahr.pop()
        if ahr:
            code_page = ahr.pop()
            self.Afficher_page(code_page, direction='right')

    def Quitter(self, obj=None):
        MsgBox.question(text="Souhaitez-vous vraiment quitter Nomadhys ?", title="Quitter", yes_callback=lambda: self.stop(), size_hint=(0.6, 0.6))	
        
    def on_resume(self):
        pass
    
    def on_pause(self):
        self.Enregistrer()
        return True
        
    def on_stop(self):
        self.Enregistrer()
        self.root_window.close()
        return True
    
    def Enregistrer(self):
        # Sauvegarde des consommations
        if self.code_page == "consommations" :
            self.dict_pages["consommations"]["page"].Enregistrer()
        # Sauvegarde de l'utilisateur
        config = UTILS_Config.Config()
        memoriser_code = config.Lire(section="utilisateur", option="memoriser_code", defaut="")
        if memoriser_code == "1" and self.mdpUtilisateur != "" :
            config.Ecrire(section="utilisateur", option="code", valeur=self.mdpUtilisateur)
        else :
            config.Ecrire(section="utilisateur", option="code", valeur="")
        config.Close() 
        
    def OnKey(self, window, key, *args):
        """ Pour intercepter le bouton Retour de Android """
        if key == 27:
            if self.code_page == "menu_principal" :
                self.Quitter()
            else :
                self.go_higherarchy_previous()
            return True
        return False      

        
if __name__ == '__main__':
    Nomadhys().run()
