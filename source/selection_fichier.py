# -*- coding: utf-8 -*-
#!/usr/bin/env python

##############################################################
# Application :    Nomadhys, application nomade pour Noethys #
# Site internet :  www.noethys.com                           #
# Auteur:          Ivan LUCAS                                #
# Copyright:       (c) 2010-15 Ivan LUCAS                    #
# Licence:         Licence GNU GPL                           #
##############################################################

import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from msgbox import MsgBox

Builder.load_string("""
<SelectionFichier>:
    filechooser: filechooser
    
    BoxLayout:
        size: root.size
        pos: root.pos
        orientation: "vertical"
        
        FileChooserListView:
            id: filechooser
            
        BoxLayout:
            size_hint_y: None
            height: 50

            Button:
                text: "Ok"
                on_release: root.Valider(filechooser.path, filechooser.selection)
            
            Button:
                text: "Annuler"
                on_release: root.Annuler()
""")



class SelectionFichier(Popup):
    filechooser = ObjectProperty()
    def __init__(self, *args, **kwargs):
        super(Popup, self).__init__(*args, **kwargs)
        self.callback = kwargs.pop("callback", None)
        self.nomFichier = kwargs.pop("nomFichier", None)
        chemin = kwargs.pop("chemin", None)
        if chemin != None :
            self.filechooser.path = chemin
        
    def Annuler(self):
        self.dismiss() 

    def Valider(self, chemin=None, listeFichiers=[]):
        if self.nomFichier != None :
            nomFichier = self.nomFichier
        else :
            if len(listeFichiers) == 0 :
                MsgBox.info(text="Vous devez selectionner un fichier !", title="Erreur", size_hint=(0.6, 0.6))
                return
            nomFichier = listeFichiers[0]
        self.callback(chemin, nomFichier)
        self.dismiss() 
        
        
class MyApp(App):
    def build(self):
        # Génération du popup            
        popup = SelectionFichier(title="Selectionnez un fichier", callback=self.test, size_hint=(0.8, 0.8))
        popup.open()    
        return popup
        
    def test(self, chemin=None, fichier=None):
        print("Fichier choisi :" + str(fichier))
        
if __name__ == '__main__':
    MyApp().run()