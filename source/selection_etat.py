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
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import get_color_from_hex


LISTE_ETATS = [
    ("reservation", "Réservation"),
    ("present", "Présent"),
    ("absentj", "Absence justifiée"),
    ("absenti", "Absence injustifiée"),
    ("attente", "Attente"),
    ("refus", "Refus"),
    ]

def GetLabelEtat(code=""):
    for codeTemp, label in LISTE_ETATS :
        if codeTemp == code :
            return label
    return None
    

Builder.load_string("""
<Tableau>:
    id: tableau
    padding: 10
    cols: 2
""")

class Tableau(GridLayout):
    def __init__(self, *args, **kwargs):
        super(Tableau, self).__init__(*args, **kwargs)		


class SelectionEtat(Popup):
    def __init__(self, *args, **kwargs):
        super(Popup, self).__init__(*args, **kwargs)
        self.selectionEtat = kwargs.pop("etat", None)
        self.bind(on_dismiss=self.on_dismiss)
        self.callback = kwargs.pop("callback", None)
        
        self.grid_base = Tableau()  
        
        for code, label in LISTE_ETATS :
            if self.selectionEtat == code :
                couleur = (0.65, 0.79, 0.18, 1) 
            else :
                couleur = (1, 1, 1, 1)
            b = Button(text=label, id=code, color=couleur, font_size=20, size_hint=(1, 1))
            self.grid_base.add_widget(b) 
            b.bind(on_release=self.on_release)
                
        self.add_widget(self.grid_base) 
    
    def on_release(self, ctrl):
        etat = ctrl.id
        if self.callback != None :
            self.callback(etat)
        self.dismiss() 

    def on_dismiss(self, *arg):
        pass
        
        
class MyApp(App):
    def build(self):
        # Génération du popup            
        popup = SelectionEtat(title="Sélectionnez un état", etat="present", callback=self.test, size_hint=(0.8, 0.8))
        popup.open()    
        return popup
        
    def test(self, etat=None):
        print("Etat choisi :" + etat)
        
if __name__ == '__main__':
    MyApp().run()