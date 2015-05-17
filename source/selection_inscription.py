# -*- coding: utf-8 -*-
#!/usr/bin/env python

##############################################################
# Application :    Nomadhys, application nomade pour Noethys #
# Site internet :  www.noethys.com                           #
# Auteur:          Ivan LUCAS                                #
# Copyright:       (c) 2010-15 Ivan LUCAS                    #
# Licence:         Licence GNU GPL                           #
##############################################################

from kivy.uix.modalview import ModalView
from kivy.logger import Logger
from kivy.uix.listview import ListView
from kivy.uix.gridlayout import GridLayout
from kivy.properties import StringProperty, ListProperty, NumericProperty, ObjectProperty
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.adapters.dictadapter import DictAdapter
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.listview import ListView, ListItemButton
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.core.window import Window


import UTILS_Images
import GestionDB


Builder.load_string("""
#:import ListAdapter kivy.adapters.listadapter.ListAdapter
#:import lv kivy.uix.listview
#:import Factory kivy.factory.Factory
			
		
<ListItemInscription>:
    height: '48sp'
    size_hint: 1, None

    BoxLayout:
        padding: 5, 0, 5, 0
		
        Button:
            text: root.texte
			on_release: root.clsListeIndividus.On_selection(root.index)

			

<SelectionInscription>:
	name: 'liste_individus'
	list_view: ctrl_listview
	ctrl_recherche: ctrl_recherche
	grid_alphabet: grid_alphabet
	label_resultats: label_resultats
    size_hint: 0.8, 0.8
    on_dismiss: self.on_dismiss()

	GridLayout:
		rows: 3
		cols: 1

        GridLayout:
		    cols: 4
			rows: 1
			row_force_default: True
			row_default_height: 40
			spacing: 5, 5
			padding: 5
			height: self.row_default_height + 10
			size_hint: 1, None
				
            Image:
                source: 'images/recherche.png'
                size_hint: None, None
				width: 32
				
            TextInput:
		        id: ctrl_recherche
				multiline: False
				focused: True
                size_hint: 1, None
				font_size: 22
		        text: ""
				on_text_validate: root.Rechercher(self)

            Button:
			    id: bouton_recherche
                size_hint: None, None
				text: "Rechercher"
				on_release: root.Rechercher(self)

            Button:
			    id: bouton_reinit_recherche
                size_hint: None, None
				text: "X"
				width: 50
				on_release: root.Reinit(self)

				
        ListView:
		    id: ctrl_listview
			padding: 5
		    size_hint: 1, 1
			adapter: ListAdapter(data=root.data, args_converter=root.args_converter, cls=Factory.ListItemInscription)
			
        GridLayout:
			id: grid_alphabet
		    cols: 1
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
				id: label_resultats
				text: "Aucun individu"


""")

	
		
class ListItemInscription(BoxLayout):
    texte = StringProperty()
    index = NumericProperty()
    clsListeIndividus = ObjectProperty() 
				


		
class SelectionInscription(Popup):
    data = ListProperty()
    filtre = StringProperty() 

    def __init__(self, **kwargs):
        self.app = kwargs.get("app", None)
        self.IDactivite = kwargs.pop("IDactivite", None)
        self.callback = kwargs.pop("callback", None)
        super(Popup, self).__init__(**kwargs)
        self.title = "Sélectionnez un individu"
        self.ctrl_recherche.focus = True
		
    def args_converter(self, row_index, item):
        return {
            'texte': item['nomComplet'],
            'index' : row_index,
            'clsListeIndividus' : self,
            'size_hint_y': None,
            'height': 32}
            
    def Remplissage(self):
        self.data = []
        
        # Importation
        if self.filtre != "" :
            DB = GestionDB.DB()
            req = """SELECT IDinscription, individus.IDindividu, IDcivilite, nom, prenom, photo, nom||' '||prenom||' '||nom as nomtemp
            FROM inscriptions 
            LEFT JOIN individus ON individus.IDindividu = inscriptions.IDindividu
            WHERE nomtemp LIKE '%%%s%%' 
            AND IDactivite=%d
            ORDER BY nom, prenom;""" % (self.filtre, self.IDactivite)
            DB.ExecuterReq(req)
            listeDonnees = DB.ResultatReq()
            DB.Close() 
            self.listeIndividus = []
            for IDinscription, IDindividu, IDcivilite, nom, prenom, photo, nomtemp in listeDonnees :
                if photo != None :
                    photo = UTILS_Images.GetTextureFromBuffer(photo, avecBord=True)
                nomComplet = "%s %s" % (nom, prenom)
                dictIndividu = {"IDinscription" : IDinscription, "IDindividu" : IDindividu, "IDcivilite" : IDcivilite, "nom" : nom, "prenom" : prenom, "nomComplet" : nomComplet, "photo" : photo}
                self.data.append(dictIndividu)
                
        self.list_view.scroll_to(0)
        self.label_resultats.text = u"%d individus trouvés" % len(self.data)
				
    def On_selection(self, index=None):
        dictInscription = self.data[index]
        IDinscription = dictInscription["IDinscription"]
        if self.callback != None :
            self.callback(IDinscription)
        self.dismiss() 
    
    def Rechercher(self, *args):
        self.filtre = self.ctrl_recherche.text
        self.Remplissage() 
        Window.release_all_keyboards()
    
    def Reinit(self, *args):
        self.ctrl_recherche.text = ""
        self.filtre = ""
        self.Remplissage() 
        self.ctrl_recherche.focus = True
    
    def on_dismiss(self):
        Window.release_all_keyboards()

		
		
class MyApp(App):
    def build(self):
        # Génération du popup            
        popup = SelectionInscription(IDactivite=1, callback=self.test)
        popup.open()    
        return popup
        
    def test(self, IDinscription=None):
        print("IDinscription choisi :" + IDinscription)


if __name__ == '__main__':
    MyApp().run()