# Importações
from socket import socket, SOCK_STREAM, AF_INET
from threading import Thread

# Constantes globais
# Endereço do servidor
HOST = '127.0.0.1'
PORT = 11234

# Dicionário para guardar os clientes
clientes = {}

# Inicializa o socket do servidor
# AF_INET indica IPv4
# SOCK_STREAM indica TCP
server = socket(AF_INET, SOCK_STREAM)
# Atribui o endereço ao servidor
server.bind((HOST, PORT))

# Função para iniciar a Thread e o escutar as conexões ao servidor
def iniciar():
	# Loop eterno
	while True:
		# Escuta conexões
		cliente, endereco = server.accept()
		# Inicia a thread com a função handle_client()
		Thread(target=handle_client, args=(cliente,)).start()

# Função para lidar com os clientes
def handle_client(cliente):
	# Função para "cadastrar" o cliente
	assign_client(cliente)

	# Loop eterno
	while True:
		# Recebe o nome do cliente guardado no dicionário 
		nome = clientes[cliente]
		# Recebe os bytes decodados do cliente
		msg = cliente.recv(1024).decode("utf8")

		if msg != "Exit":
			# Divide a mensagem em uma lista no : para identificar o tipo dela
			tipo_mensagem = msg.split(": ", 1)

			# Se a lista for menor que 2, não foi indicado um tipo
			if len(tipo_mensagem) >= 2:
				# Divide tipo e mensagem em variáveis diferentes
				tipo = tipo_mensagem[0]
				mensagem = tipo_mensagem[1]

				if tipo == "MSG":
					# Envia mensagem para todos
					send_to_all(nome + ": " + mensagem)

				elif tipo == "PRIVATE":
					# Divide a mensagem em receptor e mensagem no :
					receptor_mensagem = mensagem.split(": ", 1)
					receptor = receptor_mensagem[0]
					mensagem = bytes(nome + ": " + receptor_mensagem[1], "utf8")

					# Função para enviar mensagem privada
					# Se a função retornar falso, não existe cliente com o nome indicado
					if not send_to_one(receptor, mensagem):
						# Retorna mensagem para o cliente
						cliente.send(bytes("Nenhum cliente com este nome.", "utf8"))

				elif tipo == "NICK":
					# Função para troca de nick
					change_nick(mensagem, cliente)
				
				# Tipo de mensagem inválido
				else:
					cliente.send(bytes("Tipo de mensagem inexistente", "utf8"))

			# Nenhum tipo indicado
			else:
				cliente.send(bytes("A mensagem precisa ter um tipo (MSG, PRIVATE, NICK, SNDFILE ou RECFILE", "utf8"))

		# Caso mensagem for "Exit"
		else:
			# Fecha conexão do clietne
			cliente.close()
			# Deleta do dicionário
			del clientes[cliente]
			print("%s deixou o chat." % nome)
			send_to_all("%s deixou o chat." % nome)
			break

# Função para "cadastrar" cliente
def assign_client(cliente):
	# Recebe o nick do cliente
	cliente.send(bytes("Digite seu nick: ", "utf8"))
	nome = cliente.recv(1024).decode("utf8")

	# Função que verifica se o nome ja foi cadastrado
	# Se retornar false, o nome ja foi cadastado
	if verify_name(nome):
		# Mensagens de boas vindas
		print("%s se conectou.." % nome)
		bemVindoMsg = "Bem  vindo, %s. Para sair, digite 'Exit'." % nome
		cliente.send(bytes(bemVindoMsg, "utf8"))

		# Envia mensagem de login para todos
		entrouMsg = "%s entrou no chat.." % nome
		send_to_all(entrouMsg)

		# Adiciona cliente ao dicionário
		clientes[cliente] = nome

	# Ja existe usuário com este nome
	else:
		# Mensagem de erro
		cliente.send(bytes("Ja existe um usuário com este nome. Por favor tente novamente com outro nome", "utf8"))
		# Recursivamente pede o nick novamente
		handle_client(cliente)

# Função para verificar se o nome ja foi cadastrado
# Retorna true se não estiver cadastrado
# Retorna false se ja estiver cadastrado
def verify_name(nome):
	# Loop nos clientes e verifica
	for name in clientes.values():
		if name == nome:
			return False
	return True

# Função para enviar mensagens para todos
def send_to_all(msg):
	mensagem = bytes(msg, "utf8")

	# Loop nos clientes e envia
	for cliente in clientes:
		cliente.send(mensagem)

# Função para enviar mensagem para um
# Retorna true se a existe receptor
# Retorna false se não existe receptor
def send_to_one(receptor, msg):
	# Loop nos clientes, verifica o receptor e envia
	for cliente in clientes:
		if clientes[cliente] == receptor:
			cliente.send(msg)
			return True			
	return False

# Função para trocar nick
def change_nick(nome, cliente):
	# Verifica se nome ja foi cadastrado
	if verify_name(nome):
		clientes[cliente] = nome
		cliente.send(bytes("Nick mudado com sucesso.", "utf8"))

	# Mensagem de erro caso nick ja estiver sendo utilizado
	else:
		cliente.send(bytes("NICKERR: Este nick ja esta sendo utilizado", "utf8"))

if __name__ == "__main__":
	# Escuta as conexões
	server.listen()
	print("Servidor iniciado na porta %s" % PORT)
	# Inica a thread
	ACCEPT_THREAD = Thread(target=iniciar)
	ACCEPT_THREAD.start()
	ACCEPT_THREAD.join()
	# Fecha o servidor
	server.close()
