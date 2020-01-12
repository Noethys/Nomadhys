# -*- coding: utf-8 -*-
#!/usr/bin/env python

##############################################################
# Application :    Nomadhys, application nomade pour Noethys #
# Site internet :  www.noethys.com                           #
# Auteur:          Ivan LUCAS                                #
# Copyright:       (c) 2010-18 Ivan LUCAS                    #
# Licence:         Licence GNU GPL                           #
##############################################################

import kivy
from kivy.app import App
from kivy.logger import Logger
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty, StringProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior



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
#:import Factory kivy.factory.Factory
#:import StringProperty kivy.properties.StringProperty

<Etat>:
    index: 0
    code: StringProperty()
    label: ""
    spacing: "10dp"
    canvas.before:
        Color:
            rgb: (.19, 0.64, .8) if self.selected else (.4, .4, .4, 1)
        Rectangle:
            pos: self.pos
            size: self.size
    Label:
        font_size: "18sp"
        text: "  " + root.label
        color: (1, 1, 1, 1)
        text_size: (self.width, None)


<SelectionEtat>:
    ctrl_listview: ctrl_listview
    controller: controller
    id: popup

    BoxLayout:
        orientation: 'vertical'
        id: box_base
        padding: 10
        spacing: 10
        size_hint: 1, 1

        RecycleView:
            id: ctrl_listview
            scroll_type: ['bars', 'content']
            scroll_wheel_distance: dp(114)
            bar_width: dp(10)
            viewclass: 'Etat'
            SelectableRecycleBoxLayout:
                id: controller
                default_size: None, dp(56)
                default_size_hint: 1, None
                size_hint_y: None
                height: self.minimum_height
                orientation: 'vertical'
                spacing: dp(2)

""")


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
    """ Adds selection and focus behaviour to the view. """
    selected_value = StringProperty('')


class Etat(RecycleDataViewBehavior, BoxLayout):
    """ Add selection support to the Label """
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        """ Catch and handle the view changes """
        self.index = index
        return super(Etat, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        """ Add selection on touch down """
        if super(Etat, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        """ Respond to the selection of items in the view. """
        self.selected = is_selected



class SelectionEtat(Popup):
    def __init__(self, **kwargs):
        self.selectionEtat = kwargs.pop("etat", None)
        self.callback = kwargs.pop("callback", None)

        super(Popup, self).__init__(**kwargs)
        self.ctrl_listview.layout_manager.bind(selected_nodes=self.selectionChange)

        # Préparation des données
        self.data = []
        self.dictEtats = {}
        index = 0
        selection = None
        for code, label in LISTE_ETATS :
            dictEtat = ({"code":code, "label":label})
            if code == self.selectionEtat :
                selection = index
            self.data.append(dictEtat)
            self.dictEtats[code] = dictEtat
            index += 1

        self.ctrl_listview.data = self.data
        if selection != None :
            self.controller.select_node(selection)

    def selectionChange(self, inst, val):
        if len(val) > 0 :
            index = val[0]
            etat = self.ctrl_listview.data[index]['code']
            if self.callback != None:
                self.callback(etat)
            self.dismiss()

        
class MyApp(App):
    def build(self):
        b = Button(on_press=self.show_popup, text="Afficher Popup")
        return b

    def show_popup(self, b):
        popup = SelectionEtat(title="Sélectionnez un état", etat="present", callback=self.test, size_hint=(0.8, 0.8))
        popup.open()    
        return popup
        
    def test(self, etat=None):
        print("Etat choisi :" + etat)
        
if __name__ == '__main__':
    MyApp().run()