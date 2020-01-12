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

try :
	from Crypto.Cipher import AES
	from Crypto import Random
	IMPORT_AES = True
except:
	Logger.warning('Application: Crypto.Cipher.AES non disponible')
	IMPORT_AES = False

import hashlib
import pickle
import base64
import six


class CypherText:
	def __init__(self):
		self.__CypherText = ''
		self.__trailLen = 0

	def getCypherText(self):
		return self.__CypherText

	def setCypherText(self, CText):
		self.__CypherText = CText

	def setTrail(self, TLen):
		self.__trailLen = TLen

	def getTrail(self):
		return self.__trailLen


def hashPassword_MD5(Password):
	m = hashlib.md5()
	if six.PY3:
		Password = str(Password).encode('utf-8')
	m.update(Password)
	return m.hexdigest()


def encrypt(message, key):
	TrailLen = 0
	while (len(message) % 16) != 0:
		message = message + '_'
		# if six.PY2:
		# 	message  = message + '_'
		# else :
		# 	message = message + b'_'
		TrailLen = TrailLen + 1

	CypherOut = CypherText()
	CypherOut.setTrail(TrailLen)

	cryptu = AES.new(key, AES.MODE_ECB)

	# Try to delete the key from memory
	key = hashPassword_MD5('PYCRYPT_ERASE_')

	CypherOut.setCypherText(cryptu.encrypt(message))
	return CypherOut


def decrypt(ciphertext, key):
	if six.PY3 and not isinstance(key, bytes):
		key = key.encode("utf8")
	cryptu = AES.new(key, AES.MODE_ECB)

	# Try to delete the key from memory
	key = hashPassword_MD5('PYCRYPT_ERASE_')

	message_n_trail = cryptu.decrypt(ciphertext.getCypherText())
	return message_n_trail[0:len(message_n_trail) - ciphertext.getTrail()]


def cryptFile(filename_in, filename_out, key):
	fr = open(filename_in, 'rb')
	fileContent = fr.read()
	cyphertext = encrypt(fileContent, key)
	fw = open(filename_out, 'wb')
	pickle.dump(cyphertext, fw, -1)


# --------------------------------------------------------------------------
# 2ème version qui évite l'utilisation de Pickle pour une compatibilité py3
# --------------------------------------------------------------------------

def pad(s):
	padding_size = AES.block_size - len(s) % AES.block_size
	return s + b"\0" * padding_size, padding_size

def encrypt2(message, key, key_size=256):
	message, padding_size = pad(message)
	iv = Random.new().read(AES.block_size)
	cipher = AES.new(key, AES.MODE_CFB, iv)
	enc_bytes = iv + cipher.encrypt(message)
	if six.PY2:
		enc_bytes += bytearray([padding_size])
	else:
		enc_bytes += bytes([padding_size])
	return enc_bytes

def decrypt2(ciphertext, key):
	iv = ciphertext[:AES.block_size]
	cipher = AES.new(key, AES.MODE_CFB, iv)
	plaintext = cipher.decrypt(ciphertext[AES.block_size:-1])
	if six.PY2:
		ciphertext = bytearray(ciphertext)
	padding_size = ciphertext[-1] * (-1)
	return plaintext[:padding_size]

def cryptFile2(filename_in, filename_out, key):
	if six.PY3:
		key = key.encode("utf8")
	with open(filename_in, 'rb') as fo:
		contenu = fo.read()
	enc = encrypt2(contenu, key)
	enc = b"SV2" + enc
	with open(filename_out, 'wb') as fo:
		fo.write(enc)


def DecrypterFichier(fichierCrypte="", fichierDecrypte="", motdepasse=""):
	# Formatage du mot de passe
	motdepasse = hashPassword_MD5(motdepasse)
	if six.PY3:
		motdepasse = motdepasse.encode("utf8")

	# Lecture du fichier
	with open(fichierCrypte, 'rb') as fo:
		contenu = fo.read()

	# Analyse du fichier
	if contenu[:3] == b"SV2":
		# Nouvelle version
		contenu = contenu[3:]
		dec = decrypt2(contenu, motdepasse)
	else:
		# Ancienne version
		with open(fichierCrypte, 'rb') as fo:
			if six.PY2:
				contenu2 = pickle.load(fo)
			else:
				contenu2 = pickle.load(fo, encoding="bytes")
			dec = decrypt(contenu2, motdepasse)

	# Enregistrement du fichier décrypté
	with open(fichierDecrypte, 'wb') as fr:
		fr.write(dec)


def CrypterFichier(fichierDecrypte="", fichierCrypte="", motdepasse="", ancienne_methode=False):
	if not ancienne_methode or six.PY3:
		fonction = cryptFile2
	else:
		fonction = cryptFile
	fonction(fichierDecrypte, fichierCrypte, hashPassword_MD5(motdepasse))


if (__name__ == '__main__'):
	pass