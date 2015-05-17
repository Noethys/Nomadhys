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
from kivy.logger import Logger
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import get_color_from_hex


Builder.load_string("""

<SelectionLettre>:
    box_base: box_base
    tableau_lettres: tableau_lettres
    
    BoxLayout:
        orientation: 'vertical'
        id: box_base
        padding: 10
        spacing: 10
        size_hint: 1, 1
        
        TableauLettres:
            id: tableau_lettres
            cols: 4 if root.height > root.width else 6
        
        BoxLayout:
            orientation: 'horizontal'
            id: box_boutons
            spacing: 10
            size_hint: 1, None
            height: 50
                
            Button:
                text: 'Annuler'
                on_release: root.dismiss()

""")

class TableauLettres(GridLayout):
    def __init__(self, *args, **kwargs):
        super(TableauLettres, self).__init__(*args, **kwargs)		


class SelectionLettre(Popup):
    def __init__(self, *args, **kwargs):
        super(SelectionLettre, self).__init__(*args, **kwargs)	
        self.bind(on_dismiss=self.on_dismiss)
        self.callback = kwargs.pop("callback", None)
        
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for lettre in alphabet :
            b = Button(text=lettre, font_size=20, size_hint=(1, 1))
            self.tableau_lettres.add_widget(b) 
            b.bind(on_release=self.on_release)
    
    def on_release(self, event):
        lettre = event.text
        if self.callback != None :
            self.callback(lettre)
        self.dismiss() 

    def on_dismiss(self, *arg):
        pass
        
        
class MyApp(App):
    def build(self):
        # Génération du popup            
        popup = SelectionLettre(title="Sélectionnez une lettre", callback=self.test, size_hint=(0.8, 0.8))
        popup.open()    
        return popup
        
    def test(self, lettre=None):
        print("lettre choisie :"+ lettre)
        
if __name__ == '__main__':
    MyApp().run()