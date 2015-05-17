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
from kivy.logger import Logger
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import get_color_from_hex
from kivy.properties import StringProperty, ListProperty, NumericProperty, ObjectProperty, DictProperty, BooleanProperty
from widgets import BoutonTransparent

import time
import UTILS_Dates
from msgbox import MsgBox


Builder.load_string("""

<BoutonHorloge>:
	text: ''
	size_hint: None, 1
    width: ctrl_image.texture_size[0] + 16
			
    Image:
        id: ctrl_image
        source: 'images/horloge.png'
        size_hint: None, 1
        center: root.center
        



            
<DetailConso>:
    spinner_groupe: spinner_groupe
    ctrl_heure_debut: ctrl_heure_debut
    ctrl_heure_fin: ctrl_heure_fin
    ctrl_quantite_moins: ctrl_quantite_moins
    ctrl_quantite: ctrl_quantite
    ctrl_quantite_plus: ctrl_quantite_plus
    bouton_horloge_heure_debut: bouton_horloge_heure_debut
    bouton_horloge_heure_fin: bouton_horloge_heure_fin
    size_hint: 0.8, 0.8
    #size: 700, 470
    
    BoxLayout:
        orientation: 'vertical'
        padding: 10
        spacing: 10
        
        GridLayout:
            id: grid
            cols: 2
            spacing: 20
            
            Label: 
                text: "Horaires :"
                font_size: 15
                size_hint: 0.2, None
                height: 50
                
            BoxLayout:
                
                Button: 
                    text: ''
                    id: ctrl_heure_debut
                    font_size: 30
                    on_release: root.on_bouton_heure(self)
                
                BoutonHorloge:
                    id: bouton_horloge_heure_debut
                    on_release: root.on_bouton_horloge(ctrl_heure_debut)
                
                Label:
                    text: ''
                    width: 10
                    size_hint: None, 1
                    
                Button:
                    text: ''
                    id: ctrl_heure_fin
                    font_size: 30
                    on_release: root.on_bouton_heure(self)
                
                BoutonHorloge:
                    id: bouton_horloge_heure_fin
                    on_release: root.on_bouton_horloge(ctrl_heure_fin)

            Label: 
                text: "Quantité :"
                font_size: 15
                size_hint: 0.2, None
                height: 50
                
            BoxLayout:
                
                Button: 
                    text: '-'
                    id: ctrl_quantite_moins
                    font_size: 30
                    size_hint: None, 1
                    width: bouton_horloge_heure_fin.width
                    on_release: root.on_bouton_quantite("-")

                Button: 
                    text: '1'
                    id: ctrl_quantite
                    font_size: 30

                Button: 
                    text: '+'
                    id: ctrl_quantite_plus
                    font_size: 30
                    size_hint: None, 1
                    width: bouton_horloge_heure_fin.width
                    on_release: root.on_bouton_quantite("+")

                    
            Label: 
                text: "Etat :"
                font_size: 15
                size_hint: 0.2, None
            
            GridLayout:
                cols: 3
                
                ToggleButton:
                    id: bouton_etat_reservation
                    font_size: 15
                    text: 'Réservation'
                    group: 'etat'
                    state: 'down' if root.etat == 'reservation' else 'normal'
                    on_release: root.etat = 'reservation'

                ToggleButton:
                    id: bouton_etat_attente
                    font_size: 15
                    text: 'Attente'
                    group: 'etat'
                    state: 'down' if root.etat == 'attente' else 'normal'
                    on_release: root.etat = 'attente'

                ToggleButton:
                    id: bouton_etat_refus
                    font_size: 15
                    text: 'Refus'
                    group: 'etat'
                    state: 'down' if root.etat == 'refus' else 'normal'
                    on_release: root.etat = 'refus'

                ToggleButton:
                    id: bouton_etat_present
                    font_size: 15
                    text: 'Présent'
                    group: 'etat'
                    state: 'down' if root.etat == 'present' else 'normal'
                    on_release: root.etat = 'present'

                ToggleButton:
                    id: bouton_etat_absentj
                    font_size: 15
                    text: 'Absence justifiée'
                    group: 'etat'
                    state: 'down' if root.etat == 'absentj' else 'normal'
                    on_release: root.etat = 'absentj'

                ToggleButton:
                    id: bouton_etat_absenti
                    font_size: 15
                    text: 'Absence injustifiée'
                    group: 'etat'
                    state: 'down' if root.etat == 'absenti' else 'normal'
                    on_release: root.etat = 'absenti'


            Label: 
                text: "Groupe :"
                font_size: 15
                size_hint: 0.2, None
                height: 50
            
            Spinner:
                id: spinner_groupe
                font_size: 15
                values: [nom for ordre, nom, IDactivite in root.liste_groupes]
                size_hint: 1, None
                height: 50
        
        Label:
            height: '2dp'
            size_hint: 1, None
            
            canvas.before:
                Color:
                    rgba: 47 / 255., 167 / 255., 212 / 255., 1.
                Rectangle:
                    pos: self.pos
                    size: self.size  

        BoxLayout:
            cols: 4
            size_hint: 1, None
            height: 50
            
            Button:
                text: 'Supprimer'
                font_size: 15
                on_release: root.Supprimer() 
            
            Label:
                text: ''
                
            Button:
                text: 'Ok'
                font_size: 15
                on_release: root.Valider() 
                
            Button:
                text: 'Annuler'
                font_size: 15
                on_release: root.dismiss() 
            
            
""")

