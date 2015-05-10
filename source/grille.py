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
from kivy.properties import StringProperty, ListProperty, NumericProperty, ObjectProperty, DictProperty, BooleanProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout 
from kivy.uix.gridlayout import GridLayout 
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.graphics import Rectangle, Color
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.dropdown import DropDown
from kivy.uix.spinner import Spinner
from kivy.animation import Animation
from kivy.uix.slider import Slider
from kivy.clock import Clock

from selection_etat import GetLabelEtat
from widgets import BoutonTransparent, BoutonAvecImageEtroit, BoutonAvecImageLarge

from msgbox import MsgBox
import UTILS_Images
import UTILS_Dates
import UTILS_Sync
import GestionDB
import datetime
import time
import random
import math
import copy

COULEUR_RESERVATION = (1, 0.73, 0, 1)
COULEUR_ATTENTE = (1, 1, 0, 1)
COULEUR_REFUS = (1, 0, 0, 1)



Builder.load_string("""
#: import Animation kivy.animation.Animation

<BitmapButton>:
    halign: 'left'
    valign: 'middle'
    text_size: self.size
    padding_x: -45
    Image:
        source: "images/personnes.png"
        center_y: root.center_y
        center_x: root.x + 25
        #x: root.x

    
  
                        
                        
                        
<BoutonMemo>:
    text_size: self.width-15, self.height-2
    markup: True
    halign: 'left'
    valign: 'top'
    disabled: not self.opacity
    
    
<BoutonCase>:
    label_groupe: label_groupe
    image_etat: image_etat
    
    id: bouton_case
    markup: True
    taille_police: 12
    color: (0, 0, 0, 1)
    size_hint: 0.3, None
    height: 50
    halign: 'left'
    valign: 'top'
    font_size: self.taille_police
    text_size: self.width-6, self.height-2
    on_release: self.on_release
    on_press: self.on_press
    disabled: not self.opacity

    Label:
        id: label_groupe
        text: ''
        markup: True
        color: (1, 1, 1, 1)
        font_size: 11
        size_hint: None, None
        halign: 'center'
        valign: 'top'
        text_size: bouton_case.width, self.font_size
        pos: bouton_case.center_x - self.width/2.0, bouton_case.y - bouton_case.height + self.font_size
    
    Image:
        id: image_etat
        source: ''
        opacity: 0
        size: 16, 16
        pos: bouton_case.x + bouton_case.width - 20, bouton_case.y + bouton_case.height - 20
        





        
<Grille>:
    box_base: box_base
    slider_pages: slider_pages
    ctrl_date: ctrl_date
    ctrl_activite: ctrl_activite
    ctrl_etat: ctrl_etat
    box_grille: box_grille
	
    BoxLayout:
        id: box_base
        orientation: 'vertical'
        padding: 0
        size_hint: (1, 1)  
        
        BoxLayout:
            id: box_haut
            orientation: 'horizontal'
            padding: 0
            size_hint: (1, None)
            height: 50
            
            Button:
                id: ctrl_date
                text: 'Date'
                markup: True
                size_hint: (0.2, None)
                height: 50
                on_release: root.on_bouton_selection_date()

            Button:
                id: ctrl_activite
                text: 'Activite'
                markup: True
                size_hint: (0.5, None)
                height: 50
                on_release: root.on_bouton_selection_activite()

            Button:
                id: ctrl_etat
                text: 'Mode de saisie'
                markup: True
                size_hint: (0.3, None)
                height: 50
                on_release: root.on_bouton_selection_etat()
                
        BoxLayout:
            id: box_conteneur
            orientation: 'horizontal'
            padding: 0
            size_hint: (1, 1)
                
            BoxLayout:  
                id: box_slider
                orientation: 'vertical'        
                size_hint: (None, 1)
                width: '40sp'
                
                #canvas.before:
                    #Color:
                    #    rgba: 1, 0.5, 0, 1
                    #Rectangle:
                    #    pos: self.pos
                    #    size: self.size  
                
                Label: 
                    text: str(int(slider_pages.value)+1)
                    size: box_slider.width, '50sp'
                    size_hint: None, None
                    opacity: 0.3 if slider_pages.max > 1 else 0
                
                Scatter:
                    id: scatter_slider
                    rotation: 180
                    auto_bring_to_front: False
                    
                    Slider:
                        id: slider_pages
                        orientation: 'vertical'
                        opacity: 1 if slider_pages.max > 1 else 0
                        min: 0
                        max: 0
                        value: 0
                        step: 1
                        width: box_slider.width
                        size_hint: 1, 1
                        height: scatter_slider.height
                        on_value: root.on_slider_pages(self)
                        
                        #canvas.before:
                        #    Color:
                        #        rgba: 0, 1, 0, 1
                        #    Rectangle:
                        #        pos: self.pos
                        #        size: self.size   
                            
                Label: 
                    text: str(int(slider_pages.max)+1)
                    size: box_slider.width, '50sp'
                    size_hint: None, None
                    opacity: 0.3 if slider_pages.max > 1 else 0
                    
            BoxLayout:
                id: box_grille
                orientation: 'vertical'
                padding: (10, 10, 30, 20)
                size_hint: (1, 1)
									
				#canvas.before:
				#	Color:
				#		rgba: 0, 1, 1, 1
				#	Rectangle:
				#		pos: self.pos
				#		size: self.size   

					
            BoxLayout:
                id: box_navigation
                orientation: 'vertical'
                padding: 0
                size_hint: None, 1
                width: 60
                opacity: 1 if slider_pages.max > 1 else 0
                disabled: self.opacity != 1
                
                BoutonTransparent:
                    id: bouton_navigation_nom
                    on_release: root.on_bouton_navigation_nom()
                    chemin_image: 'images/recherche_individu.png'
                    
                BoutonTransparent:
                    id: bouton_navigation_lettre
                    on_release: root.on_bouton_navigation_lettre()
                    chemin_image: 'images/recherche_lettre.png'
                
                BoutonTransparent:
                    id: bouton_navigation_premier
                    on_release: root.on_bouton_navigation_premier()
                    opacity: 0.4 if slider_pages.value == 0 or slider_pages.max == 0 else 1
                    disabled: self.opacity != 1
                    chemin_image: 'images/premier_vertical.png'
                
                BoutonTransparent:
                    id: bouton_navigation_precedent
                    on_release: root.on_bouton_navigation_precedent()
                    opacity: 0.4 if slider_pages.value == 0 or slider_pages.max == 0 else 1
                    disabled: self.opacity != 1
                    chemin_image: 'images/precedent_vertical.png'

                BoutonTransparent:
                    id: bouton_navigation_suivant
                    on_release: root.on_bouton_navigation_suivant()
                    opacity: 0.4 if slider_pages.value == slider_pages.max or slider_pages.max == 0 else 1
                    disabled: self.opacity != 1
                    chemin_image: 'images/suivant_vertical.png'

                BoutonTransparent:
                    id: bouton_navigation_dernier
                    on_release: root.on_bouton_navigation_dernier()
                    opacity: 0.4 if slider_pages.value == slider_pages.max or slider_pages.max == 0 else 1
                    disabled: self.opacity != 1
                    chemin_image: 'images/dernier_vertical.png'


					
        GridLayout:
			id: box_commandes
		    cols: 6
			rows: 1
			row_force_default: True
			row_default_height: 50 # 30 pour avoir un bouton réduit
			spacing: 0, 0
			padding: 0
			size_hint: 1, None
			height: 50

			canvas.before:
				Color:
					rgb: 0.128, 0.128, 0.128, 1
				Rectangle:
					pos: self.pos
					size: self.size

            BoutonAvecImageLarge:
                id: bouton_enregistrer
                texte: 'Enregistrer'
                chemin_image: 'images/enregistrer.png'
                disabled: len(root.listeModifications) == 0
                on_release: root.on_bouton_enregistrer()

            BoutonAvecImageLarge:
                id: bouton_annuler
                texte: 'Annuler'
                chemin_image: 'images/annuler.png'
                disabled: len(root.listeModifications) == 0
                on_release: root.on_bouton_annuler()
                                    
            BoutonAvecImageLarge:
                id: bouton_afficher_inscrits
                texte: 'Inscrits'
                chemin_image: 'images/filtre.png'
                disabled: root.IDactivite == None
                on_release: root.on_bouton_afficher_inscrits()
                
            BoutonAvecImageLarge:
                id: bouton_afficher_presents
                texte: 'Présents'
                chemin_image: 'images/filtre.png'
                disabled: root.IDactivite == None
                on_release: root.on_bouton_afficher_presents()
            
            BoutonAvecImageLarge:
                id: bouton_afficher_totaux
                texte: 'Totaux'
                chemin_image: 'images/total.png'
                disabled: root.IDactivite == None
                on_release: root.on_bouton_afficher_totaux()

            BoutonAvecImageLarge:
                id: bouton_ajouter_individu
                texte: 'Ajouter'
                chemin_image: 'images/ajouter_individu.png'
                disabled: root.IDactivite == None
                on_release: root.on_bouton_ajouter_inscription()
        

""")

           
class LabelEnteteLigne(Label):
    def __init__(self, *args, **kwargs):
        super(LabelEnteteLigne, self).__init__(*args, **kwargs)		        
        
        
