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
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.rst import RstDocument
from kivy.uix.tabbedpanel import TabbedPanelItem

LISTE_TEXTES = [
("Commencer", """
Vous découvrez [color=a8ca2f][b]Nomadhys[/color][/b] pour la première fois ? Voici comment commencer...

1. Cliquez sur le bouton **Paramètres** du menu principal puis sur la ligne **IDfichier**. Saisissez les 17 caractères du fichier de données Noethys
avec lequel vous souhaitez travailler. Vous trouverez ce code dans Noethys (**Menu Fichier > Informations > IDfichier**). Reportez-le sans faire d'erreur.

2. Cliquez sur le bouton **Synchronisation** du menu principal. Sélectionnez le type de transfert souhaité pour cliquer sur le bouton **Recevoir** pour récupérer
le fichier de données de Noethys. En fonction du type de transfert utilisé, vous aurez peut-être besoin de renseigner des paramètres de synchronisation. Pour en savoir davantage, consultez le chapitre **Synchronisation** de l'aide.

L'application est maintenant prête à être utilisée. Il ne vous reste plus qu'à cliquer sur les boutons **Individus** ou **Consommations** pour accéder aux données.

""",),

("Individus", """
texte
""",),

("Consommations", """
texte
""",),

("Synchronisation", """
texte
""",),

]



Builder.load_string("""
<Aide>
    tab_aide: tab_aide
    
    BoxLayout:
        orientation: 'vertical'
        
        TabbedPanel: 
            id: tab_aide
            do_default_tab: False
            tab_width: 150
                                
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
            
class Aide(Screen):
    tab_aide = ObjectProperty() 
    
    def __init__(self, *args, **kwargs):
        super(Screen, self).__init__(*args, **kwargs)	
        self.MAJeffectuee = False
    
    def MAJ(self):
        if self.MAJeffectuee == True :
            return
        listeOnglets = []
        for titre, texte in LISTE_TEXTES :
            onglet = TabbedPanelItem(text=titre)
            doc = RstDocument(text=texte)
            onglet.add_widget(doc)
            self.tab_aide.add_widget(onglet)
            listeOnglets.append(onglet)
        self.tab_aide.switch_to(listeOnglets[0])
        self.MAJeffectuee = True
        
class MyApp(App):
    def build(self):
        screen = Aide()
        screen.MAJ()
        return screen
    
    def test(self):
        print("ok")
        


if __name__ == '__main__':
    MyApp().run()