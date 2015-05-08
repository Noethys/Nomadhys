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
from kivy.adapters.dictadapter import DictAdapter, ListAdapter
from kivy.uix.listview import ListItemButton, ListItemLabel, CompositeListItem, ListView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.properties import ListProperty, StringProperty, ObjectProperty, NumericProperty

import UTILS_Dates
import GestionDB


Builder.load_string("""
#:import ListAdapter kivy.adapters.listadapter.ListAdapter
#:import lv kivy.uix.listview
#:import Factory kivy.factory.Factory

<ListItemActivite>:
    height: '48sp'
    size_hint: 1, None

    BoxLayout:
        padding: 5, 0, 5, 0
		
        Button:
            text: root.label
            size_hint: 1, 1
            color: (0.65, 0.79, 0.18, 1) if root.popup.selectionActivite == root.IDactivite else (1, 1, 1, 1)
			on_release: root.popup.On_Selection(root.index)

        #Button:
        #    text: root.date_debut
        #    size_hint: 0.3, 1
		#	on_release: root.popup.On_Selection(root.index)

        #Button:
        #    text: root.date_fin
        #    size_hint: 0.3, 1
		#	on_release: root.popup.On_Selection(root.index)

            
<SelectionActivite>:
    ctrl_listview: ctrl_listview
    id: popup
    
    BoxLayout:
        orientation: 'vertical'
        id: box_base
        padding: 10
        spacing: 10
        size_hint: 1, 1
        
        ListView:
		    id: ctrl_listview
			padding: 5
		    size_hint: 1, 1
			adapter: ListAdapter(data=root.data, args_converter=root.args_converter, cls=Factory.ListItemActivite)
                
""")

        
class ListItemActivite(BoxLayout):
    index = NumericProperty()
    popup = ObjectProperty()
    IDactivite = NumericProperty()
    label = StringProperty()
    nom = StringProperty()
    date_debut = StringProperty()
    date_fin = StringProperty()

            
class SelectionActivite(Popup):
    data = ListProperty()
    
    def __init__(self, *args, **kwargs):
        super(Popup, self).__init__(*args, **kwargs)
        self.callback = kwargs.pop("callback", None)
        self.selectionActivite = kwargs.pop("IDactivite", None)
        
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
        for IDactivite, nom, date_debut, date_fin in listeTemp :
            date_debut = UTILS_Dates.DateEngFr(date_debut)
            date_debut = UTILS_Dates.DateEngFr(date_fin)
            label = nom
            self.data.append(
                {"IDactivite":IDactivite, "nom":nom, "nom":nom, 
                "label":label, "date_debut":date_debut, "date_fin":date_fin}
                )
        
        # Envoi des données vers le listview
        self.ctrl_listview.adapter.bind(on_selection_change=self.On_Selection)
        
        
    def args_converter(self, row_index, item):
        return {
            'popup': self,
            'IDactivite': item['IDactivite'],
            'nom': item['nom'],
            'label': item['label'],
            'date_debut': item['date_debut'],
            'date_fin': item['date_fin'],
            'index' : row_index,
            }

    def On_Selection(self, index=None):
        dictActivite = self.data[index]
        if self.callback != None :
            self.callback(dictActivite["IDactivite"])
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