# -*- coding: utf-8 -*-
#!/usr/bin/env python

##############################################################
# Application :    Nomadhys, application nomade pour Noethys #
# Site internet :  www.noethys.com                           #
# Auteur:          Ivan LUCAS                                #
# Copyright:       (c) 2010-15 Ivan LUCAS                    #
# Licence:         Licence GNU GPL                           #
##############################################################

from time import time
from kivy.app import App
from os.path import dirname, join
from kivy.properties import NumericProperty, StringProperty, BooleanProperty, ListProperty, DictProperty, ObjectProperty
from kivy.clock import Clock
from kivy.core.window import Window

from msgbox import MsgBox
from saisie_mdp import SaisieMdp

import GestionDB
import UTILS_Images
import UTILS_Config
import os
import sys

runpath = os.path.dirname(os.path.realpath(sys.argv[0]))
os.chdir(runpath)

# Definition de l'icon app
from kivy.config import Config
Config.set('kivy', 'window_icon', 'images/logo.png')

from page_accueil import PageAccueil
from liste_individus import ListeIndividus
from grille import Grille
from synchronisation import Synchronisation
from parametres import Popup_parametres
from aide import Aide
            
		
class Nomadhys(App):
    pages_spinner = ListProperty([])
    higherarchy = ListProperty([])
    icon = "images/logo.png"
    dictPhotos = DictProperty({})
    fichier_valide = BooleanProperty(False) 
    IDfichier = StringProperty() 
    IDutilisateur = NumericProperty(0)
    nomUtilisateur = StringProperty() 
    
    def build(self):
        self.title = "Nomadhys"
        print "Repertoire user_data_dir =", self.user_data_dir
        
        self.ctrl_multipages = self.root.ids.ctrl_multipages
        
		# Init pages
        self.dict_pages = {
            "menu_principal" : {"label" : "Menu principal", "source" : "", "page" : PageAccueil(app=self)},
            "liste_individus" : {"label" : "Individus", "source" : "", "page" : ListeIndividus(app=self)},
            "consommations" : {"label" : "Consommations", "source" : "", "page" : Grille(app=self)},
            "synchronisation" : {"label" : "Synchronisation", "source" : "", "page" : Synchronisation(app=self)},
            "aide" : {"label" : "Aide", "source" : "", "page" : Aide()},
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
        
    def on_pause(self):
        return True

    def on_resume(self):
        pass

    def on_stop(self):
        pass		
						
    def Afficher_page(self, code_page="", label_page="", direction='left'):
        if self.code_page == "consommations" :
            self.dict_pages["consommations"]["page"].On_leave()
        
        if code_page == "parametres" :
            popup = Popup_parametres(callback=self.MAJ_page)
            popup.open() 
            return
            
        # Chargement d'une page depuis son label
        if label_page != "" :
            for code_page, dictPage in self.dict_pages.iteritems() : 
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
    
    def VerifieMdp(self, mdp="", code_page=None):
        # Vérification du mot de passe utilisateur
        DB = GestionDB.DB() 
        req = "SELECT IDutilisateur, nom, prenom FROM utilisateurs WHERE mdp='%s';" % mdp
        DB.ExecuterReq(req)
        listeDonnees = DB.ResultatReq()
        DB.Close() 
        if len(listeDonnees) > 0 :
            self.IDutilisateur, nom, prenom = listeDonnees[0]
            self.nomUtilisateur = "%s %s" % (nom, prenom)
        else :
            self.IDutilisateur == 0
            self.nomUtilisateur = ""
        
        if self.IDutilisateur == 0 :
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
        if self.dict_pages[code_page]["page"] != None :
            page = self.dict_pages[code_page]["page"]
        else :
            if source.endswith(".kv") : 
                page = Builder.load_file(self.dict_pages[code_page]["source"])
            else :
                page = Builder.load_string(self.dict_pages[code_page]["source"])
                
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
    
    def on_pause(self):
        if self.code_page == "consommations" :
            self.dict_pages["consommations"]["page"].Enregistrer()
        return True
        
    def on_stop(self):
        if self.code_page == "consommations" :
            self.dict_pages["consommations"]["page"].Enregistrer()
        return True

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
