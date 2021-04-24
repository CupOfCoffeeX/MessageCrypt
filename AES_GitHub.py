from hashlib import md5
from base64 import b64decode
from base64 import b64encode

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

from RSA_CryptoChat import RSAChiffrement

import random

class AESChiffrement:
    def __init__(self):
        self.cleSauvegarde = self.generateKey(128)
        # hashage de la clé pour faire une clé AES
        self.cle = md5(self.cleSauvegarde.encode('utf8')).digest()

    def encrypt(self, data):
        iv = get_random_bytes(AES.block_size)
        self.chiffrement = AES.new(self.cle, AES.MODE_CBC, iv)
        return b64encode(iv + self.chiffrement.encrypt(pad(data.encode('utf-8'),
            AES.block_size)))

    def decrypt(self, data):
        brut = b64decode(data)
        try:
            self.dechiffrement = AES.new(self.cle, AES.MODE_CBC, brut[:AES.block_size])
        except:
            print(" [!!!] client has been disconnected ...")
            return 0

        return unpad(self.dechiffrement.decrypt(brut[AES.block_size:]), AES.block_size)

    def generateKey(self, length):
        caracteres = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
        key = ""

        for i in range(length):
            key = key + random.choice(caracteres)
        return key

    def getKey(self):
        return self.cleSauvegarde
    def setKey(self, key):
        self.cle = key






