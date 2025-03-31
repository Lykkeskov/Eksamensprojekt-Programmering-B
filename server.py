import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 8080))

server.listen(1)
u = 0

while True:
    u = u + 1
    client, addr = server.accept()
    client.send('Welcome to Eksamensprojekt!'.encode('utf-8'))
    print('Connected by', addr)
    print(client.recv(1024).decode('utf-8'))
    print(u)
