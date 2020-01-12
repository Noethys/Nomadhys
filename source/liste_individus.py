# -*- coding: utf-8 -*-
#!/usr/bin/env python

##############################################################
# Application :    Nomadhys, application nomade pour Noethys #
# Site internet :  www.noethys.com                           #
# Auteur:          Ivan LUCAS                                #
# Copyright:       (c) 2010-18 Ivan LUCAS                    #
# Licence:         Licence GNU GPL                           #
##############################################################

from kivy.logger import Logger
from kivy.properties import StringProperty, ListProperty, NumericProperty, ObjectProperty
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.clock import Clock

from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty, NumericProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior

from fiche_individu import FicheIndividu


import UTILS_Images
import GestionDB

Builder.load_file("liste_individus.kv")



class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
    """ Adds selection and focus behaviour to the view. """
    selected_value = StringProperty('')


class Individu(RecycleDataViewBehavior, BoxLayout):
    """ Add selection support to the Label """
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        """ Catch and handle the view changes """
        self.index = index
        return super(Individu, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        """ Add selection on touch down """
        if super(Individu, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        """ Respond to the selection of items in the view. """
        self.selected = is_selected



class ListeIndividus(Screen):
    data = ListProperty()
    filtre = StringProperty()

    def __init__(self, **kwargs):
        self.app = kwargs.pop("app", None)
        super(ListeIndividus, self).__init__(**kwargs)
        self.ctrl_listview.layout_manager.bind(selected_nodes=self.selectionChange)

    def Remplissage(self):
        self.data = []
        self.dictIndividus = {}

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
                else:
                    if IDcivilite == 1: photo = UTILS_Images.GetTextureFromFichier("images/homme.png")
                    if IDcivilite in (2, 3): photo = UTILS_Images.GetTextureFromFichier("images/femme.png")
                    if IDcivilite == 4: photo = UTILS_Images.GetTextureFromFichier("images/garcon.png")
                    if IDcivilite == 5: photo = UTILS_Images.GetTextureFromFichier("images/fille.png")
                nomComplet = "%s %s" % (nom, prenom)
                dictIndividu = {"idindividu" : IDindividu, "IDcivilite" : IDcivilite, "nom" : nom, "prenom" : prenom, "nom_complet" : nomComplet, "photo" : photo}
                self.data.append(dictIndividu)
                self.dictIndividus[IDindividu] = dictIndividu

        self.ctrl_listview.data = self.data
        self.label_resultats.text = u"%d individus trouvés" % len(self.ctrl_listview.data)

    def selectionChange(self, inst, val):
        if len(val) > 0 :
            index = val[0]
            IDindividu = self.ctrl_listview.data[index]['idindividu']
            self.AfficherIndividu(IDindividu)
            self.controller.clear_selection()

    def AfficherIndividu(self, IDindividu=None):
        dictIndividu = self.dictIndividus[IDindividu]
        code_page = "individus_%s" % dictIndividu["idindividu"]
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
        Clock.schedule_once(self.Focus)
    
    def MAJ(self):
        self.Reinit()

    def Focus(self, dt):
        self.ctrl_recherche.focused = True
        
        
        
		
class MyApp(App):
    def build(self):
        mainView = ListeIndividus(width=800)
        mainView.MAJ()
        mainView.ctrl_recherche.text = "e"
        mainView.Rechercher()
        return mainView


if __name__ == '__main__':
    MyApp().run()