class BoutonHorloge(Button):
    def __init__(self, *args, **kwargs):
        super(BoutonHorloge, self).__init__(*args, **kwargs)		



class DetailConso(Popup):
    ctrl_heure_debut = ObjectProperty() 
    ctrl_heure_fin = ObjectProperty() 
    liste_groupes = ListProperty() 
    spinner_groupe = ObjectProperty() 
    etat = StringProperty() 
    
    def __init__(self, *args, **kwargs):
        super(Popup, self).__init__(*args, **kwargs)
        self.callback = kwargs.pop("callback", None)
        self.dictConso = kwargs.pop("dictConso", None)
        self.typeAction = kwargs.pop("typeAction", None)
        self.grille = kwargs.pop("grille", None)
        
        # Importation des données
        if self.dictConso != None :
            
            # Titre
            nomUnite = self.grille.dictUnites[self.dictConso["IDunite"]]["nom"]
            dateStr = UTILS_Dates.DateDDEnFr(self.dictConso["date"])
            self.title = nomUnite + " du " + dateStr
            
            # Etat
            self.etat = self.dictConso["etat"]
            
            # Horaires
            if self.dictConso["heure_debut"] != None :
                self.ctrl_heure_debut.text = self.dictConso["heure_debut"]
            if self.dictConso["heure_fin"] != None :
                self.ctrl_heure_fin.text = self.dictConso["heure_fin"]
            
            if self.grille.dictUnites[self.dictConso["IDunite"]]["heure_debut_fixe"] == 1 :
                self.ctrl_heure_debut.disabled = True
                self.bouton_horloge_heure_debut.disabled = True
            if self.grille.dictUnites[self.dictConso["IDunite"]]["heure_fin_fixe"] == 1 :
                self.ctrl_heure_fin.disabled = True
                self.bouton_horloge_heure_fin.disabled = True
            
            # Quantité
            if self.grille.dictUnites[self.dictConso["IDunite"]]["type"] == "Unitaire" :
                if self.dictConso["quantite"] != None :
                    self.ctrl_quantite.text = str(self.dictConso["quantite"])
            else :
                self.ctrl_quantite_moins.disabled = 1
                self.ctrl_quantite.disabled = 1
                self.ctrl_quantite_plus.disabled = 1
                
            # Remplissage du contrôle Groupe
            self.liste_groupes = []
            nomGroupeSelection = None
            for IDgroupe, dictGroupe in self.grille.dictGroupes.iteritems() :
                self.liste_groupes.append((dictGroupe["ordre"], dictGroupe["nom"], IDgroupe))
                if IDgroupe == self.dictConso["IDgroupe"] :
                    nomGroupeSelection = dictGroupe["nom"]
            self.liste_groupes.sort() 
            if nomGroupeSelection != None :
                self.spinner_groupe.text = nomGroupeSelection
        
    
    def on_bouton_heure(self, ctrl_heure):
        from selection_heure import SelectionHeure
        popup = SelectionHeure(callback=self.SetHeure, ctrl_heure=ctrl_heure, heure=ctrl_heure.text)
        popup.open()    
    
    def SetHeure(self, heure, ctrl_heure):
        ctrl_heure.text = heure
        
    def on_bouton_horloge(self, ctrl_heure):
        heureActuelle = time.strftime('%H:%M', time.localtime())
        ctrl_heure.text = heureActuelle
    
    def on_bouton_quantite(self, valeur):
        quantite = int(self.ctrl_quantite.text)
        if valeur == "+" :
            self.ctrl_quantite.text = str(quantite + 1)
        elif valeur == "-" :
            if quantite > 1 :
                self.ctrl_quantite.text = str(quantite - 1)
        else :
            self.ctrl_quantite.text = str(valeur)
        
    def Valider(self):
        # Récupération des données
        IDgroupe = None
        for ordre, nom, IDgroupeTmp in self.liste_groupes :
            if nom == self.spinner_groupe.text :
                IDgroupe = IDgroupeTmp
        
        heure_debut = self.ctrl_heure_debut.text
        heure_fin = self.ctrl_heure_fin.text
        quantite = int(self.ctrl_quantite.text)
        etat = self.etat
        
        # Vérification de la cohérence des données
        if heure_debut > heure_fin :
            MsgBox.info(text=u"L'heure de début ne peut pas être supérieure à l'heure de fin !", title="Erreur de saisie", size_hint=(0.6, 0.6))
            return False
            
        # Enregistre les modifications dans le dictConso
        self.dictConso["heure_debut"] = heure_debut
        self.dictConso["heure_fin"] = heure_fin
        self.dictConso["quantite"] = quantite
        self.dictConso["etat"] = etat
        self.dictConso["IDgroupe"] = IDgroupe
        
        # Renvoi des données
        if self.callback != None :
            self.callback(typeAction=self.typeAction, dictConso=self.dictConso)
        self.dismiss() 
    
    def Supprimer(self):
        """ Supprimer la consommation """
        # Renvoi des données
        if self.callback != None :
            self.callback(typeAction="supprimer", dictConso=self.dictConso)
        self.dismiss() 

        
        
class MyApp(App):
    def build(self):
        # Génération du popup            
        popup = DetailConso(callback=self.test, typeAction="ajouter", dictConso=None, grille=None)
        popup.open()    
        return popup
        
    def test(self, typeAction="", dictConso=None):
        print("typeAction=" + typeAction + " - dictConso :" + dictConso)
        
if __name__ == '__main__':
    MyApp().run()