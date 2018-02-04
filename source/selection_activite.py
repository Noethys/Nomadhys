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
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.properties import ListProperty, StringProperty, ObjectProperty, NumericProperty

from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty, NumericProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior

import UTILS_Dates
import GestionDB


Builder.load_string("""
#:import Factory kivy.factory.Factory
#:import NumericProperty kivy.properties.NumericProperty

<Activite>:
    index: 0
    idactivite: NumericProperty()
    nom: ""
    spacing: "10dp"
    canvas.before:
        Color:
            rgb: (.19, 0.64, .8) if self.selected else (1, 1, 1)
        Rectangle:
            pos: self.pos
            size: self.size
    Label:
        font_size: "18sp"
        text: "  " + root.nom
        color: (0, 0, 0, 1)
        text_size: (self.width, None)

            
<SelectionActivite>:
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
            viewclass: 'Activite'
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


class Activite(RecycleDataViewBehavior, BoxLayout):
    """ Add selection support to the Label """
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        """ Catch and handle the view changes """
        self.index = index
        return super(Activite, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        """ Add selection on touch down """
        if super(Activite, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        """ Respond to the selection of items in the view. """
        self.selected = is_selected

            
class SelectionActivite(Popup):
    data = ListProperty()
    
    def __init__(self, *args, **kwargs):
        super(Popup, self).__init__(*args, **kwargs)
        self.callback = kwargs.pop("callback", None)
        self.selectionActivite = kwargs.pop("IDactivite", None)
        self.ctrl_listview.layout_manager.bind(selected_nodes=self.selectionChange)

        # Importation des activités
        DB = GestionDB.DB()
        req = """SELECT IDactivite, nom, date_debut, date_fin
        FROM activites 
        ORDER BY date_fin DESC;"""
        DB.ExecuterReq(req)
        listeTemp = DB.ResultatReq()
        DB.Close() 
        
        # Préparation des données
        self.data = []
        self.dictActivites = {}
        index = 0
        selection = None
        for IDactivite, nom, date_debut, date_fin in listeTemp :
            date_debut = UTILS_Dates.DateEngFr(date_debut)
            date_debut = UTILS_Dates.DateEngFr(date_fin)
            label = nom
            if IDactivite == self.selectionActivite :
                selection = index
            dictActivite = (
                {"IDactivite":IDactivite, "nom":nom, "nom":nom, 
                "label":label, "date_debut":date_debut, "date_fin":date_fin}
                )
            self.data.append(dictActivite)
            self.dictActivites[IDactivite] = dictActivite
            index += 1

        self.ctrl_listview.data = self.data
        if selection != None :
            self.controller.select_node(selection)

    def selectionChange(self, inst, val):
        if len(val) > 0 :
            index = val[0]
            IDactivite = self.ctrl_listview.data[index]['IDactivite']
            if self.callback != None:
                self.callback(IDactivite)
            self.dismiss()

        
        
class MyApp(App):
    def build(self):
        # Génération du popup            
        popup = SelectionActivite(title="Sélectionnez une activité", IDactivite=1, callback=self.test, size_hint=(0.8, 0.8))
        popup.open()    
        return popup
        
    def test(self, dictActivite=None):
        print("Activité choisie :" + str(dictActivite))
        
if __name__ == '__main__':
    MyApp().run()