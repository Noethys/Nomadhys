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
from kivy.properties import StringProperty, ListProperty, NumericProperty, ObjectProperty, BooleanProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.lang import Builder

import UTILS_Images
import UTILS_Config
import GestionDB
from widgets import BoutonFichier


Builder.load_string("""
<BitmapButtonVertical>:
	id: bouton_test
	text: ''
	height: box_test.height + 0
	size_hint: 1, 1
	#on_release: app.Afficher_page('pointage')
	
	BoxLayout:
		id: box_test
		orientation: 'vertical'
		center: bouton_test.center
		height: label_bouton.height + image_bouton.height
		size_hint: 1, None
		spacing: 5
		
		#canvas.before:
		#	Color:
		#	    rgba: 1, 0.5, 0, 1
		#	Rectangle:
		#	    pos: self.pos
		#	    size: self.size  
			
		Image:
			id: image_bouton
			source: root.chemin_image
			height: 32
			size_hint: 1, None
			
			#canvas.before:
			#	Color:
			#		rgba: 0.5, 0.4, 0, 1
			#	Rectangle:
			#		pos: self.pos
			#		size: self.size  
			
		Label:
			id: label_bouton
			text: root.texte
			height: 20
			size_hint: 1, None
			
			#canvas.before:
			#	Color:
			#		rgba: 0, 0, 1, 1
			#	Rectangle:
			#		pos: self.pos
			#		size: self.size  

			


			
<PageAccueil>:
	bouton_fichier: bouton_fichier
	
    BoxLayout:
        orientation: 'vertical'
		size_hint: 1, 1
        
        AnchorLayout:
            size_hint: 1, 1
            #height: root.height
			
            GridLayout:
                id: content
                cols: 2 if root.width > root.height else 1
				rows: 1 if root.width > root.height else 2
				spacing: 40
                size_hint: .8, None
                height: self.minimum_height if root.width > root.height else 400

                Image:
                    id: logo
                    source: 'images/titre.png'
                    height: 300 if root.width > root.height else 150
                    #padding: 100
                    size_hint_y: None

					
				GridLayout:
					cols: 2
					spacing: 10
					size_hint: 1, 1
					
					BitmapButtonVertical:
						texte: 'Individus'
						chemin_image: 'images/Personnes.png'
						on_release: app.Afficher_page('liste_individus')
						disabled: 1 if not root.app.fichier_valide else 0
						
					BitmapButtonVertical:
						texte: 'Consommations'
						chemin_image: 'images/calendrier1.png'
						on_release: app.Afficher_page('consommations')
						disabled: 1 if not root.app.fichier_valide else 0

					BitmapButtonVertical:
						texte: 'Synchronisation'
						chemin_image: 'images/actualisation.png'
						on_release: app.Afficher_page('synchronisation')
                        disabled: 1 if root.app.IDfichier == '' else 0
					
                    BitmapButtonVertical:
						texte: 'Aide'
						chemin_image: 'images/aide.png'
                        on_release: app.Afficher_page('aide')

                    BitmapButtonVertical:
						texte: 'Paramètres'
						chemin_image: 'images/parametres.png'
						on_release: app.Afficher_page('parametres')
					
					BitmapButtonVertical:
						texte: 'Quitter'
						chemin_image: 'images/quitter.png'
						on_release: app.Quitter()
						

    GridLayout:
        cols: 3
        rows: 1
        row_force_default: True
        row_default_height: 50
        spacing: 5, 5
        padding: 0
        size_hint: 1, None
        height: 50

        canvas.before:
            Color:
                rgb: 0.128, 0.128, 0.128, 1
            Rectangle:
                pos: self.pos
                size: self.size
        
		BoutonFichier:
			id: bouton_fichier
			texte: ''

""")         
            
            
class BitmapButtonVertical(Button):
    texte = StringProperty()
    chemin_image = StringProperty()
    def __init__(self, *args, **kwargs):
        super(BitmapButtonVertical, self).__init__(*args, **kwargs)		

        
class PageAccueil(Screen):
    fullscreen = BooleanProperty(False)
    bouton_individus = ObjectProperty()
    bouton_consommations = ObjectProperty()
    bouton_fichier = ObjectProperty()
    app = ObjectProperty()

    def __init__(self, *args, **kwargs):
        self.name = "menu_principal"
        self.app = kwargs.get("app", None)
        super(Screen, self).__init__(*args, **kwargs)		

    def MAJ(self):
        # Recherche du IDfichier
        config = UTILS_Config.Config()
        IDfichier = config.Lire(section="fichier", option="ID", defaut="")
        config.Close() 
        
        # Si aucun IDfichier chargé
        if IDfichier == "" :
            self.bouton_fichier.texte = "[color=ff3333]Aucun fichier[/color]\nSaisissez un IDfichier dans les paramètres"
            self.bouton_fichier.logo.texture = UTILS_Images.GetTextureFromFichier("images/Erreur.png")
            self.app.fichier_valide = False
            self.app.IDfichier = ""
            return
        
        # Affichage du fichier chargé et du logo
        DB = GestionDB.DB()
        if DB.echec == False :
            # Si fichier présent, recherche du nom et du logo de l'organisateur
            req = "SELECT IDorganisateur, nom, logo FROM organisateur WHERE IDorganisateur=1;"
            DB.ExecuterReq(req)
            listeDonnees = DB.ResultatReq()
            IDorganisateur, nom, logo = listeDonnees[0]
            if logo != None :
                logo = UTILS_Images.GetTextureFromBuffer(logo, avecBord=True)
            # Recherche de l'utilisateur
            nomUtilisateur = "Utilisateur inconnu"
            if self.app.fichier_valide != IDfichier :
                if self.app.nomUtilisateur != "" :
                    nomUtilisateur = self.app.nomUtilisateur
            # MAJ de l'interface
            self.bouton_fichier.texte = nom + "\n[color=a8ca2f]" + nomUtilisateur + "[/color]"
            self.bouton_fichier.logo.texture = logo
            self.app.fichier_valide = True
            self.app.IDfichier = IDfichier

        else :
            # Si IDfichier ok mais aucun fichier présent
            self.bouton_fichier.texte = "[color=ff3333]IDfichier saisi[/color]\nSynchronisez maintenant pour recevoir la base"
            self.bouton_fichier.logo.texture = UTILS_Images.GetTextureFromFichier("images/Erreur.png")
            self.app.fichier_valide = False
            self.app.IDfichier = IDfichier
        DB.Close() 


		
		
class MyApp(App):
    def build(self):
        mainView = PageAccueil()
        return mainView


if __name__ == '__main__':
    MyApp().run()