import socket
import json

PORT = 9000
SIZE = 512

class CustomException(Exception):
    pass

def main():

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    first_address = ('localhost', PORT)
    print ( 'starting up on %s port %s' % first_address)
    sock.bind(first_address)

    # Listen for incoming connections

    sock.listen(1)
    
    registrations = []

    while True:
        print ( 'waiting for a connection')
        connection, address = sock.accept()
        print ('connection from', address)
        try:
            connection.sendall(json.dumps({
                    "status": "init",
                }).encode())
            
            data = json.loads(connection.recv(SIZE).decode())
            if "status" not in data or data["status"] != "OK":
                print("Problem sending to client. Ignore connection attempt.")
                continue

            if "command" not in data:
                print("No command to execute")
                raise Exception()

            if data["command"] == "register":
                for (id, key) in registrations:
                    if id == data["clientId"]:
                        registrations.remove((id, key))
                
                print("Register with id: {} and publicKey: {}".format(data["clientId"], data["publicKey"]))
                registrations.append((data["clientId"], data["publicKey"]))
                connection.sendall(json.dumps({
                    "status": "OK",
                }).encode())

            if data["command"] == "getKey":
                for (id, key) in registrations:
                    if id == data["clientId"]:
                        publicKey = key
                print("Get key with id: {} and publicKey: {}".format(data["clientId"], publicKey))
                connection.sendall(json.dumps({
                    "publicKey": publicKey,
                }).encode())

        except Exception:
            print("Problem sending to client. Ignore connection attempt.")
        finally:
            # Clean up the connection
            connection.close()

if __name__ == "__main__":
    main()
