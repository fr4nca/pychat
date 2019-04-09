from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

HOST = '127.0.0.1'
PORT = 11234

cliente = socket(AF_INET, SOCK_STREAM)
cliente.connect((HOST, PORT))


def receive():
while True:
try:    
    msg = cliente.recv(1024).decode("utf8")
    print(msg)
except OSError:
    break


def send():
    while True:
        msg = input()
        cliente.send(bytes(msg, "utf8"))
        if msg == "Exit":
            cliente.close()


msg = input("Digite seu nome: ")
cliente.send(bytes(msg, "utf8"))

if __name__ == "__main__":
    Thread(target=receive).start()
    send()
