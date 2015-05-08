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
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import get_color_from_hex
from kivy.core.window import Window
from kivy.properties import StringProperty, ListProperty, NumericProperty, ObjectProperty, DictProperty, BooleanProperty
from kivy.animation import Animation
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.modalview import ModalView

import copy

Builder.load_string("""

<BoutonTransparent>:
    size_hint: 1, 0.8
    background_normal: ''
    background_color: (1, 1, 1, 0)
    on_press: root.Animer()
    
    Image:
        source: root.chemin_image
        center: root.center

        
<Attente>
    anchor_x: 'center'
    anchor_y: 'center'
    size_hint: 1, 1
    
    Image:
        source: 'images/attente.gif'
        center: root.center
        
        canvas.before:
            PushMatrix
            Rotate:
                angle: root.angle
                axis: 0, 0, 1
                origin: root.center
        canvas.after:
            PopMatrix

            
<BoutonAvecImageEtroit>:
	text: ''
	size_hint: None, 1
    width: ctrl_image.width + ctrl_label.width + box.spacing + box.padding[0]*2
    
	BoxLayout:
        id: box
		orientation: 'horizontal'
		center: root.center
        size: root.size
		size_hint: None, 1
		spacing: 0
        padding: 5
		
		#canvas.before:
		#	Color:
		#	    rgba: 1, 0.5, 0, 1
		#	Rectangle:
		#	    pos: self.pos
		#	    size: self.size  
			
		Image:
            id: ctrl_image
			source: root.chemin_image
			size_hint: None, 1
            width: self.height
            center_y: root.center_y
			
			#canvas.before:
			#	Color:
			#		rgba: 0.5, 0.4, 0, 1
			#	Rectangle:
			#		pos: self.pos
			#		size: self.size  
			
		Label:
            id: ctrl_label
			text: root.texte
            halign: 'left'
            valign: 'middle'
            #text_size: self.width, self.height
            size: self.texture_size
			size_hint: 1, 1
			
			#canvas.before:
			#	Color:
			#		rgba: 0, 0, 1, 1
			#	Rectangle:
			#		pos: self.pos
			#		size: self.size  
                    

                    
        




        
<BoutonAvecImageLarge>:
	text: ''
	size_hint: 1, 1
    taille_image: (22, 22) # (None, None) pour avoir taille originale de l'image
    
    background_normal: ''
    background_color: (0.128, 0.128, 0.128, 1)
    background_disabled_normal: ''
    
	BoxLayout:
        id: box
		orientation: 'horizontal'
		center: root.center
        size: self.size
		size_hint: 1, 1
		spacing: 5
        padding: 0
        width: ctrl_image.width + ctrl_label.width + box.spacing + box.padding[0]*2
        height: ctrl_image.height
		
		#canvas.before:
		#	Color:
		#	    rgba: 1, 0.5, 0, 1
		#	Rectangle:
		#	    pos: self.pos
		#	    size: self.size  
			
		Image:
            id: ctrl_image
			source: root.chemin_image
			size_hint: None, 1
            size: self.texture_size if root.taille_image[0] == None else root.taille_image
            center_y: root.center_y
            opacity: 0.2 if root.disabled else 1
			
			#canvas.before:
			#	Color:
			#		rgba: 0.5, 0.4, 0, 1
			#	Rectangle:
			#		pos: self.pos
			#		size: self.size  
			
		Label:
            id: ctrl_label
			text: root.texte
            #halign: 'left'
            valign: 'middle'
            #text_size: self.width, self.height
            size: self.texture_size
			size_hint: None, 1
			
			#canvas.before:
			#	Color:
			#		rgba: 0, 0, 1, 1
			#	Rectangle:
			#		pos: self.pos
			#		size: self.size  


<BoutonAvecImageLarge_fond_normal>:
	text: ''
	size_hint: 1, 1
    taille_image: (22, 22) # (None, None) pour avoir taille originale de l'image
    
	BoxLayout:
        id: box
		orientation: 'horizontal'
		center: root.center
        size: self.size
		size_hint: 1, 1
		spacing: 5
        padding: 0
        width: ctrl_image.width + ctrl_label.width + box.spacing + box.padding[0]*2
        height: ctrl_image.height
			
		Image:
            id: ctrl_image
			source: root.chemin_image
			size_hint: None, 1
            size: self.texture_size if root.taille_image[0] == None else root.taille_image
            center_y: root.center_y
            opacity: 0.2 if root.disabled else 1
			
		Label:
            id: ctrl_label
			text: root.texte
            #halign: 'left'
            valign: 'middle'
            #text_size: self.width, self.height
            size: self.texture_size
			size_hint: None, 1



<BoutonFichier>:
	text: ''
    logo: logo
	size_hint: 1, 1
    #taille_image: (22, 22) # (None, None) pour avoir taille originale de l'image
    
    background_normal: ''
    background_color: (0.128, 0.128, 0.128, 1)
    background_disabled_normal: ''
    
	BoxLayout:
        id: box
		orientation: 'horizontal'
		size_hint: 1, 1
		spacing: 5
        size: root.size
        padding: 10, 0
		            
		Image:
            id: logo
			source: root.chemin_image
            #texture: root.texture
			size_hint: None, 1
            size: 40, 40 #self.texture_size
            #size: self.texture_size if root.taille_image[0] == None else root.taille_image
            center_y: root.center_y
            opacity: 0.2 if root.disabled else 1
			
		Label:
            id: ctrl_label
            markup: True
            font_size: 12
			text: root.texte
            valign: 'middle'
            size: self.texture_size
			size_hint: None, 1
            
        
""")



