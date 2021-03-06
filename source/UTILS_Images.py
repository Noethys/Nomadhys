# -*- coding: utf-8 -*-
#!/usr/bin/env python

##############################################################
# Application :    Nomadhys, application nomade pour Noethys #
# Site internet :  www.noethys.com                           #
# Auteur:          Ivan LUCAS                                #
# Copyright:       (c) 2010-15 Ivan LUCAS                    #
# Licence:         Licence GNU GPL                           #
##############################################################

from kivy.logger import Logger
from kivy.uix.image import Image, CoreImage
from kivy.core.image import ImageData
from kivy.graphics.texture import Texture
import os
import six
    

# def TextureFromPyImage(pyImg):
#     try :
#         raw = pyImg.tostring()
#     except:
#         raw = pyImg.tobytes()
#     width, height = pyImg.size
#     imdata = ImageData(width, height, 'rgb', raw)
#     texture = Texture.create_from_data(imdata)
#     texture.flip_vertical()
#     return texture

# def ResizePyImage(pyImg, largeur, hauteur):
#     pyImg.thumbnail((largeur, hauteur), PyImage.ANTIALIAS)
#     return pyImg

# def GetBorderPyImage(pyImg):
#     draw = PyImageDraw.Draw(pyImg)
#     #draw.rectangle([(20,20), tuple([v - 20 for v in pyImg.size])], outline='green')
#     draw.rectangle([(0,0), tuple([v - 1 for v in pyImg.size])], outline='black')
#     del draw
#     return pyImg

# def GetPyImageFromStr(str):
#     return PyImage.open(six.BytesIO(str))

def GetTextureFromBuffer(buffer, avecBord=False):
    # Version avec PIL
    # pyImg = GetPyImageFromStr(buffer)
    # if avecBord == True :
    #     pyImg = GetBorderPyImage(pyImg)
    # texture = TextureFromPyImage(pyImg)
    # return texture

    # Version sans PIL
    data = six.BytesIO(buffer)
    texture = CoreImage(data, ext="png").texture
    return texture

def GetTextureFromFichier(nomFichier):
    texture = Image(source=nomFichier).texture
    return texture
    
    

def ConvertirToutesImagesPNG():
    """ Convertit toutes les images PNG du repertoire Noethys """
    from PIL import Image as PyImage

    racine = "C:/Users/Ivan/Documents/GitHub/Nomadhys/source/images"
    # Recherche les PNG présents
    tree = os.walk(racine)
    listeFichiersPNG = []
    for repertoire, listeRepertoires, listeFichiers in tree :
        for fichier in listeFichiers :
            if fichier.endswith(".png") :
                listeFichiersPNG.append(repertoire.replace("\\", "/") + "/" + fichier)
    print("Nbre fichiers PNG trouvees :", len(listeFichiersPNG))
    # Convertit les PNG
    nbreConversions = 0
    for fichier in listeFichiersPNG :
        # Ouverture de l'image
        image = PyImage.open(fichier)
        image.load() 
        profile = image.info.get("icc_profile")
        if profile != None :
            # Cree une image sans icc_profile
            nouvelleImage = PyImage.new("RGBA", image.size)
            nouvelleImage.paste(image) 
            
            # Supprime l'image ancienne
            os.remove(fichier)
            
            # Sauvegarde la nouvelle image
            nouveauFichier = fichier
            nouvelleImage.save(nouveauFichier, format="png")
            nbreConversions += 1

    print("%d images PNG ont ete converties" % nbreConversions)

    
    
    
    
if __name__ == '__main__':
    ConvertirToutesImagesPNG()
