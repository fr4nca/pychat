# Importações
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup

# Endereço do servidor
HOST = '127.0.0.1'
PORT = 12332

# Constantes globais
global cliente
global sm

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

# Carrega o arquivo Kvlang
Builder.load_file('pychat.kv')


# Classe Chat que faz referência a classe <Chat> do arquivo .kv
class Chat(Screen):
    global sm

    def __init__(self, **kwargs):
        super(Chat, self).__init__(**kwargs)

    # Função que gera um widget Pop Up 
    # Recebe: (String) Título do Pop Up, (String) Mensagem do corpo do Pop Up, (String) Mensagem do Botão do Pop Up
    def pop_up(self, titlepop, mensagem, msgbotao):
        self.layout = GridLayout(cols=1)
        self.popuplb= Label(text=mensagem)
        self.popupbt= Button(text=msgbotao)
        self.layout.add_widget(self.popuplb)
        self.layout.add_widget(self.popupbt)
        self.popup = Popup(title=titlepop, auto_dismiss=False,content=self.layout, size_hint=(.5, .3))
        self.popupbt.bind(on_press=self.popup.dismiss)
        self.popup.open()

    # Função de recepção de mensagens enviadas pelo servidor
    def receive(self):
        # Loop eterno
        while True:
            try:
                # Buffer de recepção dos bytes decodificados do servidor
                msg = cliente.recv(1024).decode("utf8")
                print(msg)

                # Verificação de nome já existente
                if msg == 'Ja existe um usuário com este nome. Por favor tente novamente com outro nome':
                    msg = 'Ja existe um usuário com este nome.\nPor favor tente novamente com outro nome'

                    # Chamado da função que gera um Pop Up
                    self.pop_up(self, 'Nome Inválido', msg,'Tudo bem')

                    # Volta para a tela Inicial para que o usuário digite um nome válido
                    sm.current='inicial'
                
                # Verificação de saída 
                elif msg == 'Saindo...': break
                else:

                    # Adiciona um widget Label para mostrar a mensagem na tela
                    sm.get_screen('chat').ids.box.add_widget(Label(text=msg, color=(0, 0, 0, 0), font_size=17, font_name='src/Roboto-Light.ttf'))
                
            except Exception as e:
                # Escreve o erro na tela
                print("Ocorreu algum erro", e)

    # Função de envio de dados ao servidor
    def send_msg(self, msg):
        try:
            # Verifica comando de saída "Exit"
            if msg == 'Exit':
                # Fecha a janela 
                Window.close() 
                # Envia os bytes codificados em UTF-8
                cliente.send(bytes(msg, 'utf8')) 
            
            # Envia os bytes codificados em UTF-8
            cliente.send(bytes(msg, 'utf8'))         

        except Exception as a:
            # Escreve o erro na tela
            print('Ocorreu algum erro', a)

    # Função que verifica mensagem vazia
    def verifica_msg(self, msg):
        # Caso a mensagem não for vazia, muda o estado do botão de enviar para ativado
        if not msg == 'MSG: ' or msg == 'PRIVATE: ' or msg == 'NICK ': 
            sm.get_screen('chat').ids.enviar.disabled = False

    # Função que determina o tipo de mensagem escolhida pelo usuário
    def spinner(self, spinner, text):
        if text == 'MSG':
            sm.get_screen('chat').ids.msg.text = 'MSG: '
        elif text == 'PRIVATE':
            sm.get_screen('chat').ids.msg.text = 'PRIVATE: '
        elif text == 'NICK':
            sm.get_screen('chat').ids.msg.text = 'NICK: '
        elif text == 'EXIT':
            sm.get_screen('chat').ids.msg.text = 'Exit'
    

    
# Classe Inicial que faz referência a classe <Inicial> do arquivo .kv
class Inicial(Screen):
    global sm

    # Função de envio de dados ao servidor
    def send(self, nome):
        # Inicia a thread com a função receive()
        Thread(target=Chat.receive, args=(Chat,)).start()

        try:
            # Envia os bytes codificados em UTF-8
            cliente.send(bytes(nome, "utf8"))

        except Exception as a:
            # Escreve o erro na tela
            print("Ocorreu algum erro", a)

    # Função que verifica nome vazio
    def verificanick(self, nome):
         # Caso o nome não for vazio, muda o estado do botão para ativado
        if not nome =='':
            sm.get_screen('inicial').ids.bt.disabled = False

class PyChatApp(App):
    # Função que constrói o App
    # Retorna o ScreenManager (Gerenciador de Telas)
    def build(self):
        global sm

        # Widget ScreenManager que gerencia as telas que o App irá conter
        sm = ScreenManager(transition=NoTransition())
        # Adiciona a tela Inicial
        sm.add_widget(Inicial(name='inicial'))
        # Adiciona a tela Chat
        sm.add_widget(Chat(name='chat'))

        return sm

# Define a cor da Janela como branca
Window.clearcolor = (1, 1, 1, 1)


if __name__ == "__main__":
    # Roda o App
    PyChatApp().run()
