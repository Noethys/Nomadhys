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
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty, NumericProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior

import UTILS_Images
import GestionDB


Builder.load_string("""
#:import Factory kivy.factory.Factory
#:import NumericProperty kivy.properties.NumericProperty


<Inscription>:
    index: 0
    idinscription: NumericProperty()
    photo: None
    nom_complet: ""
    spacing: "10dp"
    canvas.before:
        Color:
            rgb: (.19, 0.64, .8) if self.selected else (.4, .4, .4, 1)
        Rectangle:
            pos: self.pos
            size: self.size
    Image:
        texture: root.photo
        size_hint_x: None
        width: self.height
    Label:
        font_size: "18sp"
        text: root.nom_complet
        color: (1, 1, 1, 1)
        text_size: (self.width, None)


<SelectionInscription>:
	name: 'liste_inscriptions'
	id: liste_inscriptions
	ctrl_listview: ctrl_listview
	ctrl_recherche: ctrl_recherche
	grid_alphabet: grid_alphabet
	label_resultats: label_resultats
	controller: controller
    size_hint: 0.8, 0.8
    on_dismiss: self.on_dismiss()

	BoxLayout:
		orientation: 'vertical'
		
		GridLayout:
			rows: 2
			cols: 1
			padding: 10
			spacing: 10, 10

			GridLayout:
				cols: 4
				rows: 1
				spacing: 10, 10
				height: 40
				size_hint: 1, None

				Image:
					source: 'images/recherche.png'
					size_hint: None, 1
					width: 32

				TextInput:
					id: ctrl_recherche
					multiline: False
					#focused: True
					size_hint: 1, 1
					font_size: 22
					text: ""
					on_text_validate: root.Rechercher(self)

				Button:
					id: bouton_recherche
					size_hint: None, 1
					text: "Rechercher"
					font_size: 15
					on_release: root.Rechercher(self)

				Button:
					id: bouton_reinit_recherche
					size_hint: None, 1
					text: "X"
					font_size: 15
					width: 50
					on_release: root.Reinit(self)

            RecycleView:
                id: ctrl_listview
                scroll_type: ['bars', 'content']
                scroll_wheel_distance: dp(114)
                bar_width: dp(10)
                viewclass: 'Inscription'
                SelectableRecycleBoxLayout:
                    id: controller
                    default_size: None, dp(56)
                    default_size_hint: 1, None
                    size_hint_y: None
                    height: self.minimum_height
                    orientation: 'vertical'
                    spacing: dp(2)

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



class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
    """ Adds selection and focus behaviour to the view. """
    selected_value = StringProperty('')


class Inscription(RecycleDataViewBehavior, BoxLayout):
    """ Add selection support to the Label """
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        """ Catch and handle the view changes """
        self.index = index
        return super(Inscription, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        """ Add selection on touch down """
        if super(Inscription, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        """ Respond to the selection of items in the view. """
        self.selected = is_selected


class SelectionInscription(Popup):
    data = ListProperty()
    filtre = StringProperty() 

    def __init__(self, **kwargs):
        self.app = kwargs.get("app", None)
        self.date = kwargs.pop("date", None)
        self.IDactivite = kwargs.pop("IDactivite", None)
        self.callback = kwargs.pop("callback", None)
        super(Popup, self).__init__(**kwargs)
        self.title = "Sélectionnez un individu"
        self.ctrl_recherche.focus = True
        self.ctrl_listview.layout_manager.bind(selected_nodes=self.selectionChange)

    def Remplissage(self):
        self.data = []
        self.dictIndividus = {}

        # Importation
        if self.filtre != "" :
            DB = GestionDB.DB()
            req = """SELECT IDinscription, individus.IDindividu, IDcivilite, nom, prenom, photo, nom||' '||prenom||' '||nom as nomtemp
            FROM inscriptions 
            LEFT JOIN individus ON individus.IDindividu = inscriptions.IDindividu
            WHERE nomtemp LIKE '%%%s%%' 
            AND IDactivite=%d AND (date_desinscription IS NULL OR date_desinscription>='%s')
            ORDER BY nom, prenom;""" % (self.filtre, self.IDactivite, self.date)
            DB.ExecuterReq(req)
            listeDonnees = DB.ResultatReq()
            DB.Close() 
            self.listeIndividus = []
            for IDinscription, IDindividu, IDcivilite, nom, prenom, photo, nomtemp in listeDonnees :
                if photo != None :
                    photo = UTILS_Images.GetTextureFromBuffer(photo, avecBord=True)
                else:
                    if IDcivilite == 1: photo = UTILS_Images.GetTextureFromFichier("images/homme.png")
                    if IDcivilite in (2, 3): photo = UTILS_Images.GetTextureFromFichier("images/femme.png")
                    if IDcivilite == 4: photo = UTILS_Images.GetTextureFromFichier("images/garcon.png")
                    if IDcivilite == 5: photo = UTILS_Images.GetTextureFromFichier("images/fille.png")
                nomComplet = "%s %s" % (nom, prenom)
                dictIndividu = {"IDinscription" : IDinscription, "IDindividu" : IDindividu, "IDcivilite" : IDcivilite, "nom" : nom, "prenom" : prenom, "nom_complet" : nomComplet, "photo" : photo}
                self.data.append(dictIndividu)
                self.dictIndividus[IDindividu] = dictIndividu

        self.ctrl_listview.data = self.data
        self.label_resultats.text = u"%d individus trouvés" % len(self.data)

    def selectionChange(self, inst, val):
        if len(val) > 0 :
            index = val[0]
            IDinscription = self.ctrl_listview.data[index]['IDinscription']
            if self.callback != None:
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
        b = Button(on_press=self.show_popup, text="Afficher Popup")
        return b

    def show_popup(self, b):
        popup = SelectionInscription(IDactivite=1, callback=self.test)
        popup.open()    
        return popup
        
    def test(self, IDinscription=None):
        print("IDinscription choisi :" + str(IDinscription))


if __name__ == '__main__':
    MyApp().run()