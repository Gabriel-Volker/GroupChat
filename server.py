import socket
from threading import Thread
from time import sleep
import sys


class SERVER:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.text = None
        self.contadordethread = -1
        self.clientes = []
        self.threads = []
    def connect(self):
        #try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((self.host, self.port))
                s.listen()
                while True:
                    if self.threads != []:
                        for threadzinha in self.threads:
                            if threadzinha.is_alive() == False:
                                print("Thread: ", threadzinha, " esta morta!")
                                self.threads.remove(threadzinha)
                    self.conn, self.addr = s.accept()
                    self.clientes.append(self.conn)
                    threadzada = Thread(target=self.thread_cliente, args=(self.addr, self.conn,), daemon=True)
                    self.threads.append(threadzada)
                    threadzada.start()
                    if self.threads != []:
                        for threadzinha in self.threads:
                            if threadzinha.is_alive() == False:
                                print("Thread: ", threadzinha, " esta morta!")
                                self.threads.remove(threadzinha)
                    self.contadordethread += 1
                    print(self.contadordethread)
                    print(self.threads)    
        #except:
        #    print('Houve um erro na conexão')
    def enviarmsg(self, data, con_atual):
        for clientes in self.clientes:
            if clientes != con_atual:
                clientes.sendall(data)
        print(self.contadordethread)
        return True
            
            
            
    def thread_cliente(self, addr, conn,):
        print(f"Conectado em: {addr}")
        while True:
            try:
                data = conn.recv(6144)
                print(data)
                if data != b'' and data != '' and data != b'stop' and data != None: #and data != None
                    self.enviarmsg(data, conn)  
                else:
                    print(f"{addr} se desconectou!")
                    conn.close()
                    self.clientes.remove(conn)
                    break
            except:
                print("Erro, desligando thread {}".format(addr))
                self.clientes.remove(conn)
                sys.exit()
                break
            

#ip = input("Digite seu ip interno: ")
#port = int(input("Digite a porta da conexão: "))
conexao = SERVER("0.0.0.0", 44444)
while True:
    conexao.connect()