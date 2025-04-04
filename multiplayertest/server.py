import socket
from  _thread import *
import sys

server = "192.168.0.105"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server,port))
except socket.error as e:
    str(e)

#open port, max. 2 connections
s.listen(2)
print("Waiting for connection, Server started")

#runs in the background simultaniously to while loop that accepts new connections
def threaded_client(conn):
    conn.send(str.encode("Connected"))
    reply = ""
    while True:
        try:
            data = conn.recv(2048) # bitsize
            reply = data.decode("utf-8") # decode into human readable string

            if not data:
                print("Disconnected")
                break
            else:
                print("Received: ", reply)
                print("Sending: ", reply)

            conn.sendall(str.encode(reply)) # encode reply into byte object
        except:
            break
    
    print("Lost connection")
    conn.close()


while True:
    #addr is IP address
    conn, addr = s.accept()
    print("Connected to: ",addr)

    start_new_thread(threaded_client, (conn,))