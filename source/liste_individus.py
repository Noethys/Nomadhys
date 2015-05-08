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
from kivy.clock import Clock

from fiche_individu import FicheIndividu


import UTILS_Images
import GestionDB


Builder.load_file("liste_individus.kv")

	
		
class ListItem(BoxLayout):
    texte = StringProperty()
    index = NumericProperty()
    clsListeIndividus = ObjectProperty() 
				


		
class ListeIndividus(Screen):
    data = ListProperty()
    filtre = StringProperty() 

    def __init__(self, **kwargs):
        self.app = kwargs.get("app", None)
        super(Screen, self).__init__(**kwargs)
		
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
            req = """SELECT IDindividu, IDcivilite, nom, prenom, photo, nom||' '||prenom||' '||nom as nomtemp
            FROM individus 
            WHERE nomtemp LIKE '%""" + self.filtre + """%' 
            ORDER BY nom, prenom;""" 
            DB.ExecuterReq(req)
            listeDonnees = DB.ResultatReq()
            DB.Close() 
            self.listeIndividus = []
            for IDindividu, IDcivilite, nom, prenom, photo, nomtemp in listeDonnees :
                if photo != None :
                    photo = UTILS_Images.GetTextureFromBuffer(photo, avecBord=True)
                nomComplet = "%s %s" % (nom, prenom)
                dictIndividu = {"IDindividu" : IDindividu, "IDcivilite" : IDcivilite, "nom" : nom, "prenom" : prenom, "nomComplet" : nomComplet, "photo" : photo}
                self.data.append(dictIndividu)
                
        self.list_view.adapter.bind(on_selection_change=self.On_Selection)
        self.list_view.scroll_to(0)
        self.label_resultats.text = u"%d individus trouvés" % len(self.data)
		
    def On_Selection(self, *args):
        item = args[0].selection[0]
        index = item.index
        texte = item.texte
        item.deselect() 
        self.AfficherIndividu(index)
		
    def AfficherIndividu(self, index=None):
        dictIndividu = self.data[index]
        code_page = "individus_%s" % dictIndividu["IDindividu"]
        page = FicheIndividu(dictIndividu=dictIndividu)
        self.app.dict_pages[code_page] = {"label" : "Individu X", "source" : None, "page" : page}
        self.app.Afficher_page(code_page=code_page, direction='left')        
    
    def Rechercher(self, *args):
        self.filtre = self.ctrl_recherche.text
        self.Remplissage() 
        Window.release_all_keyboards()
    
    def Reinit(self, *args):
        self.ctrl_recherche.text = ""
        self.filtre = ""
        self.Remplissage() 
    
    def MAJ(self):
        self.Reinit() 
        Clock.schedule_once(self.Focus)
    
    def Focus(self, dt):
        self.ctrl_recherche.focused = True
        
        
        
		
class MyApp(App):
    def build(self):
        mainView = ListeIndividus(width=800)
        mainView.MAJ()
        #mainView.ctrl_recherche.text = "e"
        #mainView.Rechercher()
        return mainView


if __name__ == '__main__':
    MyApp().run()