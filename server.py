from socket import socket, SOCK_STREAM, AF_INET

HOST = 'localhost'
PORT = 12345

with socket(AF_INET, SOCK_STREAM) as s:
  s.bind((HOST, PORT))
  s.listen()
  conn, addr = s.accept()
  with conn:
    print('Conectado por ', addr)
    while 1:
      data = conn.recv(1024)
      if not data:
        break
      conn.sendall(data)