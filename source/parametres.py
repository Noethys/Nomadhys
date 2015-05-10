# -*- coding: utf-8 -*-
#!/usr/bin/env python

##############################################################
# Application :    Nomadhys, application nomade pour Noethys #
# Site internet :  www.noethys.com                           #
# Auteur:          Ivan LUCAS                                #
# Copyright:       (c) 2010-15 Ivan LUCAS                    #
# Licence:         Licence GNU GPL                           #
##############################################################


from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import StringProperty, ListProperty, NumericProperty, ObjectProperty, DictProperty, BooleanProperty
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.button import Button

from kivy.config import ConfigParser
from kivy.uix.settings import Settings, SettingItem, SettingSpacer

import os
import sys
import json
import UTILS_Divers

#runpath = os.path.dirname(os.path.realpath(sys.argv[0]))
#os.chdir(runpath)


JSON_GENERAL = [
	{
		"type": "title",
		"title": "Fichier"
    },
	{
		"type": "string",
		"title": "ID du fichier",
		"desc": "Reportez ici l'ID du fichier de données que vous trouverez dans Noethys (Menu Fichier > Informations > IDfichier). Attention, n'oubliez pas les 3 dernières lettres en majuscules.",
		"section": "fichier",
		"key": "ID",
	},
	{
		"type": "title",
		"title": "Appareil"
    },
	{
		"type": "string",
		"title": "Nom de l'appareil",
		"desc": "Exemple : 'Ma tablette 1'",
		"section": "general",
		"key": "nom_appareil",
	},
	{
		"type": "string",
		"title": "ID de l'appareil",
		"desc": "Exemple : 'ABC123'. Il est déconseillé de modifier ce paramètre généré automatiquement.",
		"section": "general",
		"key": "ID_appareil",
	},
	{
		"type": "title",
		"title": "Utilisateur"
    },
	{
		"type": "bool",
		"title": "Mémoriser l'utilisateur",
		"desc": "Permet à l'utilisateur d'éviter de saisir son code personnel à chaque ouverture.",
		"section": "utilisateur",
		"key": "memoriser_code",
	},

    ]

    
JSON_SYNCHRONISATION = [
	{
		"type": "title",
		"title": "Serveur Internet/WIFI"
	},
	{
		"type": "string",
		"title": "Adresse",
		"desc": "Adresse du serveur",
		"section": "synchronisation",
		"key": "serveur_adresse",
	},
	{
		"type": "string",
		"title": "Port",
		"desc": "Port de communication avec le serveur",
		"section": "synchronisation",
		"key": "serveur_port",
	},
	{
		"type": "title",
		"title": "FTP"
	},
	{
		"type": "string",
		"title": "Adresse",
		"desc": "Exemple : 'ftp.monadresse.com'",
		"section": "synchronisation",
		"key": "ftp_hote",
	},
	{
		"type": "string",
		"title": "Identifiant",
		"desc": "Exemple : 'monidentifiant'",
		"section": "synchronisation",
		"key": "ftp_identifiant",
	},
	{
		"type": "password",
		"title": "Mot de passe",
		"desc": "Exemple : 'monmotdepasse'",
		"section": "synchronisation",
		"key": "ftp_mdp",
	},
	{
		"type": "string",
		"title": "Repertoire",
		"desc": "Exemple : 'www/mesfichiers'",
		"section": "synchronisation",
		"key": "ftp_repertoire",
	},
	{
		"type": "title",
		"title": "Cryptage"
	},
	{
		"type": "bool",
		"title": "Activer",
		"desc": "Activer le cryptage lors de l'envoi",
		"section": "synchronisation",
		"key": "cryptage_activer",
	},
	{
		"type": "password",
		"title": "Mot de passe",
		"desc": "Mot de passe pour crypter ou décrypter les donnees",
		"section": "synchronisation",
		"key": "cryptage_mdp",
	},
    
    ]


        
        
