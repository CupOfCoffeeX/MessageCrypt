from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from hashlib import md5

import socket
import threading
import RSA_Cipher
import AES_Cipher


class Client:
    def __init__(self, host, port, window, pseudo):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.window = window

        self.pseudo = pseudo

        # attributs liés au chiffrement RSA
        self.rsa = RSA_Cipher.RSAChiffrement()
        self.RsaPublicKey = None

        # attributs liés au chiffrement AES
        self.aes = AES_Cipher.AESChiffrement()
        self.AesKey = None


    def connect(self, targetHost, targetPort):
        #self.client.bind((self.host, self.port))
        try:
            # connection au serveur
            self.client.connect((targetHost, int(targetPort)))
            print(f'connected on {targetHost} : {targetPort}')

            # on envoi le pseudo
            self.client.send(self.pseudo.encode())

            # on récupère la clé publique RSA du serveur
            self.RsaPublicKey = self.client.recv(3072)
            print(self.RsaPublicKey)

            # on envoi la clé AES chiffré avec la clé publique RSA

            # génération de la clé sous forme de string
            self.AesKey = self.aes.generateKey(16)

            # set up la clé sous forme de hash
            self.aes.setKey(md5(self.AesKey.encode('utf8')).digest())


            self.client.send(self.rsa.chiffrement(self.AesKey, self.RsaPublicKey))
            print('aes key : ', self.AesKey)
        except socket.error as e:
            print(str(e))

        self.startClient()

    def startClient(self):
        # on effectue simultanément 2 tâches : - écoute et recois des infos du serveur
        #                                      - envoi des données saisient par le client

        t1 = threading.Thread(target=self.listener)
        t2 = threading.Thread(target=self.sender)

        # lancement des deux thread
        t2.start()
        t1.start()

    def listener(self):
        print('is listening')
        while True:
            rep = self.client.recv(2048)
            if self.aes.decrypt(rep).decode()[:9] == 'addfriend':
                self.window.addToFriendList(self.aes.decrypt(rep).decode()[9:])
            else:
                print('\n' + self.aes.decrypt(rep).decode())
                self.window.print_message(self.aes.decrypt(rep).decode())

    def sender(self):
        while True:
            Input = input('Client: ')
            self.client.send(self.aes.encrypt(Input))
            print(self.aes.encrypt(Input))
            if Input != '' and Input != ' ':
                self.window.print_message(self.pseudo + ": " + Input)
    def sendMessage(self, messaage):
        self.client.send(self.aes.encrypt(messaage))
        print(self.aes.encrypt(messaage))
        self.window.print_message(self.pseudo +": " + messaage)

"""client = Client('192.168.1.61', 6666)
client.connect('192.168.1.61', 6667)
client.startClient()"""





