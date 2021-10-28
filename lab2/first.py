import socket
import json
from packages.utils.config import Config
from packages.service.stream_cryptor import StreamCryptor

PORT = 10000
SIZE = 512

class CustomException(Exception):
    pass

def main():

    config = Config()

    streamCryptor = StreamCryptor(config.getGenerator(), config.getKey())

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    first_address = ('localhost', PORT)
    print ( 'starting up on %s port %s' % first_address)
    sock.bind(first_address)

    # Listen for incoming connections
    sock.listen(1)

    second_connected = False
    second_connection = None

    while not second_connected:
        print ( 'waiting for a connection')
        connection, secont_address = sock.accept()
        second_connection = connection
        print ('connection from', secont_address)
        try:
            connection.sendall(json.dumps({
                    "status": "init",
                }).encode())
            
            data = json.loads(connection.recv(SIZE).decode())
            if "status" not in data or data["status"] != "OK":
                print("Problem sending to second. Ignore connection attempt.")
                continue

            second_connected = True
        except Exception:
            print("Problem sending to second. Ignore connection attempt.")

    try:
        plainText = input("Please enter some text: \n")

        while plainText != "":
            
            byText = bytes(plainText,'ascii')

            offset = streamCryptor.getOffset()

            cipherText = streamCryptor.encryptText(byText)

            print("Sending cipherText: ", cipherText)

            second_connection.sendall(json.dumps({
                "offset": offset,
                "cipherText": [byt for byt in cipherText],
            }).encode())

            data = json.loads(second_connection.recv(SIZE).decode())
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
        second_connection.close()
        sock.close()

if __name__ == "__main__":
    main()