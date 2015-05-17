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
from kivy.logger import Logger
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty, NumericProperty, ObjectProperty, DictProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout 
from kivy.uix.gridlayout import GridLayout 
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.rst import RstDocument
from kivy.uix.button import Button
from kivy.graphics import Rectangle, Color
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

import UTILS_Images
import GestionDB


Builder.load_string("""
<MyLabel>:
    valign: 'top'
    text_size: self.size
    canvas.before:
        Color:
            rgb: 0.80, 0.1, 1
        Rectangle:
            size: self.size
            pos: self.pos
""")

class MyLabel(Label):
    def __init__(self, *args, **kwargs):
        super(MyLabel, self).__init__(*args, **kwargs)		

        
class MultiLineLabel(Label):
    def __init__(self, **kwargs):
        super(MultiLineLabel, self).__init__( **kwargs)
        self.markup = True
        self.valign = "middle"
        self.text_size = self.size
        self.bind(size= self.on_size)
        self.bind(text= self.on_text_changed)
        self.size_hint_y = None # Not needed here
        self.bind(pos=self.on_size)
        
        with self.canvas.before:
            Color(0.170, 0.170, 0.170, 1) 
            self.rect = Rectangle(size=self.size, pos=self.pos)

    def on_size(self, widget, size):
        self.text_size = size[0], None
        self.texture_update()
        if self.size_hint_y == None and self.size_hint_x != None:
            self.height = max(self.texture_size[1], self.line_height)
        elif self.size_hint_x == None and self.size_hint_y != None:
            self.width  = self.texture_size[0]
        self.rect.pos = self.pos
        self.rect.size = self.size

    def on_text_changed(self, widget, text):
        self.on_size(self, self.size)

        

