# Inspiration for first server draft. https://www.youtube.com/watch?v=_whymdfq-R4&list=PLzMcBGfZo4-kR7Rh-7JCVDN8lm3Utumvq&index=3&ab_channel=TechWithTim
import socket
from _thread import *

server = "" #indsæt IPv4 adresse
port = 5555


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Vælger at den skal forbinde med IPv4

try:
    s.bind( (server, port) )
except socket.error as e:
    print(e)

s.listen(2) #Mængden af clients der kan connecte
print("Waiting for a connection, server is ready...")


def threaded_client(conn):

    reply = ""
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode("utf-8")

            if not data:
                print("Disconnected")
                break
            else:
                print("Received:", reply)
                print("Sending:", reply)

            conn.sendall(str.encode(reply))
        except:
            break



while True:
    conn, addr = s.accept() #Acceptere alle indgående connection anmodninger
    print("Got connection from", addr) #Giver besked om at connection er modtaget og hvor den er fra.

    start_new_thread(threaded_client, (conn,))