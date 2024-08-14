import threading
import socket
from datetime import datetime
from Cryptodome.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad

class CLIENT:
    def __init__(self, host, port, senha, nick):
        self.host = host
        self.port = port
        self.senha = senha
        self.nick = nick
        
    def conectar(self):
        try:
            key = self.senha
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.s:
                self.s.connect((self.host, self.port))
                threading.Thread(target=self.enviarmsg, args=([key]), daemon=True).start()
                self.receber(key)
                
                
                
        except:
            pass
                
    
    def receber(self, key):
        while True:
            data = self.s.recv(6144)
            if data == b'stop':
                print("Um cliente foi desconectado.")
            else:
                data = self.descriptografar(key, data)
                print(data)
    

    def enviarmsg(self, key):
        print('Digite sua mensagem e aperte enter para enviar')
        while True:
            hora = datetime.now()
            horaT = hora.strftime("%H:%M")
            #print("["+horaT+"]" + self.nick + ": ", end='')
            print("["+horaT+"] " + self.nick + ': ', end='')
            msg = input('')
            if msg == "stop":
                print("Conexão Encerrada")
                self.s.sendall(b'stop')
                self.s.close()
                return False
                
            if msg != "":
                msgFormatada = "["+horaT+"] " + self.nick + ": " + msg
                enviar = self.criptografar(key, msgFormatada)
                self.s.sendall(enviar)
    def criptografar(self, senha, text):
        try:
            codificacao = AES.new(senha.encode("utf-8"), AES.MODE_CBC)
            vetor_inicializacao = codificacao.iv
            textocodificado = vetor_inicializacao + codificacao.encrypt(pad(bytes(text, encoding='utf8'), AES.block_size))
            return textocodificado
        except:
            print("Houve um erro ao criptografar a mensagem.")
            exit()
    def descriptografar(self, senha, text):
        try:
            vetor_inicializacao = text[:16]
            codificacao = AES.new(senha.encode("utf-8"), AES.MODE_CBC, vetor_inicializacao)
            textodecodificado = (unpad(codificacao.decrypt(text[16:]), AES.block_size)).decode()
            return textodecodificado
        except:
            print("Houve um erro para decodificar a mensagem recebida.")
            

ip = input("Digite o ip do servidor: ")
port = int(input("Digite a porta da conexão "))
senha = input("Digite a senha de 16 caracteres para conexão: ")
nick = input("Digite seu Nick: ")
a = CLIENT(ip, port, senha, nick)
a.conectar()