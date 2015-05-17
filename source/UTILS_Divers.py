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

def GetRepData():
    a = App()
    rep = a.user_data_dir + "nomadhys/"
    del a
    return rep
    
    
    
if __name__ == "__main__":
    print GetRepData()