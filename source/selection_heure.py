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
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import get_color_from_hex
from kivy.properties import StringProperty, ListProperty, NumericProperty, ObjectProperty, DictProperty, BooleanProperty
from widgets import BoutonTransparent

import time

Builder.load_string("""

<CaseAffichage>
    text: ''
    font_size: 40
    background_normal: ''
    background_color: 1, 1, 1, 0
    
    canvas.before:
        Color:
            rgba: 47 / 255., 167 / 255., 212 / 255., 1.
        Rectangle:
            pos: self.pos
            size: self.size  

        Color:
            rgba: (1, 1, 1, 1) if root.bold else (47 / 255., 167 / 255., 212 / 255., 1.)
        Rectangle:
            pos: self.x+4, self.y+4
            size: self.width-8, 2  

            
            
<BoutonChiffre>
    text: str(root.chiffre)
    size_hint: 1, 1
    font_size: 25
    
    
<SelectionHeure>:
    label_0: label_0
    label_1: label_1
    label_2: label_2
    label_3: label_3
    size_hint: None, None
    size: 350, 500
    
    BoxLayout:
        orientation: 'vertical'
        spacing: 20
        padding: 10
        
        GridLayout:
            cols: 5
            spacing: 10
            size_hint: 1, None
            #height: 30
            
            CaseAffichage:
                id: label_0
                bold: True if root.case_focus == 0 else False
                on_release: root.case_focus = 0
                
            CaseAffichage:
                id: label_1
                bold: True if root.case_focus == 1 else False
                on_release: root.case_focus = 1
            
            Label:
                text: ':'
                size_hint: None, 1
                width: 20
                font_size: 40
                
            CaseAffichage:
                id: label_2
                bold: True if root.case_focus == 2 else False
                on_release: root.case_focus = 2

            CaseAffichage:
                id: label_3
                bold: True if root.case_focus == 3 else False
                on_release: root.case_focus = 3
                
        GridLayout:
            cols: 3
            spacing: 10
            
            BoutonChiffre: 
                chiffre: 7
                on_release: root.on_bouton_chiffre(self.chiffre)
        
            BoutonChiffre: 
                chiffre: 8
                on_release: root.on_bouton_chiffre(self.chiffre)

            BoutonChiffre: 
                chiffre: 9
                on_release: root.on_bouton_chiffre(self.chiffre)

            BoutonChiffre: 
                chiffre: 4
                on_release: root.on_bouton_chiffre(self.chiffre)

            BoutonChiffre: 
                chiffre: 5
                on_release: root.on_bouton_chiffre(self.chiffre)

            BoutonChiffre: 
                chiffre: 6
                on_release: root.on_bouton_chiffre(self.chiffre)

            BoutonChiffre: 
                chiffre: 1
                on_release: root.on_bouton_chiffre(self.chiffre)

            BoutonChiffre: 
                chiffre: 2
                on_release: root.on_bouton_chiffre(self.chiffre)

            BoutonChiffre: 
                chiffre: 3
                on_release: root.on_bouton_chiffre(self.chiffre)

            Button: 
                text: 'Annuler'
                on_release: root.dismiss()

            BoutonChiffre: 
                chiffre: 0
                on_release: root.on_bouton_chiffre(self.chiffre)
                
            Button: 
                text: 'Valider'
                on_release: root.Valider()
        
""")

class CaseAffichage(Button):
    def __init__(self, *args, **kwargs):
        super(CaseAffichage, self).__init__(*args, **kwargs)		

class BoutonChiffre(Button):
    chiffre = NumericProperty()
    def __init__(self, *args, **kwargs):
        super(BoutonChiffre, self).__init__(*args, **kwargs)		
    

class SelectionHeure(Popup):
    case_focus = NumericProperty() 
    label_0 = ObjectProperty() 
    label_1 = ObjectProperty() 
    label_2 = ObjectProperty() 
    label_3 = ObjectProperty()   
    
    def __init__(self, *args, **kwargs):
        super(Popup, self).__init__(*args, **kwargs)
        self.heure = kwargs.pop("heure", None)
        self.callback = kwargs.pop("callback", None)
        self.ctrl_heure = kwargs.pop("ctrl_heure", None)
        self.case_focus = 0
        
        # Importation des données
        self.title = "Saisissez une heure"
        
        # Init affichage
        self.SetHeure(self.heure)
            
    def on_bouton_chiffre(self, chiffre=None):
        if self.case_focus == 0 : 
            if chiffre > 2 : return
            self.label_0.text = str(chiffre)
            self.case_focus += 1
        elif self.case_focus == 1 : 
            if self.label_0.text == "2" and chiffre > 3 : return
            self.label_1.text = str(chiffre)
            self.case_focus += 1
        elif self.case_focus == 2 : 
            if chiffre > 5 : return
            self.label_2.text = str(chiffre)
            self.case_focus += 1
        elif self.case_focus == 3 : 
            self.label_3.text = str(chiffre)
            self.case_focus = 0            
    
    def SetHeure(self, heure="14:30"):
        if heure not in ("", None) :
            self.label_0.text = heure[0]
            self.label_1.text = heure[1]
            self.label_2.text = heure[3]
            self.label_3.text = heure[4]    
    
    def GetHeure(self):
        label0 = self.label_0.text
        label1 = self.label_1.text
        label2 = self.label_2.text
        label3 = self.label_3.text
        heure = "%s%s:%s%s" % (label0, label1, label2, label3)
        return heure
    
    def Valider(self):
        heure = self.GetHeure() 
        if self.callback != None :
            self.callback(heure=heure, ctrl_heure=self.ctrl_heure)
        self.dismiss() 
        
        
        
class MyApp(App):
    def build(self):
        # Génération du popup            
        popup = SelectionHeure(callback=self.test, heure="20:30")
        popup.open()    
        return popup
        
    def test(self, heure=None):
        print("Heure choisie :" + heure)
        
        
if __name__ == '__main__':
    MyApp().run()