class FicheIndividu(Screen):
    dictIndividu = DictProperty()
    def __init__(self, *args, **kwargs):
        super(Screen, self).__init__(*args, **kwargs)	
        self.Importation()
        self.build_layout()
    
    def MAJ(self):
        pass
        
    def Importation(self):
        # Importation des informations
        DB = GestionDB.DB()
        req = """SELECT IDinfo, IDindividu, champ, valeur 
        FROM informations 
        WHERE IDindividu=%d;""" % self.dictIndividu["IDindividu"]
        DB.ExecuterReq(req)
        listeInformations = DB.ResultatReq()
        DB.Close() 
        self.dictInfosIndividu = {}
        for IDinfo, IDindividu, champ, valeur in listeInformations :
            self.dictInfosIndividu[champ] = valeur

    def build_layout(self):
        box_base = BoxLayout(orientation="vertical", padding=0)
        
        ctrl_box_haut = BoxLayout(orientation="horizontal", padding=10, size_hint_y=None)
        
        # Nom de l'individu
        ctrl_label = Label(text="[color=000000][size=28][b]%s[/b][/size][/color]" % self.dictIndividu["nomComplet"], markup=True, size_hint_y=None)
        ctrl_box_haut.add_widget(ctrl_label)
        
		# Photo
        photo = self.dictIndividu["photo"]
        if photo == None :
            if self.dictIndividu["IDcivilite"] == 1 : photo = UTILS_Images.GetTextureFromFichier("images/homme.png")
            if self.dictIndividu["IDcivilite"] in (2, 3) : photo = UTILS_Images.GetTextureFromFichier("images/femme.png")
            if self.dictIndividu["IDcivilite"] == 4 : photo = UTILS_Images.GetTextureFromFichier("images/garcon.png")
            if self.dictIndividu["IDcivilite"] == 5 : photo = UTILS_Images.GetTextureFromFichier("images/fille.png")
            
        if photo != None :
            ctrl_image = Image(texture=photo, size_hint_x=None)
            ctrl_box_haut.add_widget(ctrl_image)
		
        box_base.add_widget(ctrl_box_haut)
        
        # Onglets
        ctrl_onglets = TabbedPanel(do_default_tab=False, padding=10, tab_pos='top_left') # Vertical=left_bottom
        box_base.add_widget(ctrl_onglets)
		
        liste_onglets = [
            {"code":"messages", "titre":u"Messages"},
            {"code":"identite", "titre":u"Identité"},
            {"code":"liens", "titre":u"Liens"},
            {"code":"coordonnees", "titre":u"Coordonnées"},
            {"code":"scolarite", "titre":u"Scolarité"},
            {"code":"activites", "titre":u"Activités"},
            {"code":"medical", "titre":u"Médical"},
            ]

        for dictOnglet in liste_onglets :
            onglet = TabbedPanelItem(id=dictOnglet["code"], text=dictOnglet["titre"])
            doc = RstDocument(text=self.GetTexteOnglet(dictOnglet["code"]))
            onglet.add_widget(doc)
            ctrl_onglets.add_widget(onglet)

        # Barre d'état
        grid = GridLayout(cols=3, row=1, row_force_default=True, row_default_height=30, spacing=(5, 5), padding=10, size_hint=(1, None), height=50)
        grid.canvas.before.add(Color(0.128, 0.128, 0.128))

        def redraw(self, args):
            grid.bg_rect.size = self.size
            grid.bg_rect.pos = self.pos
        with grid.canvas.before:
            grid.bg_rect = Rectangle(pos=grid.pos, size=grid.size)
        grid.bind(pos=redraw, size=redraw)
        
        #ctrl_bouton = Button(id="consommations", text="Consommations", width=200, size_hint=(None, None))
        #grid.add_widget(ctrl_bouton)

        box_base.add_widget(grid)
        
        # Finalisation du layout
        self.add_widget(box_base)


    def GetInfo(self, champ=""):
        if self.dictInfosIndividu.has_key(champ) :
            return self.dictInfosIndividu[champ]
        return ""

    def GetTexteOnglet(self, codeOnglet=""):
        texteInfos = ""
        
        # Messages
        if codeOnglet == "messages" :
            nbre = 0
            
            # Messages
            for x in range(0, 10) :
                texte = self.GetInfo("MESSAGE_%d_TEXTE" % x)
                if texte != "" :
                    texteInfos += u"%s [%s] : %s\n\n" % (self.GetInfo("MESSAGE_%d_DATE_PARUTION" % x), self.GetInfo("MESSAGE_%d_CATEGORIE") % x, texte)
                    nbre += 1
                    
            # Pièces et cotisations
            if self.GetInfo("PIECES_MANQUANTES") != "" :
                texteInfos += u"%s\n\n" % self.GetInfo("PIECES_MANQUANTES")
                nbre += 1
                
            if self.GetInfo("COTISATIONS_MANQUANTES") != "" :
                texteInfos += u"%s\n\n" % self.GetInfo("COTISATIONS_MANQUANTES")
                nbre += 1
            
            # Mémo de l'individu
            if self.GetInfo("INDIVIDU_MEMO") != "" :
                texteInfos += u"Mémo : %s\n\n" % self.GetInfo("INDIVIDU_MEMO")
                nbre += 1
                
            if nbre == 0 :
                texteInfos += u"Aucun message"


        # Identité
        if codeOnglet == "identite" :
            if self.GetInfo("INDIVIDU_DATE_NAISS") != "" :
                texteInfos += u"Date de naissance : %s (%s)\n\n" % (self.GetInfo("INDIVIDU_DATE_NAISS"), self.GetInfo("INDIVIDU_AGE"))
            else :
                texteInfos += u"Date de naissance inconnue\n\n"
            if self.GetInfo("INDIVIDU_VILLE_NAISS") != "" :
                texteInfos += u"Ville de naissance : %s \n\n" % self.GetInfo("INDIVIDU_VILLE_NAISS")
            texteInfos += u"------------\n\n"
            
            nbre = 0
            if self.GetInfo("INDIVIDU_CATEGORIE_TRAVAIL") != "" :
                texteInfos += u"Catégorie socio-professionnelle : %s \n\n" % self.GetInfo("INDIVIDU_CATEGORIE_TRAVAIL")
                nbre += 1
            if self.GetInfo("INDIVIDU_PROFESSION") != "" :
                texteInfos += u"Profession : %s \n\n" % self.GetInfo("INDIVIDU_PROFESSION")
                nbre += 1
            if self.GetInfo("INDIVIDU_EMPLOYEUR") != "" :
                texteInfos += u"Employeur : %s \n\n" % self.GetInfo("INDIVIDU_EMPLOYEUR")
                nbre += 1
            if nbre == 0 :
                texteInfos += u"Aucune information sur l'activité professionnelle\n\n"

        
        # Liens
        if codeOnglet == "liens" :
            nbre = 0
            listeTemp = [(u"Père", "PERE"), (u"Mère", "MERE"), (u"Conjoint", "CONJOINT")]
            listeTemp.extend([("Enfant", "ENFANT_%d" % x) for x in range(0, 10)])
            listeTemp.extend([("Autre lien", "AUTRE_LIEN_%d" % x) for x in range(0, 10)])
            for titre, x in listeTemp :
                if self.GetInfo("%s_NOM_COMPLET" % x) != "" :
                    titre = self.GetInfo("%s_NOM_LIEN" % x)
                    if self.GetInfo("%s_AUTORISATION" % x) != "" :
                        autorisation = u" (Niveau d'autorisation : %s)" % self.GetInfo("%s_AUTORISATION" % x)
                    else :
                        autorisation = ""
                    texteInfos += u"- **%s** : %s %s\n\n" % (self.GetInfo("%s_NOM_COMPLET" % x), titre, autorisation)
                    nbre += 1
            if nbre == 0 :
                texteInfos += u"Aucun lien"
        
        
        # Coordonnées
        if codeOnglet == "coordonnees" :
        
            # Coordonnées de l'individu
            if self.GetInfo("INDIVIDU_RUE") != "" or self.GetInfo("INDIVIDU_CP") != "" :
                texteInfos += u"Adresse : %s %s %s\n\n" % (self.GetInfo("INDIVIDU_RUE"), self.GetInfo("INDIVIDU_CP"), self.GetInfo("INDIVIDU_VILLE"))
                if self.GetInfo("INDIVIDU_SECTEUR") != "" :
                    texteInfos += u"Secteur : %s\n\n" % self.GetInfo("INDIVIDU_SECTEUR")
            else :
                texteInfos += u"Aucune adresse\n\n"
            
            if self.GetInfo("INDIVIDU_TEL_DOMICILE") != "" :
                texteInfos += u"Tél. Domicile : %s\n\n" % self.GetInfo("INDIVIDU_TEL_DOMICILE")
            if self.GetInfo("INDIVIDU_TEL_PORTABLE") != "" :
                texteInfos += u"Tél. Portable : %s\n\n" % self.GetInfo("INDIVIDU_TEL_PORTABLE")
            if self.GetInfo("INDIVIDU_TEL_PRO") != "" :
                texteInfos += u"Tél. Pro : %s\n\n" % self.GetInfo("INDIVIDU_TEL_PRO")
            if self.GetInfo("INDIVIDU_MAIL") != "" :
                texteInfos += u"Email : %s\n\n" % self.GetInfo("INDIVIDU_MAIL")
            texteInfos += u"------------\n\n"

            # Autres coordonnées
            listeTemp = [(u"Père", "PERE"), (u"Mère", "MERE"), (u"Conjoint", "CONJOINT")]
            listeTemp.extend([("Enfant", "ENFANT_%d" % x) for x in range(0, 10)])
            listeTemp.extend([("Autre lien", "AUTRE_LIEN_%d" % x) for x in range(0, 10)])
            nbre = 0
            for titre, x in listeTemp :
                if self.GetInfo("%s_NOM_COMPLET" % x) != "" :
                    titre = self.GetInfo("%s_NOM_LIEN" % x)
                    texteInfos += u"**%s** (%s) :\n\n" % (self.GetInfo("%s_NOM_COMPLET" % x), titre)
                    if self.GetInfo("%s_TEL_DOMICILE" % x) != "" :
                        texteInfos += u"  - Tél. Domicile : %s\n\n" % self.GetInfo("%s_TEL_DOMICILE" % x)
                    if self.GetInfo("%s_TEL_PORTABLE" % x) != "" :
                        texteInfos += u"  - Tél. Portable : %s\n\n" % self.GetInfo("%s_TEL_PORTABLE" % x)
                    if self.GetInfo("%s_TEL_PRO" % x) != "" :
                        texteInfos += u"  - Tél. Pro : %s\n\n" % self.GetInfo("%s_TEL_PRO" % x)
                    if self.GetInfo("%s_MAIL" % x) != "" :
                        texteInfos += u"  - Email : %s\n\n" % self.GetInfo("%s_MAIL" % x)
                    if self.GetInfo("INDIVIDU_RUE") != "" or self.GetInfo("INDIVIDU_CP") != "" :
                        texteInfos += u"  - Adresse : %s %s %s\n\n" % (self.GetInfo("%s_RUE" % x), self.GetInfo("%s_CP" % x), self.GetInfo("%s_VILLE" % x))

                    texteInfos += u"------------\n\n"
                    nbre += 1
                    
            if nbre == 0 :
                texteInfos += u"Aucune autre coordonnée"
		
        # Scolarité
        if codeOnglet == "scolarite" :
            if self.GetInfo("SCOLARITE_NOM_ECOLE") != "" :
                texteInfos += u"Ecole : %s\n\n" % self.GetInfo("SCOLARITE_NOM_ECOLE")
                texteInfos += u"Classe : %s\n\n" % self.GetInfo("SCOLARITE_NOM_CLASSE")
                texteInfos += u"Niveau : %s\n\n" % self.GetInfo("SCOLARITE_NOM_NIVEAU")
            else :
                texteInfos += u"Aucune étape de scolarité"
                
            
        # Activités
        if codeOnglet == "activites" :
            nbre = 0
            for x in range(0, 20) :
                if self.GetInfo("INSCRIPTION_%d_ACTIVITE" % x) != "" :
                    texteInfos += u"Date d'inscription : %s\n\n" % self.GetInfo("INSCRIPTION_%d_DATE_INSCRIPTION" % x)
                    texteInfos += u"Activité : **%s**\n\n" % self.GetInfo("INSCRIPTION_%d_ACTIVITE" % x)
                    texteInfos += u"Groupe : **%s**\n\n" % self.GetInfo("INSCRIPTION_%d_GROUPE" % x)
                    texteInfos += u"Catégorie de tarif : %s\n\n" % self.GetInfo("INSCRIPTION_%d_CATEGORIE_TARIF" % x)
                    if self.GetInfo("INSCRIPTION_%d_PARTI" % x) == "Oui" :
                        texteInfos += u"## Parti de l'activité ##\n\n"
                    texteInfos += u"------------\n\n"
                    nbre += 1
            if nbre == 0 :
                texteInfos += u"Aucune inscription"

                
        # Médical
        if codeOnglet == "medical" :
        
            # Médecin traitant
            if self.GetInfo("MEDECIN_NOM") != "" :
                texteInfos += u"Médecin traitant :\n\n"
                texteInfos += u"  - Nom : **%s %s**\n" % (self.GetInfo("MEDECIN_NOM"), self.GetInfo("MEDECIN_PRENOM"))
                texteInfos += u"  - Adresse : %s %s %s\n" % (self.GetInfo("MEDECIN_RUE"), self.GetInfo("MEDECIN_CP"), self.GetInfo("MEDECIN_VILLE"))
                texteInfos += u"  - Téléphone : %s %s\n" % (self.GetInfo("MEDECIN_TEL_CABINET"), self.GetInfo("MEDECIN_TEL_MOBILE"))
            else :
                texteInfos += u"Pas de médecin traitant\n\n"
            texteInfos += u"------------\n\n"
            
            # Problèmes médicaux
            nbre = 0
            for x in range(0, 10) :
                if self.GetInfo("MEDICAL_%d_INTITULE" % x) != "" :
                    texteInfos += u"Difficulté de santé :\n\n"
                    texteInfos += u"  - Intitulé : **%s**\n\n" % self.GetInfo("MEDICAL_%d_INTITULE" % x)
                    if self.GetInfo("MEDICAL_%d_DESCRIPTION" % x) != "" :
                        texteInfos += u"  - Description : %s\n\n" % self.GetInfo("MEDICAL_%d_DESCRIPTION" % x)
                    if self.GetInfo("MEDICAL_%d_TRAITEMENT_MEDICAL}" % x) != "" :
                        texteInfos += u"  - Traitement : %s\n\n" % self.GetInfo("MEDICAL_%d_TRAITEMENT_MEDICAL}" % x)
                        texteInfos += u"  - Description du traitement : %s\n\n" % self.GetInfo("MEDICAL_%d_DESCRIPTION_TRAITEMENT" % x)
                        texteInfos += u"  - Date de début du traitement : %s\n\n" % self.GetInfo("MEDICAL_%d_DATE_DEBUT_TRAITEMENT" % x)
                        texteInfos += u"  - Date de fin du traitement : %s\n\n" % self.GetInfo("MEDICAL_%d_DATE_FIN_TRAITEMENT" % x)
                    texteInfos += u"------------\n\n"
                    nbre += 1
            if nbre == 0 :
                texteInfos += u"Aucun problème de santé"

                    
        return texteInfos
		

		
class MyApp(App):
    def build(self):
        dictIndividu = {
            "nomComplet" : "Kévin DUPOND",
            "IDcivilite": 1,
            "photo" : None,
            "IDindividu" : 45,
            }
        mainView = FicheIndividu(dictIndividu=dictIndividu)
        return mainView

if __name__ == '__main__':
    MyApp().run()