Builder.load_string(
'''
<SettingPassword>:
    Label:
        text: '' if root.value == '' else '********'
''')
         
class SettingPassword(SettingItem):
    popup = ObjectProperty(None, allownone=True)
    textinput = ObjectProperty(None)

    def on_panel(self, instance, value):
        if value is None:
            return
        self.bind(on_release=self._create_popup)

    def _dismiss(self, *largs):
        if self.textinput:
            self.textinput.focus = False
        if self.popup:
            self.popup.dismiss()
        self.popup = None

    def _validate(self, instance):
        self._dismiss()
        value = self.textinput.text.strip()
        self.value = value

    def _create_popup(self, instance):
        # create popup layout
        content = BoxLayout(orientation='vertical', spacing='5dp')
        popup_width = min(0.95 * Window.width, dp(500))
        self.popup = popup = Popup(
            title=self.title, content=content, size_hint=(None, None),
            size=(popup_width, '250dp'))

        # create the textinput used for numeric input
        self.textinput = textinput = TextInput(
            text=self.value, font_size='24sp', multiline=False,
            size_hint_y=None, height='42sp', password=True)
        textinput.bind(on_text_validate=self._validate)
        self.textinput = textinput

        # construct the content, widget are used as a spacer
        content.add_widget(Widget())
        content.add_widget(textinput)
        content.add_widget(Widget())
        content.add_widget(SettingSpacer())

        # 2 buttons are created for accept or cancel the current value
        btnlayout = BoxLayout(size_hint_y=None, height='50dp', spacing='5dp')
        btn = Button(text='Ok')
        btn.bind(on_release=self._validate)
        btnlayout.add_widget(btn)
        btn = Button(text='Cancel')
        btn.bind(on_release=self._dismiss)
        btnlayout.add_widget(btn)
        content.add_widget(btnlayout)

        # all done, open the popup !
        popup.open()

        
        
        
class Popup_parametres(Popup):
    def __init__(self, *args, **kwargs):
        self.callback = kwargs.pop("callback", None)
        self.pages = kwargs.pop("pages", ["general", "synchronisation", "kivy"])
        self.title = "Paramètres"
        self.size_hint = (0.9, 0.9)
        
        config = ConfigParser()
        config.read(UTILS_Divers.GetRepData() + "config.cfg")

        self.settings = Settings()
        self.settings.register_type('password', SettingPassword)
        
        if "general" in self.pages : self.settings.add_json_panel("Généralités", config, data=json.dumps(JSON_GENERAL, encoding="utf-8"))
        if "synchronisation" in self.pages : self.settings.add_json_panel("Synchronisation", config, data=json.dumps(JSON_SYNCHRONISATION, encoding="utf-8"))
        if "kivy" in self.pages : self.settings.add_kivy_panel()
        
        self.settings.interface.menu.close_button.text = "Fermer"
        
        self.content = self.settings
        self.settings.bind(on_close=self.OnBoutonFermer)
        self.bind(on_dismiss=self.on_dismiss)
        super(Popup, self).__init__(*args, **kwargs)		

    def AfficherPage(self, nom="Synchronisation"):
        for button in self.settings.interface.menu.buttons_layout.children:
            if button.text == nom :
                button.selected = True
                self.settings.interface.menu.selected_uid = button.uid
                #settings.interface.menu.on_selected_uid() 

    def OnBoutonFermer(self, *args):
        self.dismiss()
        
    def on_dismiss(self, *arg):
        if self.callback != None :
            self.callback()

                
class MyApp(App):
    def build(self):
        a = App()
        print ">>>>>>>>>>>>>>>>>", a.user_data_dir
    
        popup = Popup_parametres(callback=self.Test)
        popup.open()  

        popup.AfficherPage("Kivy")
        
        return popup
    
    def Test(self):
        print "callback ici"
    
        


if __name__ == '__main__':
    MyApp().run()
    