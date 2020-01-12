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
from kivy.logger import Logger
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import get_color_from_hex
from kivy.core.window import Window


Builder.load_string("""
<SaisieMemoJournalier>:
    ctrl_texte: ctrl_texte

    id: popup
    size_hint: 0.8, 0.5
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
            focused: True
            size_hint: 1, 1
            font_size: 22
            text: ""
            on_text_validate: root.Valider(ctrl_texte.text)

        BoxLayout:
            orientation: 'horizontal'
            id: box_boutons
            spacing: 10
            size_hint: 1, None
            height: 80

            Button:
                text: 'Ok'
                on_release: root.Valider(ctrl_texte.text)

            #Button:
            #    text: 'Annuler'
            #    on_release: root.dismiss()

""")




class SaisieMemoJournalier(Popup):
    ctrl_recherche = ObjectProperty()

    def __init__(self, **kwargs):
        texte = kwargs.pop("texte", "")
        self.callback = kwargs.pop("callback", None)
        super(SaisieMemoJournalier, self).__init__(**kwargs)
        self.bind(on_dismiss=self.on_dismiss)
        self.ctrl_texte.focus = True
        self.ctrl_texte.text = texte

    def Valider(self, texte=""):
        if self.callback != None :
            self.callback(texte)
        self.dismiss()

    def on_dismiss(self, *arg):
        Window.release_all_keyboards()




class MyApp(App):
    def build(self):
        b = Button(on_press=self.show_popup, text="Afficher Popup")
        return b

    def show_popup(self, b):
        popup = SaisieMemoJournalier(title="Saisissez le texte du mémo journalier", texte="bonjour", callback=self.test)
        popup.open()

    def test(self, texte=None):
        print("texte choisi :", texte)


if __name__ == '__main__':
    MyApp().run()