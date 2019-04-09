# Importações
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

# Constantes globais
# Endereço do servidor
HOST = '127.0.0.1'
PORT = 11234

try:
	# Inicializa o socket do cliente
	# AF_INET indica IPv4
	# SOCK_STREAM indica TCP
	cliente = socket(AF_INET, SOCK_STREAM)

	# Conecta o cliente ao servidor com o HOST e PORTA
	cliente.connect((HOST, PORT))
except:
	# Exceção caso não o servidor não esteja ligado, desliga o cliente
	print("Nenhum servidor ligado..")
	quit()

# Função de recepção de dados do servidor
def receive():
	# Loop eterno
	while True:
		try:
			# Buffer de recepção dos bytes decodificados do servidor
			msg = cliente.recv(1024).decode("utf8")
			# Escreve a mensagem na tela
			print(msg)
		except Exception:
			# Escreve o erro na tela
			print("Ocorreu algum erro" + Exception.__cause__)

# Função de envio de dados ao servidor
def send():
	# Loop eterno
	while True:
		try:
			# Buffer de leitura
			msg = input()
			# Envia os bytes codificados em UTF-8 
			cliente.send(bytes(msg, "utf8"))
		except Exception:
			# Escreve o erro na tela
			print("Ocorreu algum erro" + Exception.__cause__)

if __name__ == "__main__":
	# Inicia a Thread com a função receive()
	Thread(target=receive).start()
	# Inicia a função send()
	send()

