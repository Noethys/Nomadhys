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
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.properties import ListProperty, StringProperty, ObjectProperty, NumericProperty
from kivy.uix.button import Button
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty, NumericProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior

import UTILS_Dates
import UTILS_Divers
import GestionDB


Builder.load_string("""
#:import Factory kivy.factory.Factory
#:import NumericProperty kivy.properties.NumericProperty
#:import StringProperty kivy.properties.StringProperty

<Standard>:
    index: 0
    filtre: StringProperty()
    nom: ""
    spacing: "10dp"
    canvas.before:
        Color:
            rgb: (.19, 0.64, .8) if self.selected else (.4, .4, .4, 1)
        Rectangle:
            pos: self.pos
            size: self.size
    Label:
        font_size: "18sp"
        text: "  " + root.nom
        color: (1, 1, 1, 1)
        text_size: (self.width, None)


<Groupe>:
    index: 0
    idgroupe: NumericProperty()
    nom: ""
    spacing: "10dp"
    canvas.before:
        Color:
            rgb: (.19, 0.64, .8) if self.selected else (.4, .4, .4, 1)
        Rectangle:
            pos: self.pos
            size: self.size
    Label:
        font_size: "18sp"
        text: "  " + root.nom
        color: (1, 1, 1, 1)
        text_size: (self.width, None)


<Ecole>:
    index: 0
    idecole: NumericProperty()
    nom: ""
    spacing: "10dp"
    canvas.before:
        Color:
            rgb: (.19, 0.64, .8) if self.selected else (.4, .4, .4, 1)
        Rectangle:
            pos: self.pos
            size: self.size
    Label:
        font_size: "18sp"
        text: "  " + root.nom
        color: (1, 1, 1, 1)
        text_size: (self.width, None)


<Classe>:
    index: 0
    idclasse: NumericProperty()
    nom: ""
    nom_ecole: ""
    spacing: "10dp"
    canvas.before:
        Color:
            rgb: (.19, 0.64, .8) if self.selected else (.4, .4, .4, 1)
        Rectangle:
            pos: self.pos
            size: self.size
    Label:
        font_size: "18sp"
        text: "  " + root.nom
        color: (1, 1, 1, 1)
        text_size: (self.width, None)

    Label:
        font_size: "12sp"
        text: "  " + root.nom_ecole
        color: (0.2, 0.2, 0.2, 1)
        text_size: (self.width, None)

            
<SelectionFiltre>:
    id: popup
    ctrl_standards: ctrl_standards
    ctrl_groupes: ctrl_groupes
    ctrl_classes: ctrl_classes
    ctrl_ecoles: ctrl_ecoles
        
    TabbedPanel: 
        id: tab_aide
        do_default_tab: False
        tab_width: 150
        font_size: 15
        padding: 10
        
        TabbedPanelItem:
            id: tab1
            text: 'Base'

            RecycleView:
                id: ctrl_standards
                scroll_type: ['bars', 'content']
                scroll_wheel_distance: dp(114)
                bar_width: dp(10)
                viewclass: 'Standard'
                SelectableRecycleBoxLayout:
                    id: controller_standards
                    padding: 10
                    margin: 10
                    default_size: None, dp(56)
                    default_size_hint: 1, None
                    size_hint_y: None
                    height: self.minimum_height
                    orientation: 'vertical'
                    spacing: dp(2)


        TabbedPanelItem:
            id: tab2
            text: 'Groupes'

            RecycleView:
                id: ctrl_groupes
                scroll_type: ['bars', 'content']
                scroll_wheel_distance: dp(114)
                bar_width: dp(10)
                viewclass: 'Groupe'
                SelectableRecycleBoxLayout:
                    id: controller_groupes
                    padding: 10
                    margin: 10
                    default_size: None, dp(56)
                    default_size_hint: 1, None
                    size_hint_y: None
                    height: self.minimum_height
                    orientation: 'vertical'
                    spacing: dp(2)

        TabbedPanelItem:
            id: tab3
            text: 'Ecoles'

            RecycleView:
                id: ctrl_ecoles
                scroll_type: ['bars', 'content']
                scroll_wheel_distance: dp(114)
                bar_width: dp(10)
                viewclass: 'Ecole'
                SelectableRecycleBoxLayout:
                    id: controller_ecoles
                    padding: 10
                    margin: 10
                    default_size: None, dp(56)
                    default_size_hint: 1, None
                    size_hint_y: None
                    height: self.minimum_height
                    orientation: 'vertical'
                    spacing: dp(2)

        TabbedPanelItem:
            id: tab4
            text: 'Classes'

            RecycleView:
                id: ctrl_classes
                scroll_type: ['bars', 'content']
                scroll_wheel_distance: dp(114)
                bar_width: dp(10)
                viewclass: 'Classe'
                SelectableRecycleBoxLayout:
                    id: controller_classes
                    padding: 10
                    margin: 10
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


class Standard(RecycleDataViewBehavior, BoxLayout):
    """ Add selection support to the Label """
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        """ Catch and handle the view changes """
        self.index = index
        return super(Standard, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        """ Add selection on touch down """
        if super(Standard, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        """ Respond to the selection of items in the view. """
        self.selected = is_selected


class Groupe(RecycleDataViewBehavior, BoxLayout):
    """ Add selection support to the Label """
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        """ Catch and handle the view changes """
        self.index = index
        return super(Groupe, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        """ Add selection on touch down """
        if super(Groupe, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        """ Respond to the selection of items in the view. """
        self.selected = is_selected


class Ecole(RecycleDataViewBehavior, BoxLayout):
    """ Add selection support to the Label """
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        """ Catch and handle the view changes """
        self.index = index
        return super(Ecole, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        """ Add selection on touch down """
        if super(Ecole, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        """ Respond to the selection of items in the view. """
        self.selected = is_selected


class Classe(RecycleDataViewBehavior, BoxLayout):
    """ Add selection support to the Label """
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        """ Catch and handle the view changes """
        self.index = index
        return super(Classe, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        """ Add selection on touch down """
        if super(Classe, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        """ Respond to the selection of items in the view. """
        self.selected = is_selected



class SelectionFiltre(Popup):
    data = ListProperty()
    
    def __init__(self, **kwargs):
        self.IDactivite = kwargs.pop("IDactivite", None)
        self.date_debut = kwargs.pop("date_debut", None)
        self.date_fin = kwargs.pop("date_fin", None)
        self.callback = kwargs.pop("callback", None)

        super(Popup, self).__init__(**kwargs)
        self.ctrl_standards.layout_manager.bind(selected_nodes=self.OnSelectionStandard)
        self.ctrl_groupes.layout_manager.bind(selected_nodes=self.OnSelectionGroupe)
        self.ctrl_ecoles.layout_manager.bind(selected_nodes=self.OnSelectionEcole)
        self.ctrl_classes.layout_manager.bind(selected_nodes=self.OnSelectionClasse)

        # Filtres standards
        data = []
        data.append({"filtre":"presents", "nom":"Présents"})
        data.append({"filtre":"inscrits", "nom":"Inscrits"})
        self.ctrl_standards.data = data

        DB = GestionDB.DB()

        # Importation des groupes
        if self.IDactivite == None :
            self.IDactivite = 0
        req = """SELECT IDgroupe, nom
        FROM groupes
        WHERE IDactivite=%d
        ORDER BY nom;""" % self.IDactivite
        DB.ExecuterReq(req)
        liste_groupes = DB.ResultatReq()
        data = []
        for IDgroupe, nom in liste_groupes :
            dictGroupe = {"idgroupe":IDgroupe, "nom":nom}
            data.append(dictGroupe)
        self.ctrl_groupes.data = data

        # Importation des classes
        req = """SELECT IDecole, nom
        FROM ecoles
        ORDER BY nom;"""
        DB.ExecuterReq(req)
        liste_ecoles = DB.ResultatReq()
        data = []
        for IDecole, nom in liste_ecoles :
            dictEcole = {"idecole":IDecole, "nom":nom}
            data.append(dictEcole)
        self.ctrl_ecoles.data = data

        req = """SELECT IDniveau, nom, ordre
        FROM niveaux_scolaires
        ORDER BY ordre;"""
        DB.ExecuterReq(req)
        liste_niveaux = DB.ResultatReq()
        dict_niveaux = {}
        for IDniveau, nom, ordre in liste_niveaux :
            dict_niveaux[IDniveau] = {"nom":nom, "ordre":ordre}

        req = """SELECT IDclasse, classes.nom, date_debut, date_fin, niveaux, classes.IDecole, ecoles.nom
        FROM classes 
        LEFT JOIN ecoles ON ecoles.IDecole = classes.IDecole
        WHERE date_debut<='%s' AND date_fin>='%s'
        ORDER BY ecoles.nom, date_debut;""" % (self.date_fin, self.date_debut)
        DB.ExecuterReq(req)
        liste_classes = DB.ResultatReq()
        DB.Close() 

        # Préparation des données
        self.dictClasses = {}
        dictTemp = {}
        index = 0
        for IDclasse, nom, date_debut, date_fin, niveaux, IDecole, nom_ecole in liste_classes :
            niveaux = UTILS_Divers.ConvertStrToListe(niveaux)
            ordres = []
            for IDniveau in niveaux :
                ordres.append(dict_niveaux[IDniveau]["ordre"])
            ordres.sort()
            dictClasse = {
                "idclasse": IDclasse, "nom": nom, "nom_ecole": nom_ecole, "niveaux": niveaux,
                "label": nom, "date_debut": UTILS_Dates.DateEngFr(date_debut), "date_fin": UTILS_Dates.DateEngFr(date_fin), "IDecole": IDecole,
            }
            self.dictClasses[IDclasse] = dictClasse
            key_tri = (IDecole, date_debut, tuple(ordres), IDclasse)
            dictTemp[key_tri] = dictClasse
        index += 1

        keys = list(dictTemp)
        keys.sort()
        self.ctrl_classes.data = [dictTemp[key] for key in keys]

    def OnSelectionStandard(self, inst, val):
        if len(val) > 0 :
            index = val[0]
            filtre = self.ctrl_standards.data[index]['filtre']
            if self.callback != None:
                self.callback("standard", filtre)
            self.dismiss()

    def OnSelectionGroupe(self, inst, val):
        if len(val) > 0 :
            index = val[0]
            IDgroupe = self.ctrl_groupes.data[index]['idgroupe']
            if self.callback != None:
                self.callback("groupe", IDgroupe)
            self.dismiss()

    def OnSelectionEcole(self, inst, val):
        if len(val) > 0 :
            index = val[0]
            IDecole = self.ctrl_ecoles.data[index]['idecole']
            if self.callback != None:
                self.callback("ecole", IDecole)
            self.dismiss()

    def OnSelectionClasse(self, inst, val):
        if len(val) > 0 :
            index = val[0]
            IDclasse = self.ctrl_classes.data[index]['idclasse']
            if self.callback != None:
                self.callback("classe", IDclasse)
            self.dismiss()

        
        
class MyApp(App):
    def build(self):
        b = Button(on_press=self.show_popup, text="Afficher Popup")
        return b

    def show_popup(self, b):
        popup = SelectionFiltre(title="Sélectionnez un filtre", callback=self.test, size_hint=(0.8, 0.8))
        popup.open()    
        return popup
        
    def test(self, categorie=None, id=None):
        print("Filtre choisi :", categorie, id)

if __name__ == '__main__':
    MyApp().run()