class BitmapButton(Button):
    def __init__(self, *args, **kwargs):
        super(BitmapButton, self).__init__(*args, **kwargs)		


class BoutonMemo(Button):
    dictInscription = DictProperty()
    date = ObjectProperty()
    grille = ObjectProperty()
    def __init__(self, *args, **kwargs):
        super(BoutonMemo, self).__init__(*args, **kwargs)	
        
    def on_release(self, *args):
        from saisie_memo_journalier import SaisieMemoJournalier
        popup = SaisieMemoJournalier(title="Saisissez le texte du memo journalier", texte=self.text, callback=self.Valider)
        popup.open()  
    
    def Valider(self, texte=""):
        texte = texte.decode('utf-8')
        if self.text == texte :
            return
            
        # Actualisation de l'affichage de la case
        self.text = texte
        # Envoi de la donnée à la grille
        key = (self.dictInscription["IDindividu"], self.date)
        if self.grille.dictMemos.has_key(key) == False :
            self.grille.dictMemos[key] = {"texte" : "", "IDmemo" : None}
        self.grille.dictMemos[key]["texte"] = texte
        
        if ("memo", key) not in self.grille.listeModifications :
            self.grille.listeModifications.append(("memo", key))

# ---------------------------------------------------------------------------------------------------------------        
        
