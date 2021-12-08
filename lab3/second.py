import socket
import json
import random
from packages.generator.solitaire import Solitaire
from packages.service.stream_cryptor import StreamCryptor
import packages.generator.merkle_hellman_knapsack as merkle_hellman

SERVER_PORT = 9000
PORT = 10000
SIZE = 2048
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

def waitHello(private_key):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = ('localhost', PORT)
    print ( 'starting up on %s port %s' % address)
    sock.bind(address)

    # Listen for incoming connections
    sock.listen(1)

    peer_connected = False
    connection = None
    client_public_key = None

    while not peer_connected:
        print ( 'waiting for a connection')
        connection, peer_address = sock.accept()
        print ('connection from', peer_address)
        try:

            data = json.loads(connection.recv(SIZE).decode())

            if "clientId" not in data:
                print("Problem loading msg.")
                raise CustomException(json.dumps({
                    "msg": "error"
                }))

            clientId1 = int(merkle_hellman.decrypt_mh(data["clientId"], private_key))

            client_public_key = getPubKey(clientId1)

            connection.sendall(json.dumps({
                    "clientId": merkle_hellman.encrypt_mh(str(CLIENT_ID2), client_public_key),
                }).encode())

            peer_connected = True
        except Exception:
            print("Problem sending to second. Ignore connection attempt.")

    return sock, connection, client_public_key

def generateOtherHalfDeck(halfDeck):

    halfdeckList = halfDeck.split(" ")

    otherHalfDeck = []

    print(halfdeckList)

    while(len(otherHalfDeck)<27):
        num = str(random.randint(1,54))
        if (num not in otherHalfDeck and num not in halfdeckList):
            otherHalfDeck.append(num)

    return " ".join(otherHalfDeck)

def waitHalfSecret(connection, client_public_key, private_key):
    try:

        data = json.loads(connection.recv(SIZE).decode())

        if "halfKey" not in data:
            print("Problem loading msg.")
            raise CustomException(json.dumps({
                "msg": "error"
            }))

        halfDeck = merkle_hellman.decrypt_mh(data["halfKey"], private_key)

        otherHalfDeck = generateOtherHalfDeck(halfDeck)

        connection.sendall(json.dumps({
                "halfKey": merkle_hellman.encrypt_mh(otherHalfDeck, client_public_key),
            }).encode())

        deck = halfDeck  + " " + otherHalfDeck

        return deck

    except Exception:
        print("Problem sending to second. Ignore connection attempt.")

def convertToKey(deck):
    return [int(i) for i in deck.split(" ")]

def startMessaging(sock, connection, deck):

    key = convertToKey(deck)
    
    streamCryptor = StreamCryptor(Solitaire, key)
    try:

        data = json.loads(connection.recv(SIZE).decode())
        print(data)
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

        while plainText != "":
            
            byText = bytes(plainText,'ascii')

            offset = streamCryptor.getOffset()

            cipherText = streamCryptor.encryptText(byText)

            print("Sending cipherText: ", cipherText)

            connection.sendall(json.dumps({
                "offset": offset,
                "cipherText": [byt for byt in cipherText],
            }).encode())

            data = json.loads(connection.recv(SIZE).decode())
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
        connection.close()
        sock.close()

def main():

    private_key, public_key = merkle_hellman.generate_key_pair()

    registerPubKey(CLIENT_ID2,public_key)

    sock, connection, client_public_key = waitHello(private_key)

    deck = waitHalfSecret(connection, client_public_key, private_key)

    print("---- The key ----")
    print(deck)
    print("-----------------")

    startMessaging(sock, connection, deck)
    

if __name__ == "__main__":
    main()