class BoutonTransparent(Button):
    chemin_image = StringProperty()
    animationEnCours = BooleanProperty() 
    def __init__(self, *args, **kwargs):
        super(BoutonTransparent, self).__init__(*args, **kwargs)		
        self.animationEnCours = False

    def Animer(self):
        """ Animation de la case """
        if self.animationEnCours == False :
            self.animationEnCours = True
            x, y = copy.copy(self.pos)
            largeur, hauteur = copy.copy(self.size)
            anim = Animation(pos=(x, y-5), t='in_out_back', duration=0.1)
            anim += Animation(pos=(x, y), animationEnCours=False, t='in_out_elastic', duration=0)
            anim.start(self)

            
            
class Attente(AnchorLayout):
    angle = NumericProperty()
    def __init__(self, *args, **kwargs):
        super(Attente, self).__init__(*args, **kwargs)		

class BoutonAvecImageEtroit(Button):
    texte = StringProperty()
    chemin_image = StringProperty()
    def __init__(self, *args, **kwargs):
        super(BoutonAvecImageEtroit, self).__init__(*args, **kwargs)		

        
class BoutonAvecImageLarge(Button):
    texte = StringProperty()
    chemin_image = StringProperty()
    taille_image = ListProperty()
    def __init__(self, *args, **kwargs):
        super(BoutonAvecImageLarge, self).__init__(*args, **kwargs)	
        
class BoutonAvecImageLarge_fond_normal(Button):
    texte = StringProperty()
    chemin_image = StringProperty()
    taille_image = ListProperty()
    def __init__(self, *args, **kwargs):
        super(BoutonAvecImageLarge_fond_normal, self).__init__(*args, **kwargs)	
        
class BoutonFichier(Button):
    texte = StringProperty()
    ctrl_logo = ObjectProperty()
    chemin_image = StringProperty()
    taille_image = ListProperty()
    def __init__(self, *args, **kwargs):
        super(BoutonFichier, self).__init__(*args, **kwargs)	
        
        
        
class MyApp(App):
    def build(self):
        # Génération du popup      
        box = BoxLayout(orientation="vertical")
        
        test = BoutonTransparent(chemin_image='images/horloge.png')
        box.add_widget(test) 
        
        test = BoutonAvecImageEtroit(texte="bouton 1", chemin_image='images/horloge.png')
        box.add_widget(test) 
        
        test = BoutonAvecImageLarge(texte="bouton 2\ntest", chemin_image='images/horloge.png')
        #test.disabled = True
        box.add_widget(test) 

        test = BoutonAvecImageLarge_fond_normal(texte="bouton 2 eci est", chemin_image='images/horloge.png')
        box.add_widget(test) 
        
        test = BoutonFichier(texte="Fichier Exemple\n[color=ff3333]Aucun fichier[/color]", taille_image=(None, None), chemin_image='images/horloge.png')
        box.add_widget(test) 

        #test = Attente()
        return box
        
        
if __name__ == '__main__':
    MyApp().run()