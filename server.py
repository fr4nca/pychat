from socket import socket, SOCK_STREAM, AF_INET
from threading import Thread

HOST = '127.0.0.1'
PORT = 12345

clientes = {}
enderecos = {}

server = socket(AF_INET, SOCK_STREAM)
server.bind((HOST, PORT))


def iniciar():
    while True:
        cliente, endereco = server.accept()
        print('Conectado por ', endereco)
        enderecos[cliente] = endereco
        Thread(target=handle_client, args=(cliente,)).start()


def handle_client(cliente):
    nome = cliente.recv(1024).decode("utf8")
    bemvindoMsg = "Bem  vindo, %s. Para sair, digite 'Exit'." % nome
    cliente.send(bytes(bemvindoMsg, "utf8"))
    entrouMsg = "%s entrou no chat.." % nome
    sendToAll(entrouMsg)
    clientes[cliente] = nome
    while True:
        msg = cliente.recv(1024).decode("utf8")
        if msg != "Exit":
            sendToAll(nome + ": " + msg)
        else:
            cliente.send(bytes("Exit", "utf8"))
            cliente.close()
            del clientes[cliente]
            print("%s deixou o chat." % nome)
            sendToAll("%s deixou o chat." % nome)
            break


def sendToAll(msg):
    mensagem = bytes(msg, "utf8")
    for cliente in clientes:
        cliente.send(mensagem)


if __name__ == "__main__":
    server.listen()
    print("Esperando conexões")
    ACCEPT_THREAD = Thread(target=iniciar)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    server.close()
