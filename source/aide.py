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
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.rst import RstDocument
from kivy.uix.tabbedpanel import TabbedPanelItem

LISTE_TEXTES = [
("Commencer", """
Vous découvrez [color=a8ca2f][b]Nomadhys[/color][/b] pour la première fois ? Voici comment commencer...

1- Cliquez sur le bouton **Paramètres** du menu principal puis sur la ligne **IDfichier**. Saisissez les 17 caractères du fichier de données Noethys
avec lequel vous souhaitez travailler. Vous trouverez ce code dans Noethys (**Menu Fichier > Informations > IDfichier**). Reportez-le sans faire d'erreur.

2- Cliquez sur le bouton **Synchronisation** du menu principal. Sélectionnez le type de transfert souhaité pour cliquer sur le bouton **Recevoir** pour récupérer
le fichier de données de Noethys. En fonction du type de transfert utilisé, vous aurez peut-être besoin de renseigner des paramètres de synchronisation. Pour en savoir davantage, consultez le chapitre **Synchronisation** de l'aide.

L'application est maintenant prête à être utilisée. Il ne vous reste plus qu'à cliquer sur les boutons **Individus** ou **Consommations** pour accéder aux données.

""",),

("Individus", """
[color=a8ca2f][b]Nomadhys[/color][/b] permet de consulter les principales informations sur un individu.
Ces informations ne sont pas modifiables directement dans l'application nomade.

1- Pour consulter une fiche individuelle, cliquez sur le bouton **Individus** du menu principal. Si vous n'êtes pas
encore identifié, votre code utilisateur vous sera demandé à cette étape.

2- Tapez une partie du nom ou une partie du prénom dans le champ de saisie puis cliquez sur **Ok**.

3- La fiche individuelle apparaît. 

Remarque : Pensez à synchroniser régulièrement le fichier de données (Voir **Synchronisation**) afin de bénéficier
d'informations à jour.
""",),

("Consommations", """
Vous pouvez dans [color=a8ca2f][b]Nomadhys[/color][/b] consulter et modifier les consommations des individus.

1- Cliquez sur le bouton **Consommations** du menu principal pour ouvrir la grille des consommations. Si vous n'êtes pas
encore identifié, votre code utilisateur vous sera demandé à cette étape.

2- Sélectionnez la date et l'activité à afficher.

3- La grille des consommations de [color=a8ca2f][b]Nomadhys[/color][/b] ressemble beaucoup à celle de Noethys.
Cliquez sur les cases pour ajouter ou supprimer une consommation. **Important : Pour modifier ou accéder aux détails d'une consommation,
appuyez pendant 2 secondes sur la case souhaitée**.

L'enregistrement des données n'est pas effectuée en temps réél pour des raisons de performances. Vous devez cliquer
sur le bouton **Enregistrer** pour sauvegarder les données. Si vous quitter la grille des consommations sans avoir enregistré,
l'application fera cette sauvegarde automatiquement.

Remarque : Pensez à synchroniser régulièrement vos données pour récupérer les données les plus récentes et pour
envoyer vos modifications à Noethys.

""",),

("Synchronisation", """
La synchronisation des données consiste à récupérer les données de base du fichier de Noethys et à renvoyer les modifications effectuées
sur l'application.

[color=a8ca2f][b]Nomadhys[/color][/b] propose 3 méthodes de synchronisation :

**A- Serveur Internet/WIFI :**

Lancez Noethys sur un ordinateur avec l'option "Serveur Internet/WIFI" activé (Menu Outil > Synchroniser Nomadhys).
Le cadre "Serveur Nomadhys" de la page d'accueil affiche un IP local et un IP internet. Si vous êtes sur le réseau
WIFI de cet ordinateur, reportez cet IP dans Les paramètres de connexion de Nomadhys, sinon reportez l'IP internet.
Allez ensuite sur **Nomadhys** > **Synchronisation** puis cliquez sue le bouton **Recevoir** pour récupérer les données
de Noethys ou sur **Envoyer** pour envoyer les modifications à Noethys.

**B- Transfert par FTP :**

Vous devez disposer d'un hébergement FTP (celui de votre site internet par exemple si vous en avez un). Les fichiers 
de synchronisation transiteront simplement par cet hébergement.

La première fois, vous devez créer un répertoire de stockage sur votre hébergement internet (Par exemple "www/nomadhys").

Dans les paramètres de connexion de Nomadhys et de Noethys, vous devez ensuite renseigner les champs suivants :
Hote FTP , Utilisateur FTP, Mot de passe FTP et répertoire de stockage.

Cliquez ensuite sur les boutons **Recevoir** ou **Envoyer** pour synchroniser les données dans Noethys et Nomadhys.

**C- Transfert manuel :**

Cette méthode est à utiliser si vous ne pouvez pas utiliser les deux méthodes précédentes. Il faut alors indiquer
à Nomadhys et à Noethys où se trouvent les fichiers de synchronisation (disque sur, clé USB, etc...).

""",),

]



Builder.load_string("""
<Aide>
    tab_aide: tab_aide
    
    BoxLayout:
        orientation: 'vertical'
        
        TabbedPanel: 
            id: tab_aide
            do_default_tab: False
            tab_width: 150
            padding: 10
                                
        GridLayout:
            cols: 3
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
                id: ctrl_etat
                text: ''
                markup: True
                font_size: 14
                size_hint: 1, None
                v_align: 'middle'
                text_size: (self.size[0], None)

            
""")
            
class Aide(Screen):
    tab_aide = ObjectProperty() 
    
    def __init__(self, *args, **kwargs):
        super(Screen, self).__init__(*args, **kwargs)	
        self.MAJeffectuee = False
    
    def MAJ(self):
        if self.MAJeffectuee == True :
            return
        listeOnglets = []
        for titre, texte in LISTE_TEXTES :
            onglet = TabbedPanelItem(text=titre)
            doc = RstDocument(text=texte)
            onglet.add_widget(doc)
            self.tab_aide.add_widget(onglet)
            listeOnglets.append(onglet)
        self.tab_aide.switch_to(listeOnglets[0])
        self.MAJeffectuee = True
        
class MyApp(App):
    def build(self):
        screen = Aide()
        screen.MAJ()
        return screen
    
    def test(self):
        print("ok")
        


if __name__ == '__main__':
    MyApp().run()