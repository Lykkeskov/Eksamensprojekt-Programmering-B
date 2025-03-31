import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 8080))

print(client.recv(1024).decode('utf-8'))
client.send('Welcome to Eksamensprojekt!'.encode('utf-8'))

