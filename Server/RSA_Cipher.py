from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii


class RSAChiffrement:
	def generateKeys(self):

		self.keyPair = RSA.generate(3072)

		# on récupère la clé privée
		privKeyPEM = self.keyPair.exportKey()
		#print(privKeyPEM.decode('ascii'))

		# on récupère la clé publique
		self.publique = self.keyPair.publickey()
		#print(f"Public key:  (n={hex(self.publique.n)}, e={hex(self.publique.e)})")
		pubKeyPEM = self.publique.exportKey()
		#print(pubKeyPEM.decode('ascii'))

		# Ecrit les clés dans un fichier PEM
		file_out = open('publicKeyRSA.pem', 'wb')
		file_out.write(self.publique.export_key('PEM'))
		file_out.close()

		file_out = open('privateKeyRSA.pem', 'wb')
		file_out.write(self.keyPair.export_key('PEM'))
		file_out.close()

		return pubKeyPEM, privKeyPEM

	def chiffrement(self, message, publicKey):
		encryptor = PKCS1_OAEP.new(RSA.importKey(publicKey))
		encrypted = encryptor.encrypt(message.encode())

		return encrypted

	def dechiffrement(self, messageChiffre, privateKey):
		decryptor = PKCS1_OAEP.new(RSA.importKey(privateKey))
		decrypted = decryptor.decrypt(messageChiffre)
		return decrypted

"""rsa = RSAChiffrement()
pub, priv = rsa.generateKeys()
print(pub)
print(priv)
messageChiffre = rsa.chiffrement('test', pub)
print("Encrypted:", binascii.hexlify(messageChiffre))

print(rsa.dechiffrement(messageChiffre, priv).decode())"""

