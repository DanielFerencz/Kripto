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

    first_address = ("localhost", PORT)
    sock.connect(first_address)

    try:
        data = json.loads(sock.recv(SIZE).decode())

        if "status" not in data or data["status"] != "init":
                print("Problem sending to first. Ignore connection attempt.")
                raise CustomException(json.dumps({
                    "msg": "error"
                }))
        
        sock.sendall(json.dumps({"status": "OK"}).encode())
    
    except Exception:
        print("Problem receiving from first.")

    
    try:

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
        sock.close()

if __name__ == "__main__":
    main()