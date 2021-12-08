import socket
import json
import random
from packages.service.stream_cryptor import StreamCryptor
import packages.generator.merkle_hellman_knapsack as merkle_hellman
from packages.generator.solitaire import Solitaire

SERVER_PORT = 9000
PORT = 10000
SIZE = 2048
CLIENT_ID1 = 1
CLIENT_ID2 = 2

class CustomException(Exception):
    pass

def registerPubKey(clientId, public_key):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ("localhost", SERVER_PORT)
    sock.connect(server_address)

    try:
        data = json.loads(sock.recv(SIZE).decode())

        if "status" not in data or data["status"] != "init":
                print("Problem sending to first. Ignore connection attempt.")
                raise CustomException(json.dumps({
                    "msg": "error"
                }))
        
        sock.sendall(json.dumps(
            {
                "status": "OK",
                "command": "register",
                "clientId": clientId,
                "publicKey": public_key
            }).encode())
    
    except Exception:
        print("Problem receiving from first.")
    finally:
        # Clean up the connection
        sock.close()

def getPubKey(clientId):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ("localhost", SERVER_PORT)
    sock.connect(server_address)

    try:
        data = json.loads(sock.recv(SIZE).decode())

        if "status" not in data or data["status"] != "init":
                print("Problem sending to first. Ignore connection attempt.")
                raise CustomException(json.dumps({
                    "msg": "error"
                }))
        
        sock.sendall(json.dumps(
            {
                "status": "OK",
                "command": "getKey",
                "clientId": clientId,
            }).encode())

        data = json.loads(sock.recv(SIZE).decode())

        return data["publicKey"]
    
    except Exception:
        print("Problem receiving from first.")
    finally:
        # Clean up the connection
        sock.close()

def sendHello(private_key, client_public_key):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    first_address = ("localhost", PORT)
    sock.connect(first_address)

    try:
        
        sock.sendall(json.dumps({
            "clientId": merkle_hellman.encrypt_mh(str(CLIENT_ID1), client_public_key)
        }).encode())

        data = json.loads(sock.recv(SIZE).decode())
    
        if "clientId" not in data:
            print("Problem loading from peer.")
            raise CustomException(json.dumps({
                "msg": "error"
            }))

        clientId2 = int(merkle_hellman.decrypt_mh(data["clientId"], private_key))

        if (CLIENT_ID2 != clientId2):
            raise CustomException(json.dumps({
                "msg": "error"
            }))
    
    except Exception:
        print("Problem receiving from first.")

    return sock

def generateHalfDeck():
    
    halfDeck = []
    
    while (len(halfDeck) < 27):
        num = str(random.randint(1,54))
        if (num not in halfDeck):
            halfDeck.append(num)

    return " ".join(halfDeck)


def sendHalfSecret(sock, private_key, client_public_key):

    halfDeck = generateHalfDeck()

    try:
        
        sock.sendall(json.dumps({
            "halfKey": merkle_hellman.encrypt_mh(halfDeck, client_public_key)
        }).encode())

        data = json.loads(sock.recv(SIZE).decode())
    
        if "halfKey" not in data:
            print("Problem loading from peer.")
            raise CustomException(json.dumps({
                "msg": "error"
            }))

        otherHalfDeck = merkle_hellman.decrypt_mh(data["halfKey"], private_key)

        deck = halfDeck  + " " + otherHalfDeck

        return deck
    
    except Exception:
        print("Problem receiving from first.")

def convertToKey(deck):
    return [int(i) for i in deck.split(" ")]

def startMessaging(sock, deck):

    key = convertToKey(deck)

    streamCryptor = StreamCryptor(Solitaire, key)
    try:
        plainText = input("Please enter some text: \n")

        while plainText != "":
            
            byText = bytes(plainText,'ascii')

            offset = streamCryptor.getOffset()

            cipherText = streamCryptor.encryptText(byText)

            print("Sending cipherText: ", cipherText)

            sock.sendall(json.dumps({
                "offset": offset,
                "cipherText": [byt for byt in cipherText],
            }).encode())

            data = json.loads(sock.recv(SIZE).decode())
            if "cipherText" not in data or "offset" not in data:
                raise CustomException(json.dumps({
                    "msg": "error"
                }))

            offset = data["offset"]
            cipherText = bytes(data["cipherText"])

            print("Recieved cipherText: {}\nWith offset: {}".format(cipherText, offset))

            if (streamCryptor.getOffset() != offset):
                plainText = streamCryptor.decryptTextOffset(cipherText,offset)
            else:
                plainText = streamCryptor.decryptText(cipherText)

            print("Text after decryption: ", plainText)

            plainText = input("Please enter some text: \n")

    finally:
        # Clean up the connection
        sock.close()

def main():

    private_key, public_key = merkle_hellman.generate_key_pair()

    registerPubKey(CLIENT_ID1,public_key)

    input("---- Press Enter to get the public key of CLIENT 2 ----")

    client_public_key = getPubKey(CLIENT_ID2)

    sock = sendHello(private_key, client_public_key)

    deck = sendHalfSecret(sock, private_key, client_public_key)

    startMessaging(sock, deck)

if __name__ == "__main__":
    main()
