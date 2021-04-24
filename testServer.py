from hashlib import md5

import socket
import threading
import time
# notre programme de chiffrement rsa
import RSA_CryptoChat
import AES_GitHub

class Server:
    """classe concernant la fenêtre de chat, socket, réseau"""
    def __init__(self, host, port, window):
        # attributs du serveur
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.window = window

        # attributs du client
        self.client = None
        self.clientList = {} # liste des clients
        self.compteurClientList = 0
        self.adresseList = [] # liste des adresses ip + ports
        self.clientNumber = 0
        self.currentClientListener = 0
        self.currentClientSender = 0

        self.pseudo = None
        self.pseudoList = {}
        self.compteurPseudoList = 0

        # attributs liés au chiffrement RSA
        self.rsa = RSA_CryptoChat.RSAChiffrement()
        self.publicKeyRSA, self.privateKeyRSA = self.rsa.generateKeys()


        # attributs liés au chiffrement AES
        self.aes = AES_GitHub.AESChiffrement()
        self.AesKey = {}
        self.compteurAesKey = 0

        # debug
        self.window.lineEdit.setPlaceholderText('test test test zebi')

        print(self.publicKeyRSA.decode('ascii'))
        print(self.privateKeyRSA.decode('ascii'))
        print('[~] Server is ready ! [~]')


    def startServer(self):
        # bind du serveur sur le bon port de la machine
        self.server.bind((self.host, int(self.port)))
        serverThread = threading.Thread(target=self.serverSender)
        serverThread.start()
        # debug #
        print(socket.gethostbyname(socket.gethostname()))
        print("Le programme est a l'ecoute d'une eventuelle discussion")
        # se prepare à recevoir des connexions clients
        self.server.listen(5)  # ecoute...

        while True:
            continuer = True
            self.client, self.adresse = self.server.accept()  # accepte...
            self.clientList[self.compteurClientList] = self.client

            # on récupère les pseudos
            self.pseudo = self.client.recv(2048)
            self.pseudoList[self.compteurPseudoList] = self.pseudo.decode()

            print(self.pseudoList)

            # on ajoute à la liste des pseudos
            self.window.addToFriendList(self.pseudo.decode())
            # on envoi la clé publique RSA au nouveau client
            time.sleep(1.0)
            self.client.send(self.publicKeyRSA)

            # test si le client envoi bien la clé ou s'il se déconnecte
            # protection anti DDoS car si un client n'envoi pas de pseudo il est directement retiré
            try:
                # réception de la clé AES chiffrée
                cipherKey = self.client.recv(2048)
            except ConnectionAbortedError:
                print('aborted')
                continuer = False
                self.clientList[self.clientNumber] = 0
                self.pseudoList[self.clientNumber] = 0

                print(self.clientList)
                print(self.pseudoList)
            # si le client est bien connecté et que la clé à été reçu
            if continuer:
                key = self.rsa.dechiffrement(cipherKey, self.privateKeyRSA).decode()
                self.AesKey[self.compteurAesKey] = key
                self.compteurAesKey += 1
                #self.AesKey.append(key)
                print('aes key : ', self.AesKey)

                # on créé un thread pour le nouveau client qui vient de se connecter au serveur
                clientThread = threading.Thread(target=self.clientThread, args=(self.clientNumber,))
                clientThread.start()
                print('client thread created')

                # on ajoute le client à la liste des clients
                self.adresseList.append(self.adresse)
                # affichage de l'ip/port du client
                print(f'{self.adresse} is connected on port')

                # on met à jour les indices
                self.clientNumber += 1
                print('nombre de clients : ', self.clientNumber)

            self.sendMessageAll("addfriend" + self.pseudo.decode())
            self.compteurPseudoList += 1
            self.compteurClientList += 1



    def serverSender(self):
        time.sleep(1.0)
        while True:
            send = input('Server: ')
            self.sendMessageAll(send)

    def sendMessageAll(self, send):

        if send == 'exit':
            self.server.close()
        else:
            for client in self.clientList.values():
                currentKey = self.AesKey[self.currentClientSender]
                #self.AesKey[self.currentClientSender]
                self.aes.setKey(md5(currentKey.encode('utf8')).digest())
                print(self.AesKey[self.currentClientSender] + "-->" + self.pseudoList[self.currentClientSender])
                client.send(self.aes.encrypt(send))

                self.currentClientSender += 1
            self.currentClientSender = 0

    def clientThread(self, clientIndice):
        print('client thread started...')
        print("clientIndice", clientIndice)
        self.continuer = True
        while self.continuer:
            try:
                # réception du message
                print('\n\n')
                print(self.clientList)
                print(clientIndice)
                print(self.clientList[clientIndice])
                print("a l'ecouteeeeee")
                cipherMessage = self.clientList[clientIndice].recv(2048)
                print("cipherMessage : ", cipherMessage)
                print('clientIndice : ', clientIndice)
                print(self.pseudoList[clientIndice])
                print(str(self.AesKey[clientIndice]))
                print(str(self.AesKey[clientIndice]) + "-->" + self.pseudoList[clientIndice])
                # décodage et set up de la clé du bon client
                print(md5(self.AesKey[clientIndice].encode('utf8')).digest())
                self.aes.setKey(md5(self.AesKey[clientIndice].encode('utf8')).digest()) #self.AesKey[clientIndice]
                message = self.aes.decrypt(cipherMessage)
                print(message)
                if message == 0:
                    self.deleteInformations(clientIndice)
                    break

                if message.decode() != '' and message.decode() != ' ':
                    print("passage")
                    self.window.print_message(self.pseudoList[clientIndice] +": " + message.decode())

                    self.currentClientListener = clientIndice

                    for i in self.clientList:
                        if i != self.currentClientListener and self.clientList[i] != 0:
                            self.aes.setKey(md5(str(self.AesKey[i]).encode('utf8')).digest())
                            self.clientList[i].send(self.aes.encrypt(self.pseudoList[self.currentClientListener] + ": " + message.decode()))

            except ConnectionResetError:
                self.deleteInformations(clientIndice)
        print('thread is dead ',clientIndice )

    def deleteInformations(self, clientIndice):
        # Si le client se déconnecte alors on supprime toute les traces
        print(f"\nLe client {self.pseudoList[clientIndice]} s'est déconnecté")
        self.continuer = False
        self.clientList[clientIndice].close()

        # on supprime le pseudo de l'interface graphique
        print('pseudo a supprimer : ', self.pseudoList[clientIndice])
        self.window.deleteFriend(self.pseudoList[clientIndice])

        self.clientList[clientIndice] = 0
        self.AesKey[clientIndice] = 0
        self.pseudoList[clientIndice] = 0
        #del self.adresseList[clientIndice]
        #self.clientNumber -= 1

        print(self.clientList)
        print(self.AesKey)
        print(self.pseudoList)
        print(self.adresseList)

        print('données supprimées')

"""serv = Server('192.168.1.61', 6667)
serv.startServer()"""