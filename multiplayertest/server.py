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

def read_pos(str):
    str = str.split(",")   
    return int(str[0]) , int(str[1])

def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])

pos = [(0,0), (100,100)]

#runs in the background simultaniously to while loop that accepts new connections
def threaded_client(conn, player):
    conn.send(str.encode(make_pos(pos[player]))) # send starting position of the current player
    reply = ""
    while True:
        try:
            data = read_pos(conn.recv(2048).decode()) # bitsize = 2048, 
            #reply = data.decode("utf-8") # decode into human readable string
            pos[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = pos[0]
                else:
                    reply = pos[1]
                #print("Received: ", data)
                #print("Sending: ", reply)

            conn.sendall(str.encode(make_pos(reply))) # encode reply into byte object
        except:
            break
    
    print("Lost connection")
    conn.close()

currentPlayer = 0

# accepts new connections if available
while True:
    #addr is IP address
    conn, addr = s.accept()
    print("Connected to: ",addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1