class BoutonCase(Button):
    ouvert = BooleanProperty()
    dictConso = DictProperty()
    dictInscription = DictProperty()
    grille = ObjectProperty()
    IDunite = NumericProperty()
    numLigne = NumericProperty()
    animationEnCours = BooleanProperty() 
    date = ObjectProperty()
    
    def __init__(self, *args, **kwargs):
        super(BoutonCase, self).__init__(*args, **kwargs)	
        self.animationEnCours = False
        self.long_click = False
        self.MAJ()   
        
    def MAJ(self):
        self.disabled = not self.ouvert
        
        if self.dictConso == {}:
            # Apparence par défaut
            if self.background_normal == "" :
                self.background_color = (1, 1, 1, 1)
                self.background_normal = "atlas://data/images/defaulttheme/button"
            self.image_etat.source = ""
            self.image_etat.opacity = 0
            self.label_groupe.text = ""
            self.text = ""
                
        else :
            etat = self.dictConso["etat"]
            
            # Couleur de fond
            if etat in ("reservation", "present", "absenti", "absentj") : couleur = COULEUR_RESERVATION
            if etat == "attente" : couleur = COULEUR_ATTENTE
            if etat == "refus" : couleur = COULEUR_REFUS
            self.background_color = couleur
            self.background_normal = ""
            
            # Etat
            if etat in ("present", "absenti", "absentj") :
                self.image_etat.source = source="images/%s.png" % etat
                self.image_etat.opacity = 1
            else :
                self.image_etat.source = ""
                self.image_etat.opacity = 0
            
            # Groupe
            IDgroupe = self.dictConso["IDgroupe"]
            nomGroupe = self.grille.dictGroupes[IDgroupe]["nom"]
            self.label_groupe.text = nomGroupe
            
            # Détail
            typeUnite = self.grille.dictUnites[self.IDunite]["type"]
            if typeUnite == "Unitaire" :
                detail = ""
            elif typeUnite == "Horaire" :
                detail = self.dictConso["heure_debut"] + "\n" + self.dictConso["heure_fin"]
            elif typeUnite == "Quantite" :
                detail = str(self.quantite)
            else :
                detail = ""
            self.text = detail #str(self.dictConso["IDconso"])# pour les tests 
            
    def Animer(self):
        """ Animation de la case """
        if self.animationEnCours == False :
            self.animationEnCours = True
            x, y = copy.copy(self.pos)
            largeur, hauteur = copy.copy(self.size)
            anim = Animation(pos=(x, y-5), t='in_out_back', duration=0.2)
            anim += Animation(pos=(x, y), animationEnCours=False, t='in_out_elastic', duration=0)
            anim.start(self)
            
    def on_press(self, *args):
        self.long_click = False
        Clock.schedule_once(self.ChronoClick, 1) # Temps du long click en secondes
    
    def ChronoClick(self, dt):
        self.long_click = True
        
    def on_release(self, *args):
        # Animation du bouton
        self.Animer() 
        
        # Recherche type unité
        typeUnite = self.grille.dictUnites[self.IDunite]["type"]
        
        if self.dictConso == {} :
        
            # Création
            if typeUnite != "Unitaire" or self.long_click == True :
                afficherDetail = True
            else :
                afficherDetail = False
            self.CreerConso(afficherDetail=afficherDetail)
        else :
            
            # Modification de l'état
            if self.long_click == False and self.grille.etat in ("present", "absenti", "absentj") :
                self.ModifierEtat(etat=self.grille.etat)
                return
                
            # Modification
            if typeUnite != "Unitaire" or self.long_click == True :
                self.ModifierConso()
                
            # Suppression
            else :
                # Protection anti-suppression
                if self.dictConso["etat"] in ("present", "absenti", "absentj") and self.grille.etat not in ("present", "absenti", "absentj") :
                    MsgBox.info(text="Vous ne pouvez pas supprimer une consommation pointée !", title="Erreur", size_hint=(0.6, 0.6))
                    return
                self.SupprimerConso()
            
    
    def VerifieCompatibilitesUnites(self):
        """ Vérifie les incompatibilités entre les unités """
        unites_incompatibles = self.grille.dictUnites[self.IDunite]["unites_incompatibles"]
        listeCasesLigne = self.grille.dictCasesParLigne[self.numLigne]["unites"]
        for IDunite, case in listeCasesLigne.iteritems() :
            if case.dictConso != {} and case.dictConso["etat"] in ("reservation", "present") :
                if IDunite in unites_incompatibles :
                    return IDunite
        return None

    def CreerConso(self, afficherDetail=False):
        # Vérifie les incompatibilités entre les unités
        IDuniteIncompatible = self.VerifieCompatibilitesUnites()
        if IDuniteIncompatible != None :
            nomUnite = self.grille.dictUnites[IDuniteIncompatible]["nom"]
            MsgBox.info(text="Incompatible avec la consommation '" + nomUnite + "' existante !", title="Erreur de saisie", size_hint=(0.6, 0.6))
            return

        # Mémorisation du dictConso
        dictConso = {
            "IDconso" : None,
            "IDindividu": self.dictInscription["IDindividu"],
            "IDactivite": self.grille.IDactivite,
            "IDinscription": self.dictInscription["IDinscription"],
            "date": self.date,
            "IDunite" : self.IDunite,
            "IDgroupe" : self.dictInscription["IDgroupe"],
            "heure_debut" : self.grille.dictUnites[self.IDunite]["heure_debut"],
            "heure_fin" : self.grille.dictUnites[self.IDunite]["heure_fin"],
            "etat" : self.grille.etat,
            "date_saisie": datetime.date.today(),
            "IDutilisateur" : self.grille.app.IDutilisateur,
            "IDcategorie_tarif" : self.dictInscription["IDcategorie_tarif"],
            "IDcompte_payeur" : self.dictInscription["IDcompte_payeur"],
            "quantite" : None,
            "IDfamille" : self.dictInscription["IDfamille"],
            }
        
        # Ouverture de la fenêtre de détail ou validation immédiate
        if afficherDetail == True :
            from detail_conso import DetailConso
            popup = DetailConso(callback=self.ValiderConso, dictConso=dictConso, typeAction="ajouter", grille=self.grille)
            popup.open()   
        else :
            self.ValiderConso(typeAction="ajouter", dictConso=dictConso)
            
    def ModifierConso(self):
        from detail_conso import DetailConso
        popup = DetailConso(callback=self.ValiderConso, dictConso=self.dictConso, typeAction="modifier", grille=self.grille)
        popup.open()   
    
    def ModifierEtat(self, etat=None):
        dictConso = copy.copy(self.dictConso)
        dictConso["etat"] = etat
        self.ValiderConso(typeAction="modifier", dictConso=dictConso)
        
    def SupprimerConso(self):
        self.ValiderConso(typeAction="supprimer", dictConso=self.dictConso)
        
    def ValiderConso(self, typeAction="", dictConso=None):
        t1 = time.time()
        
        key = (self.dictInscription["IDinscription"], self.date, self.IDunite)
        
        # Sauvegarde de la conso
        #dictConso = self.SauvegardeConso(typeAction=typeAction, dictConso=dictConso)
        
        # Mémorisation de l'action
        dictAction = copy.copy(dictConso)
        #UTILS_Sync.AjouterAction(nomTable="consommations", typeAction=typeAction, dictAction=dictAction)
        
        if ("consommation", key) not in self.grille.listeModifications :
            self.grille.listeModifications.append(("consommation", key))
        
        # MAJ de la case et de la liste des conso de la grille
        if typeAction == "supprimer" :
            del self.grille.dictConso[key]
            self.dictConso = {}
        else :
            self.grille.dictConso[key] = dictConso
            self.dictConso = dictConso
        self.MAJ() 
                
    def SauvegardeConso______archive(self, typeAction="", dictConso={}):
        # Préparation des données
        listeDonnees = []
        for nomChamp, valeur in dictConso.iteritems() :
            if nomChamp not in ("IDfamille", "type_action", "horodatage_action", "IDutilisateur_action") :
                listeDonnees.append((nomChamp, valeur))
        
        # Sauvegarde de la consommation dans la base
        if False :
            DB = GestionDB.DB()
            if typeAction == "supprimer" :
                if dictConso["IDconso"] != None :
                    DB.ReqDEL("consommations", "IDconso", dictConso["IDconso"])
            if typeAction == "modifier" :
                if dictConso["IDconso"] != None :
                    DB.ReqMAJ("consommations", listeDonnees, "IDconso", dictConso["IDconso"])
            if typeAction == "ajouter" :
                IDconso = DB.ReqInsert("consommations", listeDonnees)
                dictConso["IDconso"] = IDconso
            DB.Close() 
                
        return dictConso
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
# ----------------------------------------------------------------------------------------------------------
     
class Grille(Screen):
    listeModifications = ListProperty()
    IDactivite = ObjectProperty()
    app = ObjectProperty()
    
    def __init__(self, *args, **kwargs):
        self.app = kwargs.get("app", None)
        super(Screen, self).__init__(*args, **kwargs)	
        self.mode = "date"
        
        # Variables
        self.pageActuelle = 0
        self.dateDebut = datetime.date.today()
        self.dateFin = datetime.date.today()
        self.IDactivite = None
        self.etat = "reservation"
        self.dictConso = {}
        
        # Binds
        self.box_grille.bind(height=self.on_change_height)
        
        
    def MAJ(self):
        self.Importations_generales() 
        self.Selection_date(self.dateDebut, refreshGrille=False)
        self.Selection_activite(self.IDactivite, refreshGrille=False)
        self.Selection_etat("reservation")
        self.Draw_grille(importer=True)
        self.AfficherPresents() 
    
    def Importations_generales(self):
        DB = GestionDB.DB()
        
        # Activites
        req = """SELECT IDactivite, nom, date_debut, date_fin
        FROM activites 
        ORDER BY date_fin DESC;"""
        DB.ExecuterReq(req)
        listeTemp = DB.ResultatReq()
        self.dict_activites = {}
        for IDactivite, nom, date_debut, date_fin in listeTemp :
            date_debut = UTILS_Dates.DateEngEnDateDD(date_debut)
            date_fin = UTILS_Dates.DateEngEnDateDD(date_fin)
            self.dict_activites[IDactivite] = {"nom":nom, "date_debut":date_debut, "date_fin":date_fin}
        
        DB.Close() 

    def Importations_specifiques(self):
        self.listeInscriptionsAffichees = []
        
        if self.IDactivite == None :
            return False
            
        # Importation des données
        DB = GestionDB.DB()
        
        # Unités
        req = """SELECT IDunite, nom, abrege, type, heure_debut, heure_debut_fixe, heure_fin, heure_fin_fixe, 
        date_debut, date_fin
        FROM unites 
        WHERE IDactivite=%d
        ORDER BY ordre
        ;""" % self.IDactivite
        DB.ExecuterReq(req)
        listeTemp = DB.ResultatReq()
        self.listeUnites = []
        self.dictUnites = {}
        for IDunite, nom, abrege, type, heure_debut, heure_debut_fixe, heure_fin, heure_fin_fixe, date_debut, date_fin in listeTemp :
            date_debut = UTILS_Dates.DateEngEnDateDD(date_debut)
            date_fin = UTILS_Dates.DateEngEnDateDD(date_fin)
            dictTemp = {
                "IDunite":IDunite, "nom":nom, "abrege":abrege, "type":type, "heure_debut":heure_debut, 
                "heure_debut_fixe":heure_debut_fixe, "heure_fin":heure_fin, "heure_fin_fixe":heure_fin_fixe, 
                "date_debut":date_debut, "date_fin":date_fin, 
                "unites_incompatibles":[],
                }
            self.listeUnites.append(IDunite)
            self.dictUnites[IDunite] = dictTemp

        # Importation des incompatibilités entre unités
        req = """SELECT IDunite_incompat, IDunite, IDunite_incompatible
        FROM unites_incompat;"""
        DB.ExecuterReq(req)
        listeTemp = DB.ResultatReq()
        for IDunite_incompat, IDunite, IDunite_incompatible in listeTemp :
            if self.dictUnites.has_key(IDunite) : self.dictUnites[IDunite]["unites_incompatibles"].append(IDunite_incompatible)
            if self.dictUnites.has_key(IDunite_incompatible) : self.dictUnites[IDunite_incompatible]["unites_incompatibles"].append(IDunite)

        # Importation des ouvertures
        req = """SELECT IDouverture, IDunite, IDgroupe, date
        FROM ouvertures 
        WHERE IDactivite=%d AND date>='%s' AND date<='%s'
        ; """ % (self.IDactivite, self.dateDebut, self.dateFin)
        DB.ExecuterReq(req)
        listeTemp = DB.ResultatReq()
        self.listeOuvertures = []
        for IDouverture, IDunite, IDgroupe, date in listeTemp :
            date = UTILS_Dates.DateEngEnDateDD(date)
            self.listeOuvertures.append((date, IDunite, IDgroupe))

        # Importation des groupes
        req = """SELECT IDgroupe, abrege, nom, ordre
        FROM groupes 
        WHERE IDactivite=%d
        ;""" % self.IDactivite
        DB.ExecuterReq(req)
        listeTemp = DB.ResultatReq()
        self.dictGroupes = {}
        for IDgroupe, abrege, nom, ordre in listeTemp :
            self.dictGroupes[IDgroupe] = {"nom": nom, "abrege": abrege, "ordre":ordre}
            
        # Importation des consommations
        req = """SELECT IDconso, consommations.IDindividu, IDactivite, IDinscription, date, IDunite, 
        IDgroupe, heure_debut, heure_fin, etat, date_saisie, IDutilisateur, 
        IDcategorie_tarif, consommations.IDcompte_payeur, IDprestation, forfait, quantite,
        comptes_payeurs.IDfamille
        FROM consommations 
        LEFT JOIN comptes_payeurs ON comptes_payeurs.IDcompte_payeur = consommations.IDcompte_payeur
        WHERE IDactivite=%d AND date>='%s' AND date<='%s'
        ORDER BY date; """ % (self.IDactivite, self.dateDebut, self.dateFin)
        DB.ExecuterReq(req)
        listeTemp = DB.ResultatReq()
        self.dictConso = {}
        for IDconso, IDindividu, IDactivite, IDinscription, date, IDunite, IDgroupe, heure_debut, heure_fin, etat, date_saisie, IDutilisateur, IDcategorie_tarif, IDcompte_payeur, IDprestation, forfait, quantite, IDfamille in listeTemp :
            date = UTILS_Dates.DateEngEnDateDD(date)
            date_saisie = UTILS_Dates.DateEngEnDateDD(date_saisie)
            dictTemp = {
                "IDconso":IDconso, "IDindividu":IDindividu, "IDactivite":IDactivite, "IDinscription":IDinscription, "date":date, "IDunite":IDunite, "IDgroupe":IDgroupe, 
                "heure_debut":heure_debut, "heure_fin":heure_fin, "etat":etat, "date_saisie":date_saisie, "IDutilisateur":IDutilisateur, "IDcategorie_tarif":IDcategorie_tarif,
                "IDcompte_payeur":IDcompte_payeur, "IDprestation":IDprestation, "forfait":forfait, "quantite":quantite, "IDfamille":IDfamille, 
                }
            self.dictConso[(IDinscription, date, IDunite)] = dictTemp

        # Importation des titulaires
        req = """SELECT IDfamille, nom
        FROM titulaires;"""
        DB.ExecuterReq(req)
        listeTemp = DB.ResultatReq()
        self.dictTitulaires = {}
        for IDfamille, nom in listeTemp :
            self.dictTitulaires[IDfamille] = nom
            
        # Importation des inscriptions
        req = """SELECT IDinscription, inscriptions.IDindividu, IDfamille, IDcompte_payeur, IDgroupe, IDcategorie_tarif,
        individus.nom, individus.prenom
        FROM inscriptions 
        LEFT JOIN individus ON individus.IDindividu = inscriptions.IDindividu
        WHERE IDactivite=%d 
        ORDER BY nom, prenom; """ % self.IDactivite
        DB.ExecuterReq(req)
        listeTemp = DB.ResultatReq()
        self.listeInscriptions = []
        self.dictInscriptions = {}
        dictTempInscriptions = {}
        for IDinscription, IDindividu, IDfamille, IDcompte_payeur, IDgroupe, IDcategorie_tarif, nom, prenom in listeTemp :
            if prenom == None : prenom = ""
            nomComplet = nom + " " + prenom
            dictTemp = {
                "IDinscription":IDinscription, "IDindividu":IDindividu, "IDfamille":IDfamille, "IDcompte_payeur":IDcompte_payeur, 
                "IDgroupe":IDgroupe, "IDcategorie_tarif":IDcategorie_tarif, "nom":nom, "prenom":prenom, "nomComplet":nomComplet,
                }
            self.listeInscriptions.append(dictTemp)
            self.dictInscriptions[IDinscription] = dictTemp
            
            # Pour trouver les rattachements multiples
            if dictTempInscriptions.has_key(IDindividu) == False :
                dictTempInscriptions[IDindividu] = []
            dictTempInscriptions[IDindividu].append((IDfamille, IDinscription))

        for IDindividu, listeFamilles in dictTempInscriptions.iteritems() :
            if len(listeFamilles) > 1 :
                for IDfamille, IDinscription in listeFamilles :
                    nomTitulaires = self.dictTitulaires[IDfamille] 
                    nomComplet = self.dictInscriptions[IDinscription]["nomComplet"] + "\n[size=12][color=c0c0c0](" + nomTitulaires + ")[/color][/size]"
                    self.dictInscriptions[IDinscription]["nomComplet"] = nomComplet

        # Mémos journaliers
        req = """SELECT IDmemo, IDindividu, date, texte
        FROM memo_journee 
        WHERE date>='%s' AND date<='%s'
        ORDER BY date; """ % (self.dateDebut, self.dateFin)
        DB.ExecuterReq(req)
        listeTemp = DB.ResultatReq()
        self.dictMemos = {}
        for IDmemo, IDindividu, date, texte in listeTemp :
            date = UTILS_Dates.DateEngEnDateDD(date)
            self.dictMemos[(IDindividu, date)] = {"texte" : texte, "IDmemo" : IDmemo}
        
        DB.Close() 

        # Importation des actions-consommations
        DB = GestionDB.DB(typeFichier="actions")
        req = """SELECT IDconso, horodatage, action, IDindividu, IDactivite, IDinscription, date, IDunite, 
        IDgroupe, heure_debut, heure_fin, etat, date_saisie, IDutilisateur, 
        IDcategorie_tarif, IDcompte_payeur, quantite, IDfamille
        FROM consommations 
        WHERE IDactivite=%d AND date>='%s' AND date<='%s'
        ORDER BY IDconso; """ % (self.IDactivite, self.dateDebut, self.dateFin)
        DB.ExecuterReq(req)
        listeTemp = DB.ResultatReq()
        
        for IDconso, horodatage, action, IDindividu, IDactivite, IDinscription, date, IDunite, IDgroupe, heure_debut, heure_fin, etat, date_saisie, IDutilisateur, IDcategorie_tarif, IDcompte_payeur, quantite, IDfamille in listeTemp :
            date = UTILS_Dates.DateEngEnDateDD(date)
            date_saisie = UTILS_Dates.DateEngEnDateDD(date_saisie)
            dictTemp = {
                "IDconso":IDconso, "IDindividu":IDindividu, "IDactivite":IDactivite, "IDinscription":IDinscription, "date":date, "IDunite":IDunite, "IDgroupe":IDgroupe, 
                "heure_debut":heure_debut, "heure_fin":heure_fin, "etat":etat, "date_saisie":date_saisie, "IDutilisateur":IDutilisateur, "IDcategorie_tarif":IDcategorie_tarif,
                "IDcompte_payeur":IDcompte_payeur, "quantite":quantite, "IDfamille":IDfamille, #"forfait":forfait, 
                }
            
            # Recherche si l'action est plus récente que la consommation initiale
            #if self.dictConso.has_key((IDinscription, date, IDunite)) :
            #    date_saisie_ancienne_conso = self.dictConso[(IDinscription, date, IDunite)]["date_saisie"]
            
            # Si oui, on écrase l'ancienne consommation
            if True: #date_saisie > date_saisie_ancienne_conso :
                key = (IDinscription, date, IDunite)
                if action == "ajouter" or action == "modifier" :
                    self.dictConso[key] = dictTemp
                if action == "supprimer" :
                    if self.dictConso.has_key(key) :
                        del self.dictConso[key]
        
        self.dictConsoInitial = copy.deepcopy(self.dictConso)

        # Importation des actions-mémos journaliers
        req = """SELECT IDmemo, horodatage, action, IDindividu, date, texte
        FROM memo_journee 
        WHERE date>='%s' AND date<='%s'
        ORDER BY IDmemo; """ % (self.dateDebut, self.dateFin)
        DB.ExecuterReq(req)
        listeTemp = DB.ResultatReq()
        for IDmemo, horodatage, action, IDindividu, date, texte in listeTemp :
            date = UTILS_Dates.DateEngEnDateDD(date)
            self.dictMemos[(IDindividu, date)] = {"texte" : texte, "IDmemo" : IDmemo}
        
        self.dictMemosInitial = copy.deepcopy(self.dictMemos)
        
        DB.Close() 
        
        return True

    def on_change_height(self, *args):
        self.Draw_grille()
        self.Affiche_page_actuelle()

    def Draw_grille(self, importer=False):
        self.box_grille.clear_widgets()
        
        if self.IDactivite == None :
            return False

        # Importation des données
        if importer == True :
            if self.Importations_specifiques() == False :
                return False
                
        # Dessin des headers
        hauteur_ligne = 50
        self.box_cases = GridLayout(cols=len(self.listeUnites)+2, row_force_default=True, row_default_height=hauteur_ligne, size_hint=(1, 1), spacing=(5, 5))
        self.box_grille.add_widget(self.box_cases)
        
        ctrl_label = Label(text="", size_hint=(1, None))
        self.box_cases.add_widget(ctrl_label)
        
        for IDunite in self.listeUnites :
            dictUnite = self.dictUnites[IDunite]
            ctrl_label = Label(text=dictUnite["abrege"], size_hint=(0.3, None))
            self.box_cases.add_widget(ctrl_label)
        
        ctrl_label = Label(text="Mémo journalier", size_hint=(1, None))
        self.box_cases.add_widget(ctrl_label)
        
        # Dessin des cases
        
        # Calcul de l'affichage des pages
        self.nbreLignesParPage = int(math.floor((self.box_grille.height - self.box_grille.padding[1] - hauteur_ligne) / (self.box_cases.row_default_height * 1.0 + self.box_cases.spacing[1])))
        
        # Création des contrôles
        self.dictCasesParLigne = {}
        for numLigne in range(0, self.nbreLignesParPage):
            dictCasesLigne = {"entete":None, "unites":{}, "memo":None}
            
            # Case entete de ligne
            ctrl_entete = LabelEnteteLigne(text="", size_hint=(1, None), height=hauteur_ligne, markup=True, halign="center")
            self.box_cases.add_widget(ctrl_entete)
            dictCasesLigne["entete"] = ctrl_entete
            
            # Unités
            for IDunite in self.listeUnites :
                ctrl_case = BoutonCase(text="", size_hint=(0.3, None), height=hauteur_ligne, IDunite=IDunite, numLigne=numLigne, grille=self)
                self.box_cases.add_widget(ctrl_case)
                dictCasesLigne["unites"][IDunite] = ctrl_case
            
            # Mémo journalier
            ctrl_memo = BoutonMemo(text="", size_hint=(1, None), height=hauteur_ligne, grille=self)
            self.box_cases.add_widget(ctrl_memo)
            dictCasesLigne["memo"] = ctrl_memo
            
            self.dictCasesParLigne[numLigne] = dictCasesLigne
        
        self.pageActuelle = 0
        #self.AfficherPresents() 
        
        

    def Affiche_page_actuelle(self):
        """ Affichage de la page actuelle """
        t1 = time.time()
        
        if self.IDactivite == None :
            return
                    
        # Tri par ordre alphabétique des présents
        listeInscriptionsAlpha = []
        for IDinscription in self.listeInscriptionsAffichees :
            if IDinscription != None :
                listeInscriptionsAlpha.append((self.dictInscriptions[IDinscription]["nomComplet"], IDinscription))
        listeInscriptionsAlpha.sort() 
        
        # Calcul de l'affichage des pages
        if self.nbreLignesParPage == 0 :
            return
        #nbrePages = int(len(listeInscriptionsAlpha) / self.nbreLignesParPage)
        
        self.dictLignesParPage = {}
        self.dictPageLignes = {}
        numPage = 0
        numLigne = 0
        for nomComplet, IDinscription in listeInscriptionsAlpha :
            # Mémorisation par page
            if self.dictLignesParPage.has_key(numPage) == False :
                self.dictLignesParPage[numPage] = []
            self.dictLignesParPage[numPage].append(IDinscription)
            # Mémorisation du numéro de page pour chaque ligne
            self.dictPageLignes[IDinscription] = numPage
            # Saut à la page suivante
            numLigne += 1
            if numLigne >= self.nbreLignesParPage :
                numPage += 1
                numLigne = 0
        #print "self.dictLignesParPage =", self.dictLignesParPage
        
        nbrePages = len(self.dictLignesParPage)
        #print "nbrePages=", nbrePages
        #print "self.nbreLignesParPage=", self.nbreLignesParPage
        #print "len(self.dictLignesParPage)=", len(self.dictLignesParPage)
        #print "len(self.dictPageLignes)=", len(self.dictPageLignes)

        # Remplissage des contrôles
        for numLigne in range(0, self.nbreLignesParPage) :
            
            if self.mode == "date" :
                date = self.dateDebut
  
            # Recherche si inscription existe pour cette ligne
            IDinscription = None
            if self.dictLignesParPage.has_key(self.pageActuelle) :
                if numLigne < len(self.dictLignesParPage[self.pageActuelle]) :
                    IDinscription = self.dictLignesParPage[self.pageActuelle][numLigne]
                    dictInscription = self.dictInscriptions[IDinscription]
            
            # Entete de ligne
            case = self.dictCasesParLigne[numLigne]["entete"]
            if IDinscription != None :
                case.text = dictInscription["nomComplet"]
                case.opacity = 1
            else :
                case.opacity = 0
            
            # Unités
            for IDunite in self.listeUnites :
                case = self.dictCasesParLigne[numLigne]["unites"][IDunite]
                
                if IDinscription != None :
                
                    # Recherche si conso existe
                    key = (IDinscription, date, IDunite)
                    if self.dictConso.has_key(key):
                        dictConso = self.dictConso[key]
                    else :
                        dictConso = {}
                    
                    # Affichage de la case
                    if (date, IDunite, dictInscription["IDgroupe"]) in self.listeOuvertures :
                        ouvert = True
                    else :
                        ouvert = False
                    
                    case.opacity = 1
                    case.ouvert = ouvert
                    case.date = date
                    case.dictInscription = dictInscription
                    case.dictConso = dictConso
                    case.MAJ() 
                
                else :
                    case.opacity = 0
            
            # Mémo journalier
            case = self.dictCasesParLigne[numLigne]["memo"]
            if IDinscription != None :
                case.dictInscription = dictInscription
                case.date = date
                case.opacity = 1
                key = (dictInscription["IDindividu"], date)
                if self.dictMemos.has_key(key) :
                    case.text = self.dictMemos[key]["texte"]
                else :
                    case.text = ""
            else :
                case.text = ""
                case.opacity = 0
        
        # Ajustement du slider
        self.slider_pages.max = nbrePages
        self.slider_pages.value = self.pageActuelle

        # Affichage du chrono
        #temps = str(time.time()-t1)
        #print("Temps d'actualisation de la page =" + temps)
    



    def on_slider_pages(self, ctrl):
        self.pageActuelle = ctrl.value
        self.Affiche_page_actuelle()
                
    def on_bouton_ajouter_inscription(self):
        """ Ajouter un individu """
        from selection_inscription import SelectionInscription
        popup = SelectionInscription(IDactivite=self.IDactivite, callback=self.ValiderAjoutInscription)
        popup.open()
    
    def ValiderAjoutInscription(self, IDinscription=None):
        if IDinscription not in self.listeInscriptionsAffichees :
            self.listeInscriptionsAffichees.append(IDinscription)
        else :
            MsgBox.info(text="Cet individu est déjà dans la liste affichée !", title="Remarque", size_hint=(0.6, 0.6))
        # Actualisation de l'affichage
        self.Affiche_page_actuelle()
        # Sélectionne la page de l'individu
        self.RechercherIndividu(IDinscription=IDinscription)
        
    def on_bouton_afficher_inscrits(self):
        """ Afficher tous les inscrits """
        self.listeInscriptionsAffichees = self.dictInscriptions.keys()
        self.pageActuelle = 0        
        self.Affiche_page_actuelle()

    def on_bouton_afficher_presents(self):
        """ Afficher uniquement les présents """
        self.AfficherPresents()
        
    def AfficherPresents(self):
        listeInscriptionsPresents = []
        for (IDinscription, date, IDunite) in self.dictConso.keys() :
            if IDinscription not in listeInscriptionsPresents :
                listeInscriptionsPresents.append(IDinscription)
        self.listeInscriptionsAffichees = listeInscriptionsPresents
        self.pageActuelle = 0
        self.Affiche_page_actuelle()
    
    def on_bouton_selection_date(self):
        from selection_date import SelectionDate
        date = self.dateDebut
        popup = SelectionDate(title="Sélectionnez une date", date=date, callback=self.Selection_date, size_hint=(0.8, 0.8))
        popup.open() 
            
    def Selection_date(self, date=None, refreshGrille=True):
        self.dateDebut = date
        self.dateFin = date
        if refreshGrille :
            self.Draw_grille(importer=True) 
            self.AfficherPresents() 
        self.ctrl_date.text = "Date : [b][color=a8ca2f]%s[/color][/b]" % UTILS_Dates.DateDDEnFr(date)

    def on_bouton_selection_activite(self):
        self.DemandeEnregistrer()
        from selection_activite import SelectionActivite
        popup = SelectionActivite(title="Sélectionnez une activité", IDactivite=self.IDactivite, callback=self.Selection_activite, size_hint=(0.8, 0.8))
        popup.open()   
        
    def Selection_activite(self, IDactivite=None, refreshGrille=True):
        self.IDactivite = IDactivite
        if refreshGrille :
            self.Draw_grille(importer=True) 
            self.AfficherPresents() 
        if IDactivite == None or self.dict_activites.has_key(IDactivite) == False :
            nomActivite = "Aucune"
        else :
            nomActivite = self.dict_activites[IDactivite]["nom"]
        self.ctrl_activite.text = "Activité : [b][color=a8ca2f]%s[/color][/b]" % nomActivite.encode("utf-8")

    def on_bouton_selection_etat(self):
        from selection_etat import SelectionEtat
        popup = SelectionEtat(title="Sélectionnez un mode de saisie", etat=self.etat, callback=self.Selection_etat, size_hint=(0.8, 0.8))
        popup.open()   
        
    def Selection_etat(self, etat=""):
        self.etat = etat
        self.ctrl_etat.text = "Mode : [b][color=a8ca2f]%s[/color][/b]" % GetLabelEtat(etat)
        
    def on_bouton_navigation_premier(self):
        self.pageActuelle = 0
        self.Affiche_page_actuelle()
        
    def on_bouton_navigation_precedent(self):
        if self.pageActuelle > 0 :
            self.pageActuelle -= 1
        self.Affiche_page_actuelle()
        
    def on_bouton_navigation_suivant(self):
        if self.pageActuelle < len(self.dictLignesParPage) - 1 :
            self.pageActuelle += 1
        self.Affiche_page_actuelle()
        
    def on_bouton_navigation_dernier(self):
        self.pageActuelle = len(self.dictLignesParPage) - 1
        self.Affiche_page_actuelle()
    
    def on_bouton_navigation_nom(self):
        """ Recherche du nom d'un individu """
        from selection_nom import SelectionNom
        popup = SelectionNom(title="Tapez une partie du nom ou du prénom à rechercher", callback=self.RechercherNomIndividu)
        popup.open()  
    
    def SetFlashLigne(self, numLigne=None):
        case = self.dictCasesParLigne[numLigne]["entete"]
        case.color = (1, 0, 0, 1)
        anim = Animation(color=(1, 1, 1, 1), duration=3)
        anim.start(case)
        
    def RechercherIndividu(self, IDinscription=None, IDindividu=None):
        """ Rechercher un individu depuis son IDindividu ou son IDinscription """
        for numPage, listeInscriptions in self.dictLignesParPage.iteritems() :
            numLigne = 0
            for IDinscriptionTemp in listeInscriptions :
                dictInscription = self.dictInscriptions[IDinscriptionTemp]
                if IDinscriptionTemp == IDinscription or dictInscription["IDindividu"] == IDindividu :
                    self.pageActuelle = numPage
                    self.Affiche_page_actuelle()
                    self.SetFlashLigne(numLigne=numLigne)
                    return
                numLigne += 1
        
    def RechercherNomIndividu(self, texte=None):
        """ Rechercher une ligne d'après le nom de l'individu """
        texte = texte.decode("utf-8")
        for numPage, listeInscriptions in self.dictLignesParPage.iteritems() :
            numLigne = 0
            for IDinscription in listeInscriptions :
                if texte.lower() in self.dictInscriptions[IDinscription]["nomComplet"].lower() :
                    self.pageActuelle = numPage
                    self.Affiche_page_actuelle()
                    self.SetFlashLigne(numLigne=numLigne)
                    return
                numLigne += 1
        # Si aucun individu trouvé
        MsgBox.info(text="Aucun nom ne contient ce texte !", title="Echec de la recherche", size_hint=(0.6, 0.6))

    def on_bouton_navigation_lettre(self):
        """ Recherche du nom d'un individu """
        from selection_lettre import SelectionLettre
        popup = SelectionLettre(title="Sélectionnez une lettre",callback=self.RechercherPremiereLettre, size_hint=(0.8, 0.8))
        popup.open()  

    def RechercherPremiereLettre(self, lettre=None):
        """ Rechercher une ligne selon la première lettre du nom de l'individu """
        # Recherche si un nom commence par cette lettre
        for numPage, listeInscriptions in self.dictLignesParPage.iteritems() :
            for IDinscription in listeInscriptions :
                if self.dictInscriptions[IDinscription]["nomComplet"].lower().startswith(lettre.lower()) :
                    self.pageActuelle = numPage
                    self.Affiche_page_actuelle()
                    return
        # Si aucun individu trouvé
        MsgBox.info(text="Aucun nom ne commence par cette lettre !", title="Echec de la recherche", size_hint=(0.6, 0.6))
                    
    def on_bouton_enregistrer(self):
        self.Enregistrer() 
    
    def Enregistrer(self):
        t1 = time.time()
        listeActionsConsommations = []
        listeActionsMemos = []
        
        # Recherche les modifications effectuées
        for categorie, key in self.listeModifications :
        
            if categorie == "consommation" :
            
                # Recherche dictConso initial
                if self.dictConsoInitial.has_key(key) :
                    dictConsoInitial = self.dictConsoInitial[key]
                else :
                    dictConsoInitial = None
                
                # Recherche dictConso finale
                if self.dictConso.has_key(key) :
                    dictConsoFinale = self.dictConso[key]
                else :
                    dictConsoFinale = None
                
                # Comparaison de la conso initiale et de la conso finale
                listeKeys = ["IDindividu", "IDactivite", "date_saisie", "IDcategorie_tarif", "IDcompte_payeur", "etat", "quantite", "IDinscription", "IDunite", "heure_debut", "heure_fin", "date", "IDgroupe", "IDfamille"]
                
                if dictConsoInitial == None and dictConsoFinale != None :
                    listeActionsConsommations.append(("ajouter", dictConsoFinale))
                elif dictConsoInitial != None and dictConsoFinale != None :
                    listeActionsConsommations.append(("modifier", dictConsoFinale))
                elif dictConsoInitial != None and dictConsoFinale == None :
                    listeActionsConsommations.append(("supprimer", dictConsoInitial))
                else :
                    typeAction = None
        
      
        # Recherche des modifications des mémos journaliers
        for key, dictMemo in self.dictMemos.iteritems():
            texte = dictMemo["texte"]
            IDmemo = dictMemo["IDmemo"]
            donnees = {"IDindividu" : key[0], "date" : key[1], "texte" : texte}
            if self.dictMemosInitial.has_key(key) :
                if texte == "" :
                    listeActionsMemos.append(("supprimer", donnees))
                else :
                    if self.dictMemosInitial[key]["texte"] != texte :
                        listeActionsMemos.append(("modifier", donnees))
            else :
                listeActionsMemos.append(("ajouter", donnees))

        # ---------------------------------------------------------------------
        def GetValeurs(listeChamps, dictConso):
            listeValeurs = []
            for nomChamp in listeChamps :
                if dictConso.has_key(nomChamp) :
                    listeValeurs.append(dictConso[nomChamp])
                else :
                    listeValeurs.append(None)
            return listeValeurs
        
        # --------------- Sauvegarde des actions ----------------
        
        DB = GestionDB.DB(typeFichier="actions")
        
        # Mémos journaliers
        if len(listeActionsMemos) > 0 :
            listeChampsActions = ["horodatage", "action", "IDindividu", "date", "texte"]
            listeAjouts = []
            for typeAction, dictMemo in listeActionsMemos :
                dictMemo["horodatage"] = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())
                dictMemo["action"] = typeAction
                listeAjouts.append(GetValeurs(listeChampsActions, dictMemo))
            req = "INSERT INTO memo_journee (%s) VALUES (%s)" % (", ".join(listeChampsActions), ", ".join(["?" for x in range(len(listeChampsActions))]))
            DB.Executermany(req, listeAjouts, commit=False)
            DB.Commit()
            DB.Close()             

            
        # Consommations
        if len(listeActionsConsommations) > 0 :
            listeChampsActions = [
                "horodatage", "action", "IDindividu", "IDactivite", "IDinscription", "date", "IDunite", "IDgroupe", 
                "heure_debut", "heure_fin", "etat", "IDutilisateur", "IDcategorie_tarif", "IDcompte_payeur", "quantite", "IDfamille",
                ]

            listeAjouts = []
            for typeAction, dictConso in listeActionsConsommations :
                dictConso["horodatage"] = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())
                dictConso["action"] = typeAction
                listeAjouts.append(GetValeurs(listeChampsActions, dictConso))
            req = "INSERT INTO consommations (%s) VALUES (%s)" % (", ".join(listeChampsActions), ", ".join(["?" for x in range(len(listeChampsActions))]))
            DB.Executermany(req, listeAjouts, commit=False)
            DB.Commit()
        
        DB.Close()             
                    
        self.listeModifications = []
        self.dictConsoInitial = copy.deepcopy(self.dictConso)     
        self.dictMemosInitial = copy.deepcopy(self.dictMemos)
                    
    def on_bouton_annuler(self):
        if len(self.listeModifications) > 0 :
            MsgBox.question(text="Souhaitez-vous vraiment annuler les %d modifications effectuées ?" % len(self.listeModifications), title="Annuler", yes_callback=lambda: self.Annuler(), size_hint=(0.6, 0.6))
        else :
            MsgBox.info(text="Il n'existe aucune modification à annuler !", title="Annuler", size_hint=(0.6, 0.6))
            
    def Annuler(self):
        self.Draw_grille(importer=True) 
        self.AfficherPresents() 
    
    def On_leave(self):
        self.DemandeEnregistrer()
        
    def DemandeEnregistrer(self):
        if len(self.listeModifications) > 0 :
            MsgBox.question(text="Souhaitez-vous enregistrer les %d modifications effectuées ?" % len(self.listeModifications), title="Enregistrer", yes_callback=lambda: self.Enregistrer(), size_hint=(0.6, 0.6))
        
    def on_bouton_afficher_totaux(self):
        dictResultats = {}
        # Unités
        for (IDinscription, date, IDunite), dictConso in self.dictConso.iteritems() :
            if dictConso["etat"] in ("reservation", "present"):
                IDgroupe = dictConso["IDgroupe"]
                if dictResultats.has_key(IDunite) == False :
                    dictResultats[IDunite] = {}
                if dictResultats[IDunite].has_key(IDgroupe) == False :
                    dictResultats[IDunite][IDgroupe] = 0
                dictResultats[IDunite][IDgroupe] += 1
        
        # Recherche des noms de groupes
        listeGroupes = []
        for IDgroupe, dictGroupe in self.dictGroupes.iteritems() :
            listeGroupes.append((dictGroupe["ordre"], IDgroupe, dictGroupe["nom"]))
        listeGroupes.sort() 
        
        # Formatage des donnees en tableau
        donnees = []
        
        # Header
        ligne = ["",]
        for ordre, IDgroupe, nomGroupe in listeGroupes :
            ligne.append(nomGroupe)
        ligne.append("Total")
        donnees.append(ligne)
        
        
        # Unités
        for IDunite in self.listeUnites :   
            nomUnite = self.dictUnites[IDunite]["abrege"]
            ligne = [nomUnite,]
            totalLigne = 0
            for ordre, IDgroupe, nomGroupe in listeGroupes :
                valeur = 0
                if dictResultats.has_key(IDunite) :
                    if dictResultats[IDunite].has_key(IDgroupe) :
                        valeur = dictResultats[IDunite][IDgroupe]
                ligne.append(valeur)
                totalLigne += valeur
            ligne.append(totalLigne)
            donnees.append(ligne)
        
        from totaux import Totaux
        popup = Totaux(title="Totaux", donnees=donnees, size_hint=(0.8, 0.8))
        popup.open()  
        
        
        
        
class MyApp(App):
    IDutilisateur = None
    def build(self):
        mainView = Grille(app=self)
        mainView.IDactivite = 1
        mainView.MAJ()
        return mainView

if __name__ == '__main__':
    MyApp().run()