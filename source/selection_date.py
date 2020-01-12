# -*- coding: utf-8 -*-
#!/usr/bin/env python

##############################################################
# Application :    Nomadhys, application nomade pour Noethys #
# Site internet :  www.noethys.com                           #
# Auteur:          Ivan LUCAS                                #
# Copyright:       (c) 2010-15 Ivan LUCAS                    #
# Licence:         Licence GNU GPL                           #
##############################################################

import datetime
import calendar

import kivy
from kivy.app import App
from kivy.logger import Logger
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import get_color_from_hex


class SelectionDate(Popup):
    def __init__(self, **kwargs):
        self.callback = kwargs.pop("callback", None)
        self.selectionDate = kwargs.pop("date", datetime.date.today())

        super(SelectionDate, self).__init__(**kwargs)
        self.bind(on_dismiss=self.on_dismiss)
        
        self.selectionMois = self.selectionDate.month
        self.selectionAnnee = self.selectionDate.year
    
        self.listeJours = [ 'Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim' ]
        self.listeMois = [ 'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre' ]
        
        self.box_base = BoxLayout(orientation="vertical", padding=10)
        
        # Affichage des commandes de navigation
        box_navigation = BoxLayout(orientation="horizontal", size_hint=(1, None), height=40)
        
        b = Button(text="<", size_hint=(0.2, 1))
        box_navigation.add_widget(b) 
        b.bind(on_release=self.on_bouton_navigation)
        
        self.ctrl_titre = Label(text="", size_hint=(1, 1), markup=True, font_size=22, color=get_color_from_hex("30a3cc"))
        box_navigation.add_widget(self.ctrl_titre)         

        b = Button(text=">", size_hint=(0.2, 1))
        box_navigation.add_widget(b) 
        b.bind(on_release=self.on_bouton_navigation)
        
        self.box_base.add_widget(box_navigation) 
        
        # Affichage des jours        
        self.box_grille = GridLayout(cols=7)  
        self.RemplissageJours()
        self.box_base.add_widget(self.box_grille) 
        
        self.add_widget(self.box_base) 

    def RemplissageJours(self):
        calendrier = calendar.monthcalendar(self.selectionAnnee, self.selectionMois)
        
        for d in self.listeJours :
            b = Label(text=d, markup=True)
            self.box_grille.add_widget(b)
         
        for wk in range(len(calendrier)):
            for d in range(0,7):    
                dateOfWeek = calendrier[wk][d]
                if not dateOfWeek == 0:
                    date = datetime.date(self.selectionAnnee, self.selectionMois, dateOfWeek)
                    b = Button(text=str(dateOfWeek))
                    if date == self.selectionDate :
                        b.background_color = get_color_from_hex("30a3cc")
                        b.background_normal = ""
                    if date == datetime.date.today() :
                        b.color = (1, 0, 0, 1)
                    b.bind(on_release = self.on_release)
                else:
                    b = Label(text='')
                self.box_grille.add_widget(b)   
        
        # Mise à jour du titre
        self.ctrl_titre.text = "[b]" + self.listeMois[self.selectionMois-1] + " " + str(self.selectionAnnee) + "[/b]"
    
    def on_bouton_navigation(self, args):
        if args.text == "<" : navigation = -1
        if args.text == ">" : navigation = +1
        self.selectionMois += navigation
        if self.selectionMois > 12 :
            self.selectionAnnee += 1
            self.selectionMois = 1
        if self.selectionMois == 0 :
            self.selectionMois = 12
            self.selectionAnnee -= 1
        
        self.box_grille.clear_widgets()
        self.RemplissageJours() 
        
    def on_release(self, event):
        date = datetime.date(self.selectionAnnee, self.selectionMois, int(event.text))
        if self.callback != None :
            self.callback(date)
        self.dismiss() 

    def on_dismiss(self, *arg):
        pass
        
        
        
class MyApp(App):
    def build(self):
        b = Button(on_press=self.show_popup, text="Afficher Popup")
        return b

    def show_popup(self, b):
        popup = SelectionDate(title="Sélectionnez une date", callback=self.test, size_hint=(0.8, 0.8))
        popup.open()    
        return popup
        
    def test(self, date=None):
        print("date choisie :", date)
        
if __name__ == '__main__':
    MyApp().run()