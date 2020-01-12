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
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.properties import  ListProperty

    

Builder.load_string('''

<Case_totaux>:
    markup: True
    height: 40
    size_hint_y: None
    
    canvas.before:
        Color:
            rgb: self.bgcolor
        Rectangle:
            size: self.size
            pos: self.pos
            
''')

class Case_totaux(Label):
    bgcolor = ListProperty([1,1,1])



class Tableau_totaux(GridLayout):
    def __init__(self, **kwargs):
        donnees = kwargs.pop("donnees", None)

        super(Tableau_totaux, self).__init__(**kwargs)
        self.size_hint_y = None
        self.cols = len(donnees[0])
        self.rows = len(donnees)
        self.spacing = 2
        self.bind(minimum_height=self.setter('height'))
        
        numLigne = 0
        for ligne in donnees :
            numCol = 0
            for valeur in ligne :
                if numLigne == 0 and numCol == 0:
                    case = Label(text="")
                elif numLigne == 0 :
                    case = Case_totaux(text="[color=000000][b]%s[/b][/color]" % valeur)
                elif numCol == 0 :
                    case = Case_totaux(text="[color=000000][b]%s[/b][/color]" % valeur)
                else :
                    case = Case_totaux(text="[color=000000]%s[/color]" % valeur)
                self.add_widget(case)
                numCol += 1
            numLigne += 1
        

class Totaux(Popup):
    def __init__(self, **kwargs):
        self.donnees = kwargs.pop("donnees", None)

        super(Popup, self).__init__(**kwargs)
        ctrl_tableau = Tableau_totaux(donnees=self.donnees)
        ctrl_scroll = ScrollView()
        ctrl_scroll.add_widget(ctrl_tableau)
        ctrl_scroll.do_scroll_y = True
        ctrl_scroll.do_scroll_x = False
        
        ctrl_box = BoxLayout(orientation="vertical", padding=10)
        ctrl_box.add_widget(ctrl_scroll) 
        
        self.add_widget(ctrl_box) 
            
        
class MyApp(App):
    def build(self):
        b = Button(on_press=self.show_popup, text="Afficher Popup")
        return b

    def show_popup(self, b):
        donnees = [
            ("", "col1", "col2"),
            ("ligne1", "L1C1", "L1C2"),
            ("ligne2", "L2C1", "L2C2"),
            ("ligne3", "L3C1", "L3C2"),
            ("ligne3", "L3C1", "L3C2"),
            ("ligne3", "L3C1", "L3C2"),
            ("ligne3", "L3C1", "L3C2"),
            ("ligne3", "L3C1", "L3C2"),
            ("ligne3", "L3C1", "L3C2"),
            ]
        # Génération du popup
        popup = Totaux(title="Totaux", donnees=donnees, size_hint=(0.8, 0.8))
        popup.open()    
        return popup
        
        
if __name__ == '__main__':
    MyApp().run()