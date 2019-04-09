from socket import socket, AF_INET, SOCK_STREAM

HOST = 'localhost'
PORT = 12345

with socket(AF_INET, SOCK_STREAM) as cliente:
  cliente.connect((HOST, PORT))
  cliente.sendall(b"Hello, world")
  data = cliente.recv(1024)

print('Recebido', repr(data))