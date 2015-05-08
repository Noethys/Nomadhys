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
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import get_color_from_hex
from kivy.core.window import Window


Builder.load_string("""
<SaisieMdp>:
    ctrl_texte: ctrl_texte
    
    id: popup
    size_hint: 0.6, 0.4
    pos_hint: {'center_x': 0.5, 'top': 0.9}
    
    BoxLayout:
        orientation: 'vertical'
        id: box_base
        padding: 10
        spacing: 10
        size_hint: 1, 1
        
        TextInput:
            id: ctrl_texte
            multiline: False
            password: True
            focused: True
            size_hint: 1, 1
            font_size: 22
            text: ""
            on_text_validate: root.Rechercher(ctrl_texte.text)
        
        BoxLayout:
            orientation: 'horizontal'
            id: box_boutons
            spacing: 10
            size_hint: 1, None
            height: 50
            
            Button:
                text: 'Ok'
                on_release: root.Rechercher(ctrl_texte.text)
                
            Button:
                text: 'Annuler'
                on_release: root.dismiss()
                
""")



class SaisieMdp(Popup):
    ctrl_texte = ObjectProperty() 
    def __init__(self, *args, **kwargs):
        super(Popup, self).__init__(*args, **kwargs)	
        self.bind(on_dismiss=self.on_dismiss)
        self.callback = kwargs.pop("callback", None)
        self.code_page = kwargs.pop("code_page", None)
        self.ctrl_texte.focus = True
    
    def Rechercher(self, texte=""):
        if self.callback != None :
            self.callback(texte, self.code_page)
        self.dismiss() 
    
    def on_dismiss(self, *arg):
        Window.release_all_keyboards()
        
        
        
class MyApp(App):
    def build(self):
        # Génération du popup            
        popup = SaisieMdp(title="Saisissez votre mot de passe utilisateur", callback=self.Test, code_page=None)
        popup.open()    
        return popup
        
    def Test(self, texte=None, code_page=None):
        print "mot de passe =", texte
        print "code_page =", code_page
        
if __name__ == '__main__':
    MyApp().run()