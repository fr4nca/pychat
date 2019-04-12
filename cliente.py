# Importações
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty


# Constantes globais
# Endereço do servidor
HOST = '127.0.0.1'
PORT = 12332
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

Builder.load_file('pychat.kv')


class Chat(Screen):
    global sm

    def __init__(self, **kwargs):
        super(Chat, self).__init__(**kwargs)

    def receive(self):
        # Loop eterno
        while True:
            try:
                # Buffer de recepção dos bytes decodificados do servidor
                msg = cliente.recv(1024).decode("utf8")
                print(msg)
                sm.get_screen('chat').ids.box.add_widget(Label(text=msg, color=(0, 0, 0, 0)))
                # self.msgbox.add_widget(Label(text='kldsmlkfmslkdfmslkdfm'))
                # Escreve a mensagem na tela
            except Exception as e:
                # Escreve o erro na tela
                print("Ocorreu algum erro", e)

    def send_msg(self, msg):
        try:
            cliente.send(bytes(msg, 'utf8'))                
        except Exception as a:
            print('Ocorreu algum erro', a)

    def spinner(self, spinner, text):
        if text == 'MSG':
            sm.get_screen('chat').ids.msg.text = 'MSG: '
        elif text == 'PRIVATE':
            sm.get_screen('chat').ids.msg.text = 'PRIVATE: '
        elif text == 'NICK':
            sm.get_screen('chat').ids.msg.text = 'NICK: '
        elif text == 'EXIT':
            sm.get_screen('chat').ids.msg.text = 'Exit'
    # Função de envio de dados ao servidor

    

class Inicial(Screen):
    def send(self, nome):
        Thread(target=Chat.receive, args=(Chat,)).start()
        try:
            # Buffer de leitura
            cliente.send(bytes(nome, "utf8"))
            # Envia os bytes codificados em UTF-8
        except Exception as a:
            # Escreve o erro na tela
            print("Ocorreu algum erro", a)


class PyChatApp(App):

    def build(self):
        global sm
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(Inicial(name='inicial'))
        sm.add_widget(Chat(name='chat'))
        return sm


Window.clearcolor = (1, 1, 1, 1)
if __name__ == "__main__":
    PyChatApp().run()

    # Inicia a Thread com a função receive()

    # Inicia